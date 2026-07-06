"""Import shim for the vendored SURD reference code (surd/VENDOR.md).

Usage:
    from vendorlib import surd_mod          # the vendored utils/surd.py module
    I_R, I_S, MI, leak = surd_mod.surd(hist)

Handles the two portability quirks found in Phase 0:
- utils/ is not a package: it must go on sys.path for `import surd` and the
  flat `import it_tools` inside it to resolve.
- surd.py imports pymp (fork-based, POSIX-only) at module level but only
  run_parallel() uses it; stub it so import works on Windows.
"""
from __future__ import annotations

import sys
import types
from pathlib import Path

VENDOR = Path(__file__).resolve().parent / "vendor" / "SURD" / "utils"
if not VENDOR.exists():
    raise ImportError(
        f"vendored SURD not found at {VENDOR} — restore it per surd/VENDOR.md")
sys.path.insert(0, str(VENDOR))

if "pymp" not in sys.modules:
    _pymp = types.ModuleType("pymp")
    _pymp.shared = types.SimpleNamespace(dict=dict)
    sys.modules["pymp"] = _pymp

import matplotlib

matplotlib.use("Agg")

import surd as surd_mod  # noqa: E402  (vendor)
import it_tools as it_tools_mod  # noqa: E402  (vendor)

__all__ = ["surd_mod", "it_tools_mod", "VENDOR"]
