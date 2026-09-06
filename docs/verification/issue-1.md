# Issue #1: canonical GUI kernel and native bridge

The standalone package owns the kernel; the legacy module contains only
stateless typed C ABI forwarding calls. The runtime archive has no GUI owner.
The tests check 1,000 reclaim/reorder cycles, generation-safe ids, full hit
paths, clipping, dock/scroll geometry, and a real Metal render/present receipt.

The restored legacy gates also exposed and fixed ignored flow vertical spacing,
truncated 64-bit control identities, and PNG decoding errors. PNG regressions
cover all four supported color types and all five filters, split IDAT chunks,
unsigned samples, exact RGBA output capacity, truncated data and invalid filters.
The PNG decoder does not validate CRCs or support palette/interlaced images.

## Verification on 2026-09-06

With the adjacent core at `f597f612` plus its working tree, the explicit **host
compiler** override `PCC1="$PWD/.venv/bin/pcc"` passed these native-program gates
using the self backend and libpython off:

- `uv run pytest -q tests/test_pcc_gui_kit.py`: 4 passed.
- `uv run pytest -q -m integration tests/test_pcc_gui_kit_darwin.py`: real bridge
  render/present acknowledgement passed.
- `uv run pytest -q -m integration tests/test_pcc_gui_python.py`: all 8 original
  cases and the added 20-combination PNG matrix passed across focused runs.

The installed `~/.local/bin/pcc1` resolves to
`toolchains/v84-baseline-c1f4342696e9/bin/pcc1`. All the following also passed
through that native compiler after making address conversion explicit at the
compatibility-module/FFI boundary:

- `uv run pytest -q tests/test_pcc_gui_kit.py`: 4 passed.
- `uv run pytest -q tests/test_pcc_gui_current_pcc1.py::test_kernel_strict_self_no_libpython`: 1 passed.
- `uv run pytest -q -m integration tests/test_pcc_gui_kit_darwin.py`: 1 passed.
- All 9 integration cases in `tests/test_pcc_gui_python.py` passed across focused
  runs, including the 20-combination PNG matrix. Control identities are compared
  as 64-bit address words, with no C-string or managed-object conversion.

These results qualify the installed v84 compiler, not the later core 0.1.8
candidate. Native delegate/shutdown acceptance is tracked separately in #8.
