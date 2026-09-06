# Issue #2: bounded keyed component commit

The tests now compile the standalone GUI package and inspect its actual ABI
exports instead of requiring a GUI implementation in the core archive. The
reorder fixture retains one immutable text address across renders, so it tests
stable descriptor reuse rather than assuming two separate C string literals
share an address. Frozen descriptor/effect arena sizes are literal byte counts,
so the fixture does not require the core's newer constant-expression lowering.
Diagnostic failures include the actual structural effects.

## Verification on 2026-09-06

- PASS: `PCC1="$PWD/.venv/bin/pcc" uv run pytest -q tests/test_pcc_gui_components.py`
  (2 tests). The native program covers deterministic insert/move/update/replace/
  remove effects, ownership, descriptor/effect/node capacity, rejected duplicate
  keys and failed callbacks, rollback, external removal and unmount.
- PASS with the installed v84 baseline:
  `uv run pytest -q tests/test_pcc_gui_current_pcc1.py::test_keyed_render_commit_strict_self_no_libpython`.
- PASS with the installed v84 baseline: `uv run pytest -q tests/test_pcc_gui_components.py`
  (2 tests), including the complete rollback/capacity/ownership fixture.
