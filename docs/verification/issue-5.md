# Issue #5: canonical theme tokens and selective invalidation

Packed ARGB colors now read back as unsigned 32-bit values from the kernel's
64-bit style getter. Previously an opaque color such as `0xFF123456` was sign
extended and disagreed with the canonical theme value.

The standalone fixture now refreshes every changed dependency after a theme
swap, including the negative spacing operation. It first verifies that the
component stays dirty and rejects commit while that dependency remains stale.

## Verification on 2026-09-06

`uv run pytest -q tests/test_pcc_gui_style.py tests/test_pcc_gui_current_pcc1.py::test_style_token_utilities_strict_self_no_libpython`
passed all 3 tests with installed pcc1, self backend and libpython off.
Coverage includes exact token/namespace dependencies, selective theme swaps,
immutable stale-operation rejection, unsigned ARGB round-trip, font/size values,
padding/gap geometry and unmount cleanup. Kernel acceptance is recorded in
issue-1.md.
