"""Verification primitives for code changes."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .analysis import Diagnostic

@dataclass(frozen=True)
class VerificationReport:
    passed: bool
    diagnostics: tuple[Diagnostic, ...] = ()
    checks: tuple[str, ...] = ()

class Verifier:
    def verify_diagnostics(self, diagnostics: Iterable[Diagnostic], *, checks: Iterable[str] = ()) -> VerificationReport:
        diagnostics = tuple(diagnostics)
        return VerificationReport(not any(d.severity == "error" for d in diagnostics), diagnostics, tuple(checks))

    def verify_tests(self, results: Iterable[object], *, checks: Iterable[str] = ()) -> VerificationReport:
        results = tuple(results)
        passed = all(bool(getattr(item, "passed", False)) for item in results)
        return VerificationReport(passed, checks=tuple(checks))
