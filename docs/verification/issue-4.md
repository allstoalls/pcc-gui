# Issue #4: event targets and component lifecycle

Native probes now set the root viewport before dispatching pointer events;
a zero-sized root cannot contain the painted target. The probes link the
standalone package, preserve frozen literal arena sizes and find compiler ABI
support in the editable core dependency.

## Verification on 2026-09-06

`uv run pytest -q tests/test_pcc_gui_events.py tests/test_pcc_gui_current_pcc1.py::test_event_lifecycle_strict_self_no_libpython`
passed all 3 tests through the installed pcc1 self backend with libpython off.
The component suite also passed through that compiler (see issue-2.md).

The full fixture verifies the topmost target, parent bubbling, exactly one
queued state update and affected-component render, ordered layout/passive
cleanup and creation, keyed removal/remount, listener removal, stale focus and
hover cleanup, and child-before-parent unmount. These are deterministic event
and lifecycle results, not a pixel-parity claim.
