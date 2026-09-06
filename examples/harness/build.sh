#!/bin/sh
set -eu

PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
GUI_ROOT=$(CDPATH= cd -- "$PROJECT_DIR/../.." && pwd)
export PCC_PACKAGE_SITE="$GUI_ROOT${PCC_PACKAGE_SITE:+:$PCC_PACKAGE_SITE}"
OUTPUT_DIR=$PROJECT_DIR/build
OUTPUT=$OUTPUT_DIR/harness-core
BRIDGE_SOURCE=$GUI_ROOT/pcc_gui/native/pcc_gui_metal_render_bridge.m
BRIDGE=$OUTPUT_DIR/libpcc_gui_metal.dylib

PCC1_BIN=$(command -v "${PCC1:-pcc1}") || {
    echo "pcc1 not found; install the core compiler on PATH or set PCC1" >&2
    exit 1
}
case "$PCC1_BIN" in
    /*) ;;
    *) PCC1_BIN=$PWD/$PCC1_BIN ;;
esac

mkdir -p "$OUTPUT_DIR"

if [ ! -f "$BRIDGE" ] || [ "$BRIDGE_SOURCE" -nt "$BRIDGE" ]; then
    xcrun --sdk macosx clang -fobjc-arc \
        -framework Foundation \
        -framework Metal \
        -framework AppKit \
        -framework QuartzCore \
        -dynamiclib "$BRIDGE_SOURCE" \
        -o "$BRIDGE"
fi

cd "$GUI_ROOT"
"$PCC1_BIN" --backend self --python-libpython off --ir-scaffold on \
    "$PROJECT_DIR/app.py" -o "$OUTPUT"

echo "built: $OUTPUT"
echo "compiler: $PCC1_BIN"
echo "gui bridge: $BRIDGE"
