"""Colocated tests for BaseTransformMixin — core transform engine."""

from dataclasses import dataclass, fields
from typing import Any, Dict, Optional

from .base_transform import BaseTransformMixin


# ── Fixtures: minimal dataclasses with a field mapping ──


@dataclass
class FakeAPI(BaseTransformMixin):
    camelField: Optional[str] = None
    anotherOne: Optional[int] = None

    _field_mapping = {
        'snake_field': 'camelField',
        'another_one': 'anotherOne',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        return FakeUser


@dataclass
class FakeUser(BaseTransformMixin):
    snake_field: Optional[str] = None
    another_one: Optional[int] = None
    scope_param: Optional[str] = None

    _field_mapping = {
        'snake_field': 'camelField',
        'another_one': 'anotherOne',
    }

    @classmethod
    def _get_api_class(cls):
        return FakeAPI

    @classmethod
    def _get_ansible_class(cls):
        return cls


@dataclass
class FakeAPIWithHook(BaseTransformMixin):
    camelField: Optional[str] = None
    bonus: Optional[str] = None

    _field_mapping = {
        'snake_field': 'camelField',
    }

    @classmethod
    def _get_api_class(cls):
        return cls

    @classmethod
    def _get_ansible_class(cls):
        return FakeUser

    def _post_transform_hook(self, data: dict, direction: str, context: dict) -> dict:
        if direction == 'reverse':
            data['snake_field'] = (data.get('snake_field') or '') + '_hooked'
        return data


def _ctx():
    return {'manager': None, 'cache': {}}


# ── Forward mapping ──


class TestForwardMapping:
    """User -> API field mapping."""

    def test_basic_forward(self):
        user = FakeUser(snake_field='hello', another_one=42)
        api = user.to_api(_ctx())
        assert isinstance(api, FakeAPI)
        assert api.camelField == 'hello'
        assert api.anotherOne == 42

    def test_none_values_omitted(self):
        user = FakeUser(snake_field='x')
        api = user.to_api(_ctx())
        assert api.camelField == 'x'
        assert api.anotherOne is None


# ── Reverse mapping ──


class TestReverseMapping:
    """API -> User field mapping."""

    def test_basic_reverse(self):
        api = FakeAPI(camelField='world', anotherOne=7)
        user = api.to_ansible(_ctx())
        assert isinstance(user, FakeUser)
        assert user.snake_field == 'world'
        assert user.another_one == 7


# ── Roundtrip ──


class TestRoundtrip:
    """User -> API -> User preserves all mapped fields."""

    def test_roundtrip(self):
        original = FakeUser(snake_field='rt', another_one=99)
        ctx = _ctx()
        api = original.to_api(ctx)
        back = api.to_ansible(ctx)
        assert back.snake_field == original.snake_field
        assert back.another_one == original.another_one


# ── Field filtering: unknown keys don't blow up constructor ──


class TestFieldFiltering:
    """Scope params and extra keys must not leak into target dataclass."""

    def test_scope_param_excluded(self):
        user = FakeUser(snake_field='a', scope_param='SCOPE')
        api = user.to_api(_ctx())
        api_field_names = {f.name for f in fields(api)}
        assert 'scope_param' not in api_field_names

    def test_extra_keys_in_forward_no_error(self):
        """If _field_mapping references a field not on target, it's silently dropped."""
        user = FakeUser(snake_field='x', scope_param='SCOPE')
        api = user.to_api(_ctx())
        assert api.camelField == 'x'


# ── _post_transform_hook ──


class TestPostTransformHook:
    """Subclass hooks modify data after mapping."""

    def test_hook_fires_on_reverse(self):
        api = FakeAPIWithHook(camelField='base')
        user = api.to_ansible(_ctx())
        assert user.snake_field == 'base_hooked'


# ── Edge cases ──


class TestEdgeCases:
    """Edge cases: empty mapping, None context."""

    def test_no_mapping(self):
        @dataclass
        class NoMap(BaseTransformMixin):
            value: Optional[str] = None

            @classmethod
            def _get_api_class(cls):
                return cls

            @classmethod
            def _get_ansible_class(cls):
                return cls

        obj = NoMap(value='x')
        result = obj.to_api({})
        assert isinstance(result, NoMap)

    def test_none_context_uses_empty(self):
        user = FakeUser(snake_field='z')
        api = user.to_api(None)
        assert api.camelField == 'z'
