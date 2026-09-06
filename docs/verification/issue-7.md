# Issue #7: typed state and command resolution

Command gates now resolve the standalone owners and frozen ABI contract from
this package, while checking compiler intrinsics in the editable core. The
static-intrinsic guard rejects an empty source inventory instead of passing
when pointed at a missing pre-extraction directory. Native probes explicitly
link the framework and resolve installed pcc1 through PATH.

## Verification on 2026-09-06

`uv run pytest -q tests/test_pcc_gui_commands.py tests/test_pcc_gui_current_pcc1.py::test_command_state_boundary_strict_self_no_libpython`
passed all 5 tests through installed pcc1, self backend and libpython off.
The fixture covers typed scalar/handle state, managed binding propagation,
allowed/denied targets, payload errors, synchronous and asynchronous results,
structured errors, duplicate and late resolution, bounded resolver capacity,
cancellation and teardown. Event ownership acceptance is recorded in issue-4.md.
