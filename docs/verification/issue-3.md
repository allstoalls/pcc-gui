# Issue #3: queued state and priority lanes

The scheduler gate now links the standalone package and locates compiler ABI
support in the editable core dependency. The installed compiler is resolved
through PATH, with no automatic bootstrap or private build-directory search.

## Verification on 2026-09-06

- PASS: `uv run pytest -q tests/test_pcc_gui_scheduler.py` (2 tests).
- PASS: `uv run pytest -q tests/test_pcc_gui_current_pcc1.py::test_state_lane_scheduler_strict_self_no_libpython`.
- PASS: the same full scheduler suite with the current core host compiler via
  `PCC1="$PWD/.venv/bin/pcc"` (2 tests).

The native fixture exercises enqueue ordering, SET/reducer replay, lane aging,
yield/resume and high-priority restart, rejected impure/reentrant reducers,
callback failure, cancellation, overflow and exact handle ownership. The
installed native compiler is the v84 baseline; the core's later 0.1.8 candidate
is not represented by these results. Component acceptance is recorded in
[issue-2.md](issue-2.md).
