# pcc-gui

A declarative desktop GUI framework written in pcc-Python and compiled to native
code by the [pcc](https://github.com/allstoalls/pcc) compiler: a retained
element/control tree, a Tailwind-like bounded style grammar, layout, theme
animation, CoreGraphics/Metal drawing and an AppKit window bridge, with no
libpython at run time.

It started life inside the compiler repository as a flagship showcase for the
no-libpython runtime; this repository is its standalone home. Extracted from
`allstoalls/pcc` at commit `2574f585` (2026-09-06).

## Layout

- `pcc_gui/` – the framework: 17 pcc-Python modules (`pcc_gui_kit`,
  `pcc_gui_layout`, `pcc_gui_style`, `pcc_gui_theme_anim`, `pcc_gui_cg`,
  `pcc_gui_window`, `pcc_gui_app`, ...) plus `gui_declarative_contract_v1.json`.
  They export a C ABI (`pcc_kit_*`, `pcc_gui_*` symbols) that applications call
  through `pcc.extern` declarations.
- `examples/mac_diff_app/` – a Beyond-Compare-style diff viewer (Metal render
  bridge, declarative and headless variants).
- `examples/harness/` – the agent harness application: GUI front end
  (`gui_app.py`, `gui_bridge.py`, `gui_model.py`) plus its runtime modules and
  tests.
- `tests/` – unit tests and pcc1 canaries for the framework.
- `docs/gui-declarative-absorption.md` – design note.
- `Makefile` – builds `build/libpcc_gui.a` from `pcc_gui/`.

## Requirements

- macOS on Apple silicon (the window bridge uses AppKit/CoreGraphics/Metal).
- A checkout of the compiler core, `allstoalls/pcc`, next to this repository
  (`../pcc`), with its environment synced:

  ```bash
  git clone https://github.com/allstoalls/pcc ../pcc
  (cd ../pcc && uv sync)
  ```

  The framework modules import only `pcc.extern` and `pcc.unsafe` (compiler
  intrinsics); they are ordinary pcc-Python sources.

## Build the framework library

```bash
make PCC=../pcc/.venv/bin/pcc PYTHON=../pcc/.venv/bin/python3 PCC_CORE=../pcc
# -> build/pcc_gui_*.o (17 objects) and build/libpcc_gui.a
```

Each module is compiled the same way the core builds its runtime archive:
`pcc --backend self --python-libpython=off --ir-scaffold=on --python-library
--emit-llvm` emits the module IR, then `python -m pcc.tools.ir_to_obj` turns it
into a native object. `PCC` may also point at a bootstrapped native `pcc1`.

Verified on 2026-09-06 with the core at `2574f585` plus its current working
tree: 17 objects, 227 exported `pcc_*` symbols.

## Link an application against it

Two link paths exist today; they are mode-labelled on purpose.

1. **Through the core runtime archive (current default).** The core's
   `pcc/py_runtime/Makefile` still compiles these same modules into
   `libpy_runtime_pcc_py.a`, so any program compiled by the core's `pcc`/`pcc1`
   with `--backend self --python-libpython=off` already links the GUI symbols.
   This is how both examples build today.
2. **Standalone archive via the host linker.** pcc's own self-link path does not
   accept extra link inputs yet (`pcc self-link mode does not support link
   arguments`), so the standalone archive is linked through the system linker:

   ```bash
   ../pcc/.venv/bin/pcc --backend llvm --system-link \
       --python-libpython=off --ir-scaffold=on \
       --link-arg "$PWD/build/libpcc_gui.a" app.py -o app
   ```

   Verified with a probe that calls `pcc_kit_live_nodes()` through
   `extern("pcc_kit_live_nodes", (), c_int64)`.

Making the self-link path accept `libpcc_gui.a`, and removing the modules from
the core archive, is tracked in the core task board as
`REPO-P1-EXTRACT-PCC-GUI-REPO`.

## Build and run the examples

Both example build scripts locate the core through `PCC_CORE` (default
`../../../pcc` relative to the example) and the stage-1 compiler through `PCC1`.

```bash
# mac_diff_app: Metal render bridge dylib + pcc1-compiled app
PCC_CORE=$PWD/../pcc PCC1=$PWD/../pcc/build/bootstrap/pcc1 \
    examples/mac_diff_app/build.sh
examples/mac_diff_app/mac_diff_app examples/mac_diff_app/samples/left.txt \
    examples/mac_diff_app/samples/right.txt

# harness: bootstrap a current-source pcc1 first, then build the GUI app
PCC_CORE=$PWD/../pcc examples/harness/bootstrap-pcc1.sh
PCC_CORE=$PWD/../pcc examples/harness/build.sh
```

A `pcc1` is produced by the core's `scripts/bootstrap.sh --stage 1 --backend
self` (about 3-4 minutes); see the core README.

## Tests

The tests still use the core's pytest fixtures (`pcc_py_runtime_archive`,
`pcc1_gate`), so run them from the core checkout with this repository on the
path:

```bash
cd ../pcc && gtimeout 900s env -u LC_ALL uv run pytest -q -x \
    ../pcc-gui/tests/test_pcc_gui_style.py ../pcc-gui/tests/test_pcc_gui_kit.py
```

`tests/test_pcc_gui_current_pcc1.py` and the `*_darwin.py` tests need a built
`pcc1` and a display; they are gated with `pcc_gate` markers, not skips.

## Status and provenance

- The modules here are byte-identical to the core's `pcc/py_runtime/py/pcc_gui_*.py`
  as of the extraction (the `__pcc_runtime_port__ = True` directive marks them
  as pointer-lane runtime-style modules for the current frontend).
- `SEED_FILES.txt` lists every tracked path with its original location.
- Visibility: public, like the core.
