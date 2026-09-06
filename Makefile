# Build the pcc_gui library objects and archive with the pcc compiler.
#
#   make PCC=../pcc/.venv/bin/pcc PYTHON=../pcc/.venv/bin/python3
#
# PCC     : the pcc compiler entry point (host `pcc` from allstoalls/pcc, or a
#           bootstrapped native `pcc1`).
# PYTHON  : the interpreter that has the pcc package importable (used for the
#           IR -> object step, `python -m pcc.tools.ir_to_obj`).
# PCC_CORE: checkout of allstoalls/pcc; only needed so `pcc.extern`/`pcc.unsafe`
#           resolve when PCC is the host compiler.
PCC      ?= pcc
PYTHON   ?= python3
PCC_CORE ?= $(abspath ../pcc)
OUT      ?= build

SRC_DIR  := pcc_gui
MODULES  := $(sort $(patsubst $(SRC_DIR)/%.py,%,$(wildcard $(SRC_DIR)/pcc_gui_*.py)))
OBJS     := $(addprefix $(OUT)/,$(addsuffix .o,$(MODULES)))
ARCHIVE  := $(OUT)/libpcc_gui.a

.PHONY: all clean list
all: $(ARCHIVE)

list:
	@printf '%s\n' $(MODULES)

$(OUT):
	mkdir -p $(OUT)

# Same two-step rule as the core runtime archive: pcc emits the module IR in
# --python-library mode (closed-world, no libpython), then the pcc IR->object
# tool produces a native object.  (Provenance receipts are a runtime-archive
# concept and are not emitted for this standalone library.)
$(OUT)/%.o: $(SRC_DIR)/%.py | $(OUT)
	PYTHONPATH=$(PCC_CORE) $(PCC) --backend self --python-libpython=off --ir-scaffold=on --python-library --emit-llvm=$(OUT)/$*.ll $<
	PYTHONPATH=$(PCC_CORE) $(PYTHON) -m pcc.tools.ir_to_obj $(OUT)/$*.ll $@

$(ARCHIVE): $(OBJS)
	rm -f $@
	ar rcs $@ $(OBJS)

clean:
	rm -rf $(OUT)
