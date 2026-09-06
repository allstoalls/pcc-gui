# pcc-gui

A declarative desktop GUI framework written in pcc-Python and compiled to native
code by [pcc](https://github.com/allstoalls/pcc): a retained element/control
tree, a Tailwind-like bounded style grammar, layout, theme animation,
CoreGraphics/Metal drawing and an AppKit window bridge, with no libpython at run
time.

It is an ordinary pcc package. An application does `import pcc_gui`, and
`pcc1` compiles the framework into the program together with the application
code. Nothing is prebuilt and nothing is linked from outside the compiler.

## Layout

- `pcc_gui/` – the framework package (17 modules: `pcc_gui_kit`,
  `pcc_gui_layout`, `pcc_gui_style`, `pcc_gui_theme_anim`, `pcc_gui_cg`,
  `pcc_gui_window`, `pcc_gui_app`, ...). `import pcc_gui` imports all of them.
  Applications call the framework through its C ABI (`pcc_kit_*`,
  `pcc_gui_*`) declared with `pcc.extern`.
- `examples/closure_probe/probe.py` – the smallest complete program.
- `examples/mac_diff_app/` – a Beyond-Compare-style diff viewer (Metal render
  bridge, declarative and headless variants).
- `examples/harness/` – the agent harness application: GUI front end plus its
  runtime modules and tests.
- `tests/` – framework unit tests and pcc1 canaries.
- `docs/gui-declarative-absorption.md` – design note.

## Requirements

- macOS on Apple silicon (the window bridge uses AppKit/CoreGraphics/Metal).
- A `pcc1` built from https://github.com/allstoalls/pcc
  (`scripts/bootstrap.sh --stage 1 --backend self`, or the stage-1 build
  receipt tools). The framework modules only import `pcc.extern` and
  `pcc.unsafe`, the compiler's own intrinsic surface.

## Use it

Tell `pcc1` where the package lives and compile your program. `PCC_PACKAGE_SITE`
is pcc's package-site list (colon separated); the package can also be copied
into pcc's default site, `~/.local/share/pcc/environments/<tag>/site-packages`,
after which no variable is needed.

```python
# app.py
from pcc.extern import c_int32, c_int64, extern

import pcc_gui  # pcc1 compiles the framework into this program

_kit_init = extern("pcc_kit_init", (c_int64,), c_int32)
_kit_create = extern("pcc_kit_create", (c_int64,), c_int64)
_live_nodes = extern("pcc_kit_live_nodes", (), c_int64)

_kit_init(64)
root = _kit_create(-1)
print("nodes", _live_nodes())
```

```bash
PCC_PACKAGE_SITE=/path/to/pcc-gui \
  pcc1 --backend self --python-libpython off --ir-scaffold on app.py -o app
./app
```

Verified on 2026-09-06 with a pcc1 built from the core at `2574f585` plus its
current working tree: `examples/closure_probe/probe.py` prints
`live nodes 2 root 0 child 1`, and `examples/mac_diff_app/declarative_headless.py`
compiles and runs, both from directories outside this repository with the core
runtime archive containing no GUI code.

## Examples

```bash
# headless diff viewer (no Metal window)
cd examples/mac_diff_app
PCC_PACKAGE_SITE=$PWD/../.. pcc1 --backend self --python-libpython off \
    --ir-scaffold on declarative_headless.py -o declarative_headless
./declarative_headless samples/left.txt samples/right.txt

# windowed diff viewer: Metal render bridge + app
PCC1=/path/to/pcc1 ./build.sh
./mac_diff_app samples/left.txt samples/right.txt

# harness application
PCC1=/path/to/pcc1 ../harness/build.sh
```

The Metal render bridge (`pcc_gui_metal_render_bridge.m`) is Objective-C
generated once from the core's `pcc.kernel_ir.metal_render_surface` and compiled
with clang; it is the only non-pcc build step and only the windowed example
needs it.

## Tests

The tests still use the core's pytest fixtures (`pcc_py_runtime_archive`,
`pcc1_gate`); run them from a core checkout with this repository as the package
site:

```bash
cd /path/to/pcc && PCC_PACKAGE_SITE=/path/to/pcc-gui gtimeout 900s env -u LC_ALL \
    uv run pytest -q -x /path/to/pcc-gui/tests/test_pcc_gui_style.py
```

## Provenance

Extracted from `allstoalls/pcc` at commit `2574f585` (2026-09-06). The core no
longer ships these modules in its runtime archive; the framework modules carry
the `__pcc_runtime_port__ = True` directive because they build objects out of
raw memory exactly like the runtime ports they came from.
