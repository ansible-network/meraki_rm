"""Root conftest — ensure plugins/ is on sys.path for all tests."""

import sys
from pathlib import Path

_plugins = str(Path(__file__).parent / "plugins")
if _plugins not in sys.path:
    sys.path.insert(0, _plugins)
