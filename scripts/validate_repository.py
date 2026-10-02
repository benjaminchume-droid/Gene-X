"""Static repository validation entry point."""
from __future__ import annotations
import ast
import sys
from pathlib import Path

def validate(root: Path) -> list[str]:
    errors = []
    for path in root.rglob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path}:{exc.lineno}:{exc.offset}: {exc.msg}")
    return errors

if __name__ == "__main__":
    errors = validate(Path(__file__).resolve().parents[1])
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("syntax validation passed")
