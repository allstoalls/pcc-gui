# Issue #6: bounded style candidate compiler

Numeric slash modifiers now scale and round the token before applying the
negative prefix. For token 13, both `x-3/[dense]` and `-x-3/[dense]` therefore
have magnitude 6; previously the negative form rounded -6.5 down to -7.
Compilation and cached-operation validation share the same value function.

## Verification on 2026-09-06

`uv run pytest -q tests/test_pcc_gui_style_compiler.py tests/test_pcc_gui_current_pcc1.py::test_style_candidate_compiler_strict_self_no_libpython`
passed all 3 tests through installed pcc1, self backend and libpython off.
The full fixture covers source order, duplicate/unknown/ambiguous candidates,
negative prefixes, named/arbitrary modifiers, immutable operation values,
selective token/schema invalidation, direct/class dependency overlap, and zero
parser calls or allocations on valid warm application. The style dependency
suite also passed (issue-5.md).
