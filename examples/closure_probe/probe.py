from pcc.extern import c_int32, c_int64, extern

import pcc_gui  # noqa: F401  (the whole framework rides into the closure)

_kit_init = extern("pcc_kit_init", (c_int64,), c_int32)
_live_nodes = extern("pcc_kit_live_nodes", (), c_int64)
_kit_create = extern("pcc_kit_create", (c_int64,), c_int64)


def main() -> int:
    if _kit_init(64) != 0:
        return 1
    root = _kit_create(-1)
    child = _kit_create(root)
    print("live nodes", _live_nodes(), "root", root, "child", child)
    return 0


print("rc", main())
