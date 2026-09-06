# pcc-gui

pcc GUI framework (pcc_gui runtime ports, mac_diff_app showcase, GUI harness and tests) extracted from the pcc compiler core

Seeded from `allstoalls/pcc` at commit `2574f585` (2026-09-06).

Layout:

- `pcc/py_runtime/py/pcc_gui_*.py` and `pcc/py_runtime/gui_declarative_contract_v1.json`: the GUI
  framework itself (currently runtime ports compiled into the pcc runtime archive; same relative
  path as in the core so the core can drop them without renames).
- `examples/mac_diff_app/`: the Beyond-Compare-style diff viewer built on pcc_gui.
- `examples/harness/`: the agent harness application (GUI front end plus its runtime modules and tests).
- `tests/`: the GUI unit and pcc1 canary tests moved out of the core test tree.
- `docs/design/gui-declarative-absorption.md`: the design note.

The core repository's `projects/mac_diff_app` and `projects/harness` are the same examples; they move
here under `examples/`. The code still depends on
the pcc compiler and runtime (`pcc/py_runtime`, `pcc.unsafe`, `pcc.extern`);
build and test it against an installed pcc from the core repository.

Files copied (see `SEED_FILES.txt`): 55 tracked paths.

Status: seed copy only. The core repository keeps the originals until the
extraction task on its task board (docs/goal/task-board.yaml) removes them
behind the bootstrap and runtime-archive gates.
