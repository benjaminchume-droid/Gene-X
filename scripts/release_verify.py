"""Release verification helper for Gene X.

The release workflow remains the authoritative gate. This module provides a
local equivalent for the structural checks that can be run before publishing.
It intentionally contains no domain-specific knowledge or canned intelligence.
"""
from __future__ import annotations

import importlib
import pkgutil

import gene


def verify_import_graph() -> None:
    failures: list[str] = []
    for module in pkgutil.walk_packages(gene.__path__, gene.__name__ + "."):
        try:
            importlib.import_module(module.name)
        except Exception as exc:
            failures.append(f"{module.name}: {type(exc).__name__}: {exc}")
    if failures:
        raise RuntimeError("\n".join(failures))


def main() -> int:
    verify_import_graph()
    print(f"Gene X {gene.__version__}: import graph verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
