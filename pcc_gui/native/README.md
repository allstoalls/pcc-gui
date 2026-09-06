# Native GUI bridge

`pcc_gui_metal_render_bridge.m` is the canonical Metal/AppKit bridge for
pcc-gui applications and tests. It was extracted from
`allstoalls/pcc@77cdf411`, `pcc/kernel_ir/metal_render_surface.py`, and is now
maintained here. Compiler intrinsics and the reusable PCC runtime remain in
core; GUI paint, window and event behavior belong to this framework.

The public window handle transfers one retained NSWindow reference to the
caller. Creation disables `releasedWhenClosed`; `pcc_gui_metal_window_close`
closes the window and releases that reference exactly once. Clients must not
reuse a closed handle. Native ownership and delegate integration are tested
with `tests/test_pcc_gui_app_lifecycle_darwin.py` through the default pcc1.

Both example build scripts compile this file with clang. There is no
build-time dependency on core's older GUI source generator. Python package
builds include this source asset alongside the pcc-Python framework.
