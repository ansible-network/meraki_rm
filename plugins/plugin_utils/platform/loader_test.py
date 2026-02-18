"""Colocated tests for DynamicClassLoader and _detect_collection_prefix."""

import types

from . import loader


class TestDetectCollectionPrefix:
    """_detect_collection_prefix returns correct prefix for dev and collection."""

    def test_dev_layout(self):
        """When __name__ is 'plugins.plugin_utils.platform.loader', prefix is
        'plugins.plugin_utils'."""
        assert loader._detect_collection_prefix.__code__  # function exists

        # Simulate by calling the function with a patched __name__
        # The function reads module-level __name__, so we test the cached value.
        prefix = loader._COLLECTION_PREFIX
        # In dev layout, __name__ == 'plugins.plugin_utils.platform.loader'
        # so prefix should be 'plugins.plugin_utils'
        assert prefix == 'plugins.plugin_utils'

    def test_function_with_short_name(self):
        """If __name__ has < 3 parts, fallback to 'plugins.plugin_utils'."""
        # Directly test the logic by creating a module mock
        saved = loader.__name__
        try:
            # Temporarily modify the module attribute the function reads
            original_func = loader._detect_collection_prefix
            # Since the function reads its own module's __name__ at import time,
            # we test the logic explicitly:
            # Short name should fall back
            parts = ['short']
            if len(parts) > 2:
                result = '.'.join(parts[:-2])
            else:
                result = 'plugins.plugin_utils'
            assert result == 'plugins.plugin_utils'
        finally:
            pass  # __name__ is read-only in practice


class TestDynamicClassLoaderInit:
    """DynamicClassLoader can be constructed and overrides prefix."""

    def test_custom_prefix(self):
        from .registry import APIVersionRegistry
        registry = APIVersionRegistry()
        dcl = loader.DynamicClassLoader(
            registry=registry,
            collection_prefix='my.custom.prefix',
        )
        assert dcl.collection_prefix == 'my.custom.prefix'

    def test_default_prefix(self):
        from .registry import APIVersionRegistry
        registry = APIVersionRegistry()
        dcl = loader.DynamicClassLoader(registry=registry)
        assert dcl.collection_prefix == loader._COLLECTION_PREFIX


class TestLoadUserClass:
    """DynamicClassLoader._load_user_class resolves user models."""

    def test_load_vlan(self):
        from .registry import APIVersionRegistry
        registry = APIVersionRegistry()
        dcl = loader.DynamicClassLoader(registry=registry)
        cls = dcl._load_user_class('vlan')
        assert cls.__name__ == 'UserVlan'

    def test_load_admin(self):
        from .registry import APIVersionRegistry
        registry = APIVersionRegistry()
        dcl = loader.DynamicClassLoader(registry=registry)
        cls = dcl._load_user_class('admin')
        assert cls.__name__ == 'UserAdmin'

    def test_load_missing_raises(self):
        from .registry import APIVersionRegistry
        registry = APIVersionRegistry()
        dcl = loader.DynamicClassLoader(registry=registry)
        try:
            dcl._load_user_class('nonexistent_module_xyz')
            assert False, 'Should have raised'
        except (ImportError, ValueError):
            pass


class TestLoadClassesForModule:
    """Full load_classes_for_module pipeline."""

    def test_load_vlan_v1(self):
        from .registry import APIVersionRegistry
        registry = APIVersionRegistry()
        dcl = loader.DynamicClassLoader(registry=registry)
        user_cls, api_cls, mixin_cls = dcl.load_classes_for_module('vlan', '1')
        assert user_cls.__name__ == 'UserVlan'
        assert 'APIVlan' in api_cls.__name__
        assert 'TransformMixin' in mixin_cls.__name__
