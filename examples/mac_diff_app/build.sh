#!/bin/bash
# Build mac_diff_app with pcc1 from PATH or an explicit PCC1 executable.
# Self backend, no libpython.  The pcc_gui framework is compiled into the app
# through `import pcc_gui`; PCC_PACKAGE_SITE tells pcc1 where the package lives.
set -e
cd "$(dirname "$0")"
APP_DIR="$(pwd)"
GUI_ROOT="$(cd ../.. && pwd)"

PCC1="${PCC1:-pcc1}"
if ! command -v "$PCC1" >/dev/null 2>&1; then
  echo "compiler not found: $PCC1; install ~/.local/bin/pcc1, add it to PATH, or set PCC1" >&2
  exit 1
fi

echo "[1/2] Metal render bridge (Objective-C, compiled by clang)"
python -c 'from pcc.kernel_ir.metal_render_surface import write_metal_render_bridge; write_metal_render_bridge(".")'
clang -fobjc-arc -framework Foundation -framework Metal -framework AppKit \
      -framework QuartzCore -dynamiclib pcc_gui_metal_render_bridge.m \
      -o libpcc_gui_metal.dylib

echo "[2/2] compile the app with $PCC1"
PCC_PACKAGE_SITE="$GUI_ROOT${PCC_PACKAGE_SITE:+:$PCC_PACKAGE_SITE}" \
  "$PCC1" --backend self "$APP_DIR/app.py" -o "$APP_DIR/mac_diff_app"

echo "built: $APP_DIR/mac_diff_app"
