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

## Setup

Install [uv](https://docs.astral.sh/uv/) and keep the compiler checkout next to
this one, as in `pcc-gateway`:

```bash
# from this checkout, if the compiler is not already present
git clone https://github.com/allstoalls/pcc ../pcc
```

Run all commands below from the `pcc-gui` checkout root:

```bash
uv sync --locked
command -v pcc1  # normally ~/.local/bin/pcc1, installed by the core checkout
export PCC_PACKAGE_SITE="$PWD"
pcc1 examples/closure_probe/probe.py -o examples/closure_probe/probe
./examples/closure_probe/probe
```

uv installs the pinned development Python and dependencies, including the
editable `../pcc` development tools. The native compiler has a separate stable
installation at `~/.local/bin/pcc1`; keep `~/.local/bin` on PATH. `uv sync` does
not build or install that executable. Applications compile through `pcc1` and
do not link libpython.
Native windows require macOS on Apple silicon and Xcode command line tools.

## Use it

Import the framework to include its implementation in your application:

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
pcc1 app.py -o app
./app
```

`pcc1` defaults to the self backend, libpython off and IR lowering on, so
ordinary commands do not repeat those options. Builds resolve `pcc1` through
PATH; set `PCC1=/absolute/path/to/pcc1` for an explicit build-script/test override.
This repository does not bootstrap a compiler or search core build directories.

The `PCC_PACKAGE_SITE` export above makes the framework available even to
example sources in subdirectories. Set it once per shell; it accepts a
colon-separated list when adding multiple packages.

## Examples

```bash
# headless diff viewer
pcc1 examples/mac_diff_app/declarative_headless.py -o examples/mac_diff_app/declarative_headless
./examples/mac_diff_app/declarative_headless examples/mac_diff_app/samples/left.txt examples/mac_diff_app/samples/right.txt

# windowed diff viewer; generates and builds the Metal bridge too
uv run examples/mac_diff_app/build.sh
./examples/mac_diff_app/mac_diff_app examples/mac_diff_app/samples/left.txt examples/mac_diff_app/samples/right.txt
```

Set `PCC1=/absolute/path/to/pcc1` when invoking `build.sh` to use a self-hosted
compiler. The Metal bridge is maintained in `pcc_gui/native/` and compiled
with the Xcode toolchain.
See [Harness](examples/harness/README.md) for the agent application's separate
build and current migration status.

## Tests

Tests run directly from this checkout; native tests reuse the adjacent core's
provenance-checked runtime archive fixture. Hardware integration tests are
excluded by default and can be selected explicitly with `-m integration`.

```bash
uv run pytest -q
uv run pytest -q tests/test_pcc_gui_kit.py
uv run pytest -q examples/harness/tests
uv run pytest -q -m integration tests/test_pcc_gui_kit_darwin.py
```

`tests/test_pcc_gui_current_pcc1.py` checks the installed self-hosted compiler.
A missing compiler produces an installation error; it never starts a core build.
The older `PCC_CURRENT_PCC1` test override is also accepted.
Open migration work and remaining acceptance gates are tracked in
[GitHub issues](https://github.com/allstoalls/pcc-gui/issues).

## Provenance

Extracted from `allstoalls/pcc` at commit `2574f585` (2026-09-06). The core no
longer ships these modules in its runtime archive; the framework modules carry
the `__pcc_runtime_port__ = True` directive because they build objects out of
raw memory exactly like the runtime ports they came from.
