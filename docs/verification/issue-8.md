# Issue #8: native application lifecycle

The framework owns its Metal/AppKit source at
`pcc_gui/native/pcc_gui_metal_render_bridge.m`. Both example builds and native
tests consume that same file, without generating GUI code from the compiler
repository. Compiler/runtime implementation remains in core.

The window handle transfers one retained NSWindow reference to the caller.
Creation sets `releasedWhenClosed=NO`, so the explicit bridge close releases
that retain once. Previously AppKit's automatic close release and the bridge's
CFRelease caused an autorelease-pool crash. A native Objective-C oracle isolates
this defect from PCC and checks three close cycles with zero retained windows.

## Verified on 2026-09-07

- Default PATH pcc1, with no compiler override:
  `uv run pytest -vv -x -m integration tests/test_pcc_gui_app_lifecycle_darwin.py tests/test_pcc_gui_kit_darwin.py`
  passed all 3 native tests (132.95 seconds).
- The native delegate test proves Window/Opened/Reopen payload delivery and
  terminal Exit; the ownership oracle proves one window release; the kernel
  bridge gate proves a real render/present acknowledgement.
- `uv run pytest -vv -x examples/harness/tests tests/test_harness_gui.py`:
  62 passed, 1 native Harness test deselected. Harness builds now also use the
  installed pcc1 on PATH, the correct standalone app path and this native source.
- The prior frozen GUI layer run passed all 29 cases, including the app event,
  cancellation and teardown state machine and installed-pcc1 lifecycle canary.

Native Objective-C builds use the Xcode-selected Apple toolchain via xcrun.
The old proposal to modify core's generator is superseded by framework
ownership; no compiler source or installed compiler was changed for this fix.
This closes lifecycle/ownership acceptance, not pixel parity or Harness feature
parity. Full Harness product acceptance remains tracked by its own issues.
