"""Base action plugin for Meraki Dashboard resource modules.

Provides a data-driven run() that eliminates per-module boilerplate.
Each resource action plugin declares class-level attributes and the
base class handles validation, state dispatch, and manager interaction.

Subclass contract:
    MODULE_NAME    — resource identifier (e.g. 'vlan')
    SCOPE_PARAM    — scope kwarg name ('network_id', 'organization_id', 'serial')
    USER_MODEL     — dotted import path to the User Model dataclass
    CANONICAL_KEY  — human-facing field for matching (e.g. 'name', 'email', 'vlan_id')
    SYSTEM_KEY     — API-generated identity field for URL routing (e.g. 'admin_id')
                     None when CANONICAL_KEY is also the API routing key (Category A)
    SUPPORTS_DELETE — False for singletons that cannot be removed
    DOCUMENTATION  — imported from the corresponding plugins/modules/ file

Identity categories (see docs/05-design-principles.md, Principle 2):
    Category A: CANONICAL_KEY set, SYSTEM_KEY=None  — user key IS the API key
    Category B: CANONICAL_KEY set, SYSTEM_KEY set   — match by canonical, resolve system
    Category C: CANONICAL_KEY=None, SYSTEM_KEY set  — gather-first, user provides system key

For the common case the subclass needs NO run() override at all. Modules
with custom logic (e.g. meraki_facts) override run() as before.
"""

from __future__ import annotations

import base64
import fcntl
import importlib
import logging
import os
import secrets
import time
from pathlib import Path

import yaml
from ansible.errors import AnsibleError
from ansible.module_utils.common.arg_spec import ArgumentSpecValidator
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

logger = logging.getLogger(__name__)
display = Display()


