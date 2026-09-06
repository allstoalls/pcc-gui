#!/bin/bash
# Build mac_diff_app with pcc1: Metal render bridge dylib + pcc1-compiled app.
# Self backend, no libpython.  The pcc_gui framework is compiled into the app
# through `import pcc_gui`; PCC_PACKAGE_SITE tells pcc1 where the package lives.
set -e
cd "$(dirname "$0")"
APP_DIR="$(pwd)"
GUI_ROOT="$(cd ../.. && pwd)"

PCC1="${PCC1:-}"
if [ -z "$PCC1" ] || [ ! -x "$PCC1" ]; then
  echo "set PCC1=/path/to/pcc1 (a stage-1 compiler built from https://github.com/allstoalls/pcc)" >&2
  exit 1
fi

echo "[1/2] Metal render bridge (Objective-C, compiled by clang)"
if [ ! -f pcc_gui_metal_render_bridge.m ]; then
  echo "pcc_gui_metal_render_bridge.m is missing; generate it once from the core:" >&2
  echo "  python -c \"from pcc.kernel_ir.metal_render_surface import write_metal_render_bridge; write_metal_render_bridge('.')\"" >&2
  exit 1
fi
clang -fobjc-arc -framework Foundation -framework Metal -framework AppKit \
      -framework QuartzCore -dynamiclib pcc_gui_metal_render_bridge.m \
      -o libpcc_gui_metal.dylib

echo "[2/2] compile the app with pcc1"
PCC_PACKAGE_SITE="$GUI_ROOT${PCC_PACKAGE_SITE:+:$PCC_PACKAGE_SITE}" \
  "$PCC1" --backend self --python-libpython off --ir-scaffold on \
          "$APP_DIR/app.py" -o "$APP_DIR/mac_diff_app"

echo "built: $APP_DIR/mac_diff_app"
