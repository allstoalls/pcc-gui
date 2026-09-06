# Shared compiler entry and framework-owned native bridge

- Schema: pcc.harness.migration.v1
- Sequence: 0002
- PCC change: pending:shared-compiler-framework-bridge
- Upstream range: not-applicable
- Native-only rationale: Route standalone native builds through the shared installed compiler and the canonical GUI framework bridge.
- Changed domains: pcc/gui, pcc/toolchain, examples/harness/build
- Tasks: HARNESS-P0-CURRENT-PCC1, HARNESS-P0-NATIVE-GUI-SHELL
- GUI impact: changed

## Behavior migrated

- Build the actual standalone app source, use pcc1 from PATH or explicit PCC1, and never select an unrelated private bootstrap binary.
- Compile the framework-owned Metal/AppKit source and rebuild when application, framework or bridge sources change.

## PCC facilities

- The installed compiler and runtime remain core-owned; GUI bridge lifetime is now maintained by pcc-gui.

## Verification

- PASS | uv run pytest -vv -x examples/harness/tests tests/test_harness_gui.py | 62 passed; the native Harness case was deselected.
- NOT-RUN | uv run pytest -m integration tests/test_harness_gui.py | Full native Harness acceptance remains part of the open native-shell task.

## GUI evidence

- PASS | GUI-P2-APP-RUN-LIFECYCLE | Three native lifecycle, ownership and render tests passed through the canonical framework bridge and default PATH pcc1.

## Remaining boundaries

- Full Harness native compilation, viewport/input/session parity and migration-ledger validation still have their own open boundaries; the legacy validator targets the retired monorepo layout.
