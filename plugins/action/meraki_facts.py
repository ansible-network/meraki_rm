"""Action plugin for meraki_facts module."""

from __future__ import annotations

from .base_action import BaseResourceActionPlugin


class ActionModule(BaseResourceActionPlugin):
    MODULE_NAME = 'facts'

    def run(self, tmp=None, task_vars=None):
        super().run(tmp, task_vars)
        if task_vars is None:
            task_vars = {}

        args = self._task.args.copy()

        try:
            gather_subset = set(args.get('gather_subset', ['all']))
            org_id = args.get('organization_id')
            network_id = args.get('network_id')

            manager = self._get_or_spawn_manager(task_vars)

            facts_args = {
                'gather_subset': list(gather_subset),
                'organization_id': org_id,
                'network_id': network_id,
            }
            result = manager.execute('find', self.MODULE_NAME, facts_args)

            ansible_facts = {}
            ansible_facts['meraki_organizations'] = result.get('organizations', [])
            ansible_facts['meraki_networks'] = result.get('networks', [])
            ansible_facts['meraki_devices'] = result.get('devices', [])
            ansible_facts['meraki_inventory'] = result.get('inventory', [])

            return {
                'failed': False,
                'changed': False,
                'ansible_facts': ansible_facts,
            }
        except Exception as e:
            return {'failed': True, 'msg': str(e)}