class BaseResourceActionPlugin(ActionBase):
    """Data-driven base action plugin for all Meraki resource modules.

    Subclasses declare metadata as class attributes:

        class ActionModule(BaseResourceActionPlugin):
            MODULE_NAME     = 'vlan'
            SCOPE_PARAM     = 'network_id'
            USER_MODEL      = 'plugins.plugin_utils.user_models.vlan.UserVlan'
            CANONICAL_KEY   = 'vlan_id'
            SUPPORTS_DELETE = True

    The base run() validates input, loops over config items, builds User
    Model instances, and dispatches to the manager.  Only meraki_facts
    needs a custom run().
    """

    # --- subclass must set these ----------------------------------------
    MODULE_NAME: str = None
    SCOPE_PARAM: str = 'network_id'
    USER_MODEL: str = None
    CANONICAL_KEY: str = None
    SYSTEM_KEY: str = None
    SUPPORTS_DELETE: bool = True

    # Canonical resource module states
    VALID_STATES = frozenset({
        'merged', 'replaced', 'overridden', 'deleted', 'gathered',
    })

    # Resolved lazily by _get_user_model_class()
    _user_model_cls = None

    @property
    def _match_key(self) -> str:
        """The field used to index and match resources.

        Returns CANONICAL_KEY when set (Categories A and B), otherwise
        falls back to SYSTEM_KEY (Category C — gather-first resources).
        """
        return self.CANONICAL_KEY or self.SYSTEM_KEY

    def _index_by_key(self, items: list, key: str) -> dict:
        """Index a list of resource dicts by *key*, detecting duplicates.

        Raises AnsibleError when two resources share the same canonical key
        value, directing the user to provide the SYSTEM_KEY to disambiguate.
        """
        index = {}
        for item in items:
            k = str(item.get(key, ''))
            if not k:
                continue
            if k in index and key == self.CANONICAL_KEY and self.SYSTEM_KEY:
                raise AnsibleError(
                    f"Duplicate {key}='{k}' found in existing resources. "
                    f"Provide '{self.SYSTEM_KEY}' in your config to "
                    f"disambiguate."
                )
            index[k] = item
        return index

    def _prepare_user_data(self, item, current, scope_value, user_cls):
        """Build user_data, injecting the system key from a matched resource.

        When SYSTEM_KEY is set and the user did not provide it, copy it
        from the matched ``current`` resource so the platform manager can
        resolve the API path parameter for update/delete operations.
        """
        effective_item = dict(item)
        if self.SYSTEM_KEY and current is not None:
            if not effective_item.get(self.SYSTEM_KEY):
                effective_item[self.SYSTEM_KEY] = current[self.SYSTEM_KEY]
        return user_cls(**{self.SCOPE_PARAM: scope_value}, **effective_item)

    # ------------------------------------------------------------------ #
    #  Data-driven run()                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _resolve_plugin_path(dotted_path: str) -> str:
        """Rewrite a 'plugins.plugin_utils...' path to the real namespace.

        When Ansible loads the collection, the package prefix is
        'ansible_collections.cisco.meraki_rm.plugins.plugin_utils', not
        bare 'plugins.plugin_utils'. Detect the correct prefix from
        this module's own __name__.
        """
        _DEV_PREFIX = 'plugins.plugin_utils'
        if dotted_path.startswith(_DEV_PREFIX):
            my_name = __name__  # e.g. ansible_collections.cisco.meraki_rm.plugins.action.base_action
            parts = my_name.split('.')
            # Walk up from action.base_action → plugins → prepend
            if 'plugins' in parts:
                idx = parts.index('plugins')
                real_prefix = '.'.join(parts[:idx]) + '.' + _DEV_PREFIX
                return real_prefix + dotted_path[len(_DEV_PREFIX):]
        return dotted_path

    def _get_user_model_class(self):
        """Lazily resolve USER_MODEL dotted path to a class object."""
        if self._user_model_cls is not None:
            return self._user_model_cls

        if not self.USER_MODEL:
            raise AnsibleError(
                f"{type(self).__name__}.USER_MODEL is not set"
            )

        resolved = self._resolve_plugin_path(self.USER_MODEL)
        module_path, class_name = resolved.rsplit('.', 1)
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        type(self)._user_model_cls = cls
        return cls

    def _get_documentation(self) -> str:
        """Auto-discover DOCUMENTATION from the sibling modules/ package.

        Derives the module file name from the action plugin file name
        (both are always ``meraki_<name>.py``).  Tries a package-relative
        import first (works in both flat dev layout and installed collection),
        then falls back to the full collection namespace.
        """
        if not self.MODULE_NAME:
            return ''

        # Derive module name from action plugin filename convention
        action_mod = type(self).__module__            # e.g. ...plugins.action.meraki_appliance_vlan
        action_leaf = action_mod.rsplit('.', 1)[-1]   # meraki_appliance_vlan
        module_leaf = action_leaf                      # same filename in modules/

        # Try relative import (..modules.meraki_appliance_vlan)
        parent_pkg = action_mod.rsplit('.', 2)[0]     # ...plugins
        for candidate in (
            f'{parent_pkg}.modules.{module_leaf}',
            f'ansible_collections.cisco.meraki_rm.plugins.modules.{module_leaf}',
        ):
            try:
                mod = importlib.import_module(candidate)
                doc = getattr(mod, 'DOCUMENTATION', None)
                if doc:
                    return doc
            except (ImportError, ModuleNotFoundError):
                continue

        return ''

    def run(self, tmp=None, task_vars=None):
        """Data-driven resource module execution.

        Follows the standard Ansible network resource module pattern:
          1. Gather current state → ``before``
          2. Apply desired mutations based on ``state``
          3. Gather resulting state → ``after``
          4. ``changed = (before != after)``

        Supports ``--check`` (dry-run) and ``--diff`` modes:

        - **Check mode**: gathers ``before``, predicts ``after`` from set
          theory without making API calls, reports ``changed`` accurately.
        - **Diff mode**: attaches a YAML-formatted ``diff`` to the result
          showing ``before`` vs ``after`` state.

        Return structure matches cisco.ios / cisco.nxos conventions::

            {
                "before": [ ... ],   # config before this run
                "after":  [ ... ],   # config after this run
                "changed": bool,
                "gathered": [ ... ], # only for state=gathered
                "diff": { ... },     # only when --diff is active
            }

        Subclasses with truly unique logic (meraki_facts) override this.
        """
        super().run(tmp, task_vars)
        if task_vars is None:
            task_vars = {}

        self._manager_socket = None
        self._manager_authkey_b64 = None

        args = self._task.args.copy()

        try:
            doc = self._get_documentation()
            if doc:
                argspec = self._build_argspec_from_docs(doc)
                validated_args = self._validate_data(args, argspec, 'input')
            else:
                argspec = None
                validated_args = args

            state = validated_args.get('state', 'merged')
            config = validated_args.get('config', [])
            scope_value = validated_args.get(self.SCOPE_PARAM)

            manager = self._get_or_spawn_manager(task_vars)
            user_cls = self._get_user_model_class()

            # -- gathered: read-only, no before/after -----------------------
            if state == 'gathered':
                gathered = self._do_gathered(
                    manager, user_cls, scope_value, config,
                )
                if argspec and gathered:
                    gathered = self._validate_output(gathered, argspec)
                return self._build_result(
                    failed=False, changed=False,
                    gathered=gathered, config=gathered,
                )

            # -- mutating states: before → apply → after --------------------
            before = self._do_gathered(
                manager, user_cls, scope_value, None,
            )
            if argspec and before:
                before = self._validate_output(before, argspec)

            # -- check mode: predict after without applying -----------------
            if self._task.check_mode:
                after = self._predict_after(state, before, config)
                changed = self._lists_differ(before, after)
                return self._build_result(
                    failed=False, changed=changed,
                    before=before, after=after, config=after,
                )

            if state in ('deleted', 'overridden') and not self.SUPPORTS_DELETE:
                raise AnsibleError(
                    f"State '{state}' requires delete capability, but "
                    f"{self.__class__.__name__} has SUPPORTS_DELETE=False."
                )

            if state == 'deleted':
                self._apply_deleted(
                    manager, user_cls, scope_value, config, before,
                )
            elif state == 'overridden':
                self._apply_overridden(
                    manager, user_cls, scope_value, config, before,
                )
            else:  # merged, replaced
                self._apply_merged_or_replaced(
                    manager, user_cls, scope_value, config, state, before,
                )

            after = self._do_gathered(
                manager, user_cls, scope_value, None,
            )
            if argspec and after:
                after = self._validate_output(after, argspec)

            changed = self._lists_differ(before, after)

            return self._build_result(
                failed=False, changed=changed,
                before=before, after=after, config=after,
            )
        except Exception as e:
            msg = str(e) or f"{type(e).__name__} (no message)"
            return self._build_result(failed=True, msg=msg)

    def _build_result(self, **kwargs):
        """Build result dict, injecting ansible_facts and optional diff."""
        result = dict(kwargs)
        if self._manager_socket and self._manager_authkey_b64:
            result['ansible_facts'] = {
                'platform_manager_socket': self._manager_socket,
                'platform_manager_authkey': self._manager_authkey_b64,
            }
        if (getattr(self._task, 'diff', False)
                and 'before' in result and 'after' in result
                and result.get('before') is not None
                and result.get('after') is not None):
            result['diff'] = {
                'before': yaml.dump(
                    result['before'], default_flow_style=False, sort_keys=True,
                ),
                'after': yaml.dump(
                    result['after'], default_flow_style=False, sort_keys=True,
                ),
            }
        return result

    # ------------------------------------------------------------------ #
    #  State dispatch helpers                                              #
    # ------------------------------------------------------------------ #

    def _do_gathered(self, manager, user_cls, scope_value, config):
        """Gather current resource state (read-only)."""
        results = []
        for item in config or [{}]:
            user_data = user_cls(**{self.SCOPE_PARAM: scope_value}, **item)
            result = manager.execute('find', self.MODULE_NAME, user_data)
            if isinstance(result, dict) and 'config' in result:
                results.extend(result['config'])
            else:
                results.append(result)
        return results

    def _apply_deleted(self, manager, user_cls, scope_value, config, before):
        """Delete specified resources.

        Matches by canonical key (or system key for Category C).
        Skips items not present in ``before`` (already absent).
        Injects the system key from ``before`` when needed for API routing.
        """
        match_key = self._match_key
        if not match_key:
            return

        before_by_key = self._index_by_key(before, match_key)
        before_by_sys = (
            self._index_by_key(before, self.SYSTEM_KEY)
            if self.SYSTEM_KEY else {}
        )

        for item in config:
            current = None
            if self.SYSTEM_KEY and item.get(self.SYSTEM_KEY):
                current = before_by_sys.get(str(item[self.SYSTEM_KEY]))
            elif match_key and item.get(match_key):
                current = before_by_key.get(str(item[match_key]))

            if current is None:
                continue

            user_data = self._prepare_user_data(
                item, current, scope_value, user_cls,
            )
            manager.execute('delete', self.MODULE_NAME, user_data)

    def _apply_merged_or_replaced(self, manager, user_cls, scope_value,
                                   config, state, before):
        """Create or update resources, skipping items already at desired state.

        Uses ``before`` to decide create vs update and to skip no-ops.
        When SYSTEM_KEY is set, injects the resolved system key from
        matched ``before`` items so the platform manager can route API calls.
        """
        operation = self._detect_operation({'state': state})
        match_key = self._match_key

        before_by_key = (
            self._index_by_key(before, match_key) if match_key else {}
        )
        before_by_sys = (
            self._index_by_key(before, self.SYSTEM_KEY)
            if self.SYSTEM_KEY else {}
        )

        for item in config:
            current = None

            if self.SYSTEM_KEY and item.get(self.SYSTEM_KEY):
                current = before_by_sys.get(str(item[self.SYSTEM_KEY]))
            elif match_key and item.get(match_key):
                current = before_by_key.get(str(item[match_key]))

            if match_key:
                if current is not None:
                    if self._config_matches(item, current):
                        continue
                    op = 'update' if state == 'merged' else operation
                elif item.get(match_key) or item.get(self.SYSTEM_KEY):
                    op = 'create'
                else:
                    op = 'create'
            else:
                if before and self._config_matches(item, before[0]):
                    continue
                op = operation

            user_data = self._prepare_user_data(
                item, current, scope_value, user_cls,
            )
            manager.execute(op, self.MODULE_NAME, user_data)

    def _apply_overridden(self, manager, user_cls, scope_value, config,
                           before):
        """Override: delete extras, then replace each desired item.

        Uses ``before`` (already gathered by run()) to determine extras.
        Matches by canonical key; injects system key for API routing.
        Skips replace for items already matching desired state.
        """
        match_key = self._match_key
        if not match_key:
            return

        before_by_key = self._index_by_key(before, match_key)
        desired_keys = set()

        for item in config:
            key_val = item.get(match_key)
            if key_val is not None:
                desired_keys.add(str(key_val))

        # Delete extras (current items not in desired set)
        for current in before:
            current_key = str(current.get(match_key, ''))
            if current_key and current_key not in desired_keys:
                delete_item = {match_key: current.get(match_key)}
                delete_data = self._prepare_user_data(
                    delete_item, current, scope_value, user_cls,
                )
                manager.execute('delete', self.MODULE_NAME, delete_data)

        # Replace each desired item (skip no-ops)
        for item in config:
            current = None
            if match_key and item.get(match_key):
                current = before_by_key.get(str(item[match_key]))
                if current and self._config_matches(item, current):
                    continue

            user_data = self._prepare_user_data(
                item, current, scope_value, user_cls,
            )
            manager.execute('replace', self.MODULE_NAME, user_data)

    @staticmethod
    def _config_matches(desired: dict, current: dict) -> bool:
        """Check if every user-supplied field in desired matches current.

        Only compares fields explicitly provided by the user (non-None).
        Extra fields in current (from API defaults) are ignored.
        """
        for key, desired_val in desired.items():
            if desired_val is None:
                continue
            current_val = current.get(key)
            if str(desired_val) != str(current_val):
                return False
        return True

    @staticmethod
    def _lists_differ(before: list, after: list) -> bool:
        """Compare two config lists to determine if anything changed.

        Handles None values and type mismatches by normalizing to strings.
        """
        if len(before) != len(after):
            return True
        for b, a in zip(
            sorted(before, key=lambda x: str(x)),
            sorted(after, key=lambda x: str(x)),
        ):
            if b != a:
                return True
        return False

    # ------------------------------------------------------------------ #
    #  Check mode: predict after state from set theory                     #
    # ------------------------------------------------------------------ #

    def _predict_after(self, state, before, config):
        """Predict the resulting state without making API calls.

        Implements the set-theoretic state operations:
          merged:     C' = C ∪ D   (additive merge)
          replaced:   C' = (C \\ K(D)) ∪ D   (item-level replacement)
          overridden: C' = D   (set equality)
          deleted:    C' = C \\ D   (set difference)
        """
        match_key = self._match_key
        before_by_key = {}
        if match_key:
            for item in before:
                k = str(item.get(match_key, ''))
                if k:
                    before_by_key[k] = item

        if state == 'deleted':
            return self._predict_deleted(before, config, before_by_key)
        elif state == 'overridden':
            return self._predict_overridden(before, config, before_by_key)
        elif state == 'replaced':
            return self._predict_replaced(before, config, before_by_key)
        else:  # merged
            return self._predict_merged(before, config, before_by_key)

    def _predict_merged(self, before, config, before_by_key):
        """Predict merged: union — add new items, merge fields into existing."""
        match_key = self._match_key
        result = [dict(item) for item in before]
        result_by_key = {}
        if match_key:
            for item in result:
                k = str(item.get(match_key, ''))
                if k:
                    result_by_key[k] = item

        for item in config:
            if match_key and item.get(match_key):
                key = str(item[match_key])
                existing = result_by_key.get(key)
                if existing is not None:
                    for field, val in item.items():
                        if val is not None:
                            existing[field] = val
                else:
                    new_item = dict(item)
                    result.append(new_item)
                    result_by_key[key] = new_item
            elif not match_key and before:
                for field, val in item.items():
                    if val is not None:
                        result[0][field] = val
            else:
                result.append(dict(item))
        return result

    def _predict_replaced(self, before, config, before_by_key):
        """Predict replaced: item-level replacement, untouched items preserved."""
        match_key = self._match_key
        result = [dict(item) for item in before]
        result_by_key = {}
        if match_key:
            for i, item in enumerate(result):
                k = str(item.get(match_key, ''))
                if k:
                    result_by_key[k] = i

        for item in config:
            if match_key and item.get(match_key):
                key = str(item[match_key])
                idx = result_by_key.get(key)
                if idx is not None:
                    result[idx] = dict(item)
                else:
                    result.append(dict(item))
                    result_by_key[key] = len(result) - 1
            elif not match_key and before:
                result[0] = dict(item)
            else:
                result.append(dict(item))
        return result

    @staticmethod
    def _predict_overridden(before, config, before_by_key):
        """Predict overridden: set equality — result is exactly the desired set."""
        return [dict(item) for item in config]

    def _predict_deleted(self, before, config, before_by_key):
        """Predict deleted: set difference — remove items whose keys match."""
        match_key = self._match_key
        if not config:
            return []
        if not match_key:
            return []

        delete_keys = set()
        for item in config:
            k = item.get(match_key)
            if k is not None:
                delete_keys.add(str(k))

        return [
            dict(item) for item in before
            if str(item.get(match_key, '')) not in delete_keys
        ]

    # ------------------------------------------------------------------ #
    #  Manager lifecycle                                                   #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _runtime_dir():
        """Return a user-private runtime directory for sockets, keys, PIDs.

        Prefers $XDG_RUNTIME_DIR (per-user tmpfs, 0700).  Falls back to
        /tmp/meraki_rm_<uid> created with mode 0700.
        """
        base = os.environ.get('XDG_RUNTIME_DIR')
        if base:
            d = Path(base) / 'meraki_rm'
        else:
            d = Path(f'/tmp/meraki_rm_{os.getuid()}')
        d.mkdir(mode=0o700, exist_ok=True)
        return d

    def _get_or_spawn_manager(self, task_vars: dict):
        """Get existing manager or spawn a new one.

        The manager is **always** detached from Python's atexit cleanup so
        it survives Ansible fork-worker exits (task-to-task reuse).

        Lifecycle is controlled by a ``.survive`` flag file in the runtime
        directory:

        - **No flag file (production)**: The server process watches
          ``os.getppid()`` and shuts itself down when the parent
          ``ansible-playbook`` process exits.  No orphans.
        - **Flag file present (Molecule)**: No watchdog — the manager
          lives indefinitely across playbooks.  ``default/destroy.yml``
          kills it via the PID file and removes all runtime files.

        Reconnection tiers:

        1. **ansible_facts** — socket/authkey injected by a prior task in
           the same playbook (zero I/O, fastest).
        2. **socket + keyfile** — the manager from a prior task/playbook
           is still alive on disk.

        A filelock serializes spawn-or-connect across parallel worker
        processes so only one process spawns and the others connect.

        Returns:
            ManagerRPCClient instance
        """
        from ..plugin_utils.manager.rpc_client import ManagerRPCClient

        hostvars = task_vars.get('hostvars', {})
        inventory_hostname = task_vars.get('inventory_hostname', 'localhost')
        host_vars = hostvars.get(inventory_hostname, {})

        meraki_url = host_vars.get('meraki_dashboard_url')
        meraki_api_key = host_vars.get('meraki_api_key')

        if not meraki_url:
            raise AnsibleError(
                "meraki_dashboard_url must be defined in inventory or host_vars"
            )
        if not meraki_api_key:
            raise AnsibleError(
                "meraki_api_key must be defined in inventory or host_vars"
            )

        runtime = self._runtime_dir()
        stem = f'manager_{inventory_hostname}'
        socket_path = str(runtime / f'{stem}.sock')
        keyfile = runtime / f'{stem}.key'
        pidfile = runtime / f'{stem}.pid'

        # ── Tier 1: ansible_facts from a prior task in this playbook ──
        cached_socket = task_vars.get('platform_manager_socket')
        cached_authkey_b64 = task_vars.get('platform_manager_authkey')

        if cached_socket and cached_authkey_b64 and Path(cached_socket).exists():
            try:
                authkey = base64.b64decode(cached_authkey_b64)
                client = ManagerRPCClient(meraki_url, cached_socket, authkey)
                display.v("Platform Manager: Tier-1 reconnect via ansible_facts")
                return client
            except Exception as e:
                display.v(f"Platform Manager: Tier-1 reconnect failed: {e}")

        # ── Tier 2+Spawn under filelock ────────────────────────────────
        # Serialize across parallel worker processes so exactly one
        # spawns the manager and the rest connect via Tier 2.
        lockfile_path = runtime / f'{stem}.lock'
        lockfile = open(lockfile_path, 'w')
        try:
            fcntl.flock(lockfile, fcntl.LOCK_EX)

            # Re-check Tier 2 after acquiring lock — another process
            # may have spawned the manager while we waited.
            if Path(socket_path).exists() and keyfile.exists():
                try:
                    authkey = keyfile.read_bytes()
                    client = ManagerRPCClient(meraki_url, socket_path, authkey)
                    display.v(
                        f"Platform Manager: Tier-2 reconnect via keyfile "
                        f"at {socket_path}"
                    )
                    return client
                except Exception as e:
                    display.v(
                        f"Platform Manager: Tier-2 reconnect failed "
                        f"(stale): {e}"
                    )
                    Path(socket_path).unlink(missing_ok=True)
                    keyfile.unlink(missing_ok=True)
                    pidfile.unlink(missing_ok=True)

            # ── Spawn a new manager ───────────────────────────────────
            survive = (runtime / f'{stem}.survive').exists()
            display.v(
                f"Platform Manager: spawning new instance "
                f"(survive={survive})"
            )

            from ..plugin_utils.manager.platform_manager import (
                PlatformManager,
                PlatformService,
            )

            authkey = secrets.token_bytes(32)

            service = PlatformService(meraki_url, meraki_api_key)
            PlatformManager.register(
                'get_platform_service',
                callable=lambda: service,
            )

            manager = PlatformManager(address=socket_path, authkey=authkey)
            manager.start()

            # Detach from Python's atexit so the server survives
            # fork-worker exits.
            import multiprocessing.process
            from multiprocessing.util import _finalizer_registry
            multiprocessing.process._children.discard(manager._process)
            fin = manager.shutdown
            if hasattr(fin, '_key') and fin._key in _finalizer_registry:
                del _finalizer_registry[fin._key]

            max_wait = 50
            for _ in range(max_wait):
                if Path(socket_path).exists():
                    break
                time.sleep(0.1)
            else:
                raise RuntimeError(
                    f"Manager socket not ready after {max_wait * 0.1}s"
                )

            # Persist runtime files for Tier-2 reconnection.
            old_umask = os.umask(0o177)
            try:
                keyfile.write_bytes(authkey)
            finally:
                os.umask(old_umask)
            pidfile.write_text(str(manager._process.pid))

            display.v(
                f"Platform Manager: spawned PID {manager._process.pid} "
                f"at {socket_path}"
            )

            client = ManagerRPCClient(meraki_url, socket_path, authkey)

            self._manager_socket = socket_path
            self._manager_authkey_b64 = base64.b64encode(
                authkey,
            ).decode('utf-8')

            return client
        finally:
            fcntl.flock(lockfile, fcntl.LOCK_UN)
            lockfile.close()

    def _build_argspec_from_docs(self, documentation: str) -> dict:
        """
        Build argument spec from DOCUMENTATION string.

        Parses the YAML documentation and extracts the options dict
        plus any constraint lists (mutually_exclusive, etc.).

        Args:
            documentation: DOCUMENTATION string from module

        Returns:
            Dict with 'argument_spec' (param_name -> spec) and
            constraint keys for ArgumentSpecValidator

        Raises:
            ValueError: If documentation cannot be parsed
        """
        try:
            doc_data = yaml.safe_load(documentation)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse DOCUMENTATION: {e}") from e

        return {
            'argument_spec': doc_data.get('options', {}),
            'mutually_exclusive': doc_data.get('mutually_exclusive', []),
            'required_together': doc_data.get('required_together', []),
            'required_one_of': doc_data.get('required_one_of', []),
            'required_if': doc_data.get('required_if', []),
        }

    def _validate_data(
        self,
        data: dict,
        argspec: dict,
        direction: str
    ) -> dict:
        """
        Validate data against argument spec.

        Uses Ansible's ArgumentSpecValidator to validate
        both input (from playbook) and output (from manager).

        Args:
            data: Data dict to validate
            argspec: Dict with 'argument_spec' and optional constraint keys
            direction: 'input' or 'output' (for error messages)

        Returns:
            Validated and normalized data dict

        Raises:
            AnsibleError: If validation fails
        """
        validator = ArgumentSpecValidator(
            argspec['argument_spec'],
            mutually_exclusive=argspec.get('mutually_exclusive', []),
            required_together=argspec.get('required_together', []),
            required_one_of=argspec.get('required_one_of', []),
            required_if=argspec.get('required_if', []),
        )
        result = validator.validate(data)

        if result.error_messages:
            error_msg = (
                f"{direction.title()} validation failed: " +
                ", ".join(result.error_messages)
            )
            raise AnsibleError(error_msg)

        return result.validated_parameters

    def _validate_output(self, results: list, argspec: dict) -> list:
        """Validate return data against the config suboptions schema.

        Ensures the contract with the user: what we return in ``config``
        matches the documented suboptions (field names, types). Items with
        extra keys not in the schema are filtered out; items missing
        required keys log a warning but are still returned.

        This catches bugs where the reverse transform (API → User) produces
        field names or types that don't match the documented interface.
        """
        config_spec = argspec.get('argument_spec', {}).get('config', {})
        suboptions = config_spec.get('suboptions', {})

        if not suboptions:
            return results

        valid_keys = set(suboptions.keys())
        validated = []

        for item in results:
            if not isinstance(item, dict):
                validated.append(item)
                continue

            cleaned = {}
            for key, value in item.items():
                if key not in valid_keys:
                    logger.debug(
                        "Output field %r not in config suboptions — "
                        "stripping from return data", key,
                    )
                elif value is None:
                    continue
                else:
                    cleaned[key] = value

            validated.append(cleaned)

        return validated

    def _detect_operation(self, args: dict) -> str:
        """
        Map resource module state to API operation.

        State-to-operation mapping for resource modules:
        - merged   -> 'update' (create if not exists, update if exists)
        - replaced -> 'replace' (full resource replacement)
        - overridden -> 'override' (replace all instances of this resource type)
        - deleted  -> 'delete'
        - gathered -> 'find'
        Args:
            args: Module arguments

        Returns:
            Operation name

        Raises:
            AnsibleError: If state is unknown
        """
        state = args.get('state', 'merged')

        if state not in self.VALID_STATES:
            raise AnsibleError(
                f"Unknown state: {state}. "
                f"Valid states: {sorted(self.VALID_STATES)}"
            )

        state_to_operation = {
            'merged': 'update',
            'replaced': 'replace',
            'overridden': 'override',
            'deleted': 'delete',
            'gathered': 'find',
        }

        return state_to_operation[state]
