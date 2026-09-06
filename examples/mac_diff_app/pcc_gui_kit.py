"""Compatibility calls into the single canonical GUI kernel.

This module contains no tree implementation or retained state. The framework
is linked by importing pcc_gui; these functions forward to its public C ABI.
Unsafe addresses use the integer address type at application-module boundaries.
"""

import pcc_gui  # noqa: F401: compile the canonical kernel into this application
from pcc.extern import c_int32, c_int64, c_ptr, c_void, extern
from pcc.unsafe import int_to_ptr

_abi_pcc_kit_init = extern("pcc_kit_init", (c_int64,), c_int32)


def pcc_kit_init(cap: int) -> int:
    return _abi_pcc_kit_init(cap)


_abi_pcc_kit_is_valid = extern("pcc_kit_is_valid", (c_int64,), c_int32)


def pcc_kit_is_valid(node_id: int) -> int:
    return _abi_pcc_kit_is_valid(node_id)


_abi_pcc_kit_live_nodes = extern("pcc_kit_live_nodes", (), c_int64)


def pcc_kit_live_nodes() -> int:
    return _abi_pcc_kit_live_nodes()


_abi_pcc_kit_create = extern("pcc_kit_create", (c_int64,), c_int64)


def pcc_kit_create(parent: int) -> int:
    return _abi_pcc_kit_create(parent)


_abi_pcc_kit_detach = extern("pcc_kit_detach", (c_int64,), c_int32)


def pcc_kit_detach(node_id: int) -> int:
    return _abi_pcc_kit_detach(node_id)


_abi_pcc_kit_append_child = extern("pcc_kit_append_child", (c_int64, c_int64), c_int32)


def pcc_kit_append_child(parent: int, child: int) -> int:
    return _abi_pcc_kit_append_child(parent, child)


_abi_pcc_kit_insert_before = extern(
    "pcc_kit_insert_before", (c_int64, c_int64, c_int64), c_int32
)


def pcc_kit_insert_before(parent: int, child: int, before: int) -> int:
    return _abi_pcc_kit_insert_before(parent, child, before)


_abi_pcc_kit_reorder = extern("pcc_kit_reorder", (c_int64, c_int64, c_int64), c_int32)


def pcc_kit_reorder(parent: int, child: int, before: int) -> int:
    return _abi_pcc_kit_reorder(parent, child, before)


_abi_pcc_kit_destroy_subtree = extern("pcc_kit_destroy_subtree", (c_int64,), c_int64)


def pcc_kit_destroy_subtree(node_id: int) -> int:
    return _abi_pcc_kit_destroy_subtree(node_id)


_abi_pcc_kit_set_removal_hook = extern("pcc_kit_set_removal_hook", (c_ptr,), c_void)


def pcc_kit_set_removal_hook(hook: int) -> None:
    _abi_pcc_kit_set_removal_hook(int_to_ptr(hook))


_abi_pcc_kit_rect = extern(
    "pcc_kit_rect", (c_int64, c_int64, c_int64, c_int64, c_int64, c_int32), c_void
)


def pcc_kit_rect(node_id: int, x: int, y: int, w: int, h: int, color: int) -> None:
    _abi_pcc_kit_rect(node_id, x, y, w, h, color)


_abi_pcc_kit_text = extern(
    "pcc_kit_text",
    (c_int64, c_int64, c_int64, c_ptr, c_int64, c_int64, c_int32),
    c_void,
)


def pcc_kit_text(
    node_id: int, x: int, y: int, text_ptr: int, tlen: int, font: int, color: int
) -> None:
    _abi_pcc_kit_text(node_id, x, y, int_to_ptr(text_ptr), tlen, font, color)


_abi_pcc_kit_visible = extern("pcc_kit_visible", (c_int64, c_int32), c_void)


def pcc_kit_visible(node_id: int, value: int) -> None:
    _abi_pcc_kit_visible(node_id, value)


_abi_pcc_kit_layout = extern("pcc_kit_layout", (c_int64, c_int32), c_void)


def pcc_kit_layout(node_id: int, layout: int) -> None:
    _abi_pcc_kit_layout(node_id, layout)


_abi_pcc_kit_dock = extern("pcc_kit_dock", (c_int64, c_int32), c_void)


def pcc_kit_dock(node_id: int, side: int) -> None:
    _abi_pcc_kit_dock(node_id, side)


_abi_pcc_kit_padding = extern(
    "pcc_kit_padding", (c_int64, c_int64, c_int64, c_int64, c_int64), c_void
)


def pcc_kit_padding(node_id: int, left: int, top: int, right: int, bottom: int) -> None:
    _abi_pcc_kit_padding(node_id, left, top, right, bottom)


_abi_pcc_kit_gap = extern("pcc_kit_gap", (c_int64, c_int64), c_void)


def pcc_kit_gap(node_id: int, gap: int) -> None:
    _abi_pcc_kit_gap(node_id, gap)


_abi_pcc_kit_clip_children = extern("pcc_kit_clip_children", (c_int64, c_int32), c_void)


def pcc_kit_clip_children(node_id: int, on: int) -> None:
    _abi_pcc_kit_clip_children(node_id, on)


_abi_pcc_kit_scroll_container = extern(
    "pcc_kit_scroll_container", (c_int64, c_int32), c_void
)


def pcc_kit_scroll_container(node_id: int, on: int) -> None:
    _abi_pcc_kit_scroll_container(node_id, on)


_abi_pcc_kit_scroll_max = extern("pcc_kit_scroll_max", (c_int64,), c_int64)


def pcc_kit_scroll_max(node_id: int) -> int:
    return _abi_pcc_kit_scroll_max(node_id)


_abi_pcc_kit_scroll = extern("pcc_kit_scroll", (c_int64, c_int64), c_int64)


def pcc_kit_scroll(node_id: int, offset: int) -> int:
    return _abi_pcc_kit_scroll(node_id, offset)


_abi_pcc_kit_scroll_by = extern("pcc_kit_scroll_by", (c_int64, c_int64), c_int64)


def pcc_kit_scroll_by(node_id: int, delta: int) -> int:
    return _abi_pcc_kit_scroll_by(node_id, delta)


_abi_pcc_kit_layout_tree = extern(
    "pcc_kit_layout_tree", (c_int64, c_int64, c_int64), c_void
)


def pcc_kit_layout_tree(node_id: int, w: int, h: int) -> None:
    _abi_pcc_kit_layout_tree(node_id, w, h)


_abi_pcc_kit_handler = extern("pcc_kit_handler", (c_int64, c_int32), c_void)


def pcc_kit_handler(node_id: int, on: int) -> None:
    _abi_pcc_kit_handler(node_id, on)


_abi_pcc_kit_key_handler = extern("pcc_kit_key_handler", (c_int64, c_int32), c_void)


def pcc_kit_key_handler(node_id: int, on: int) -> None:
    _abi_pcc_kit_key_handler(node_id, on)


_abi_pcc_kit_focus = extern("pcc_kit_focus", (c_int64,), c_void)


def pcc_kit_focus(node_id: int) -> None:
    _abi_pcc_kit_focus(node_id)


_abi_pcc_kit_focused = extern("pcc_kit_focused", (c_int64,), c_int32)


def pcc_kit_focused(node_id: int) -> int:
    return _abi_pcc_kit_focused(node_id)


_abi_pcc_kit_key_event = extern("pcc_kit_key_event", (c_int64, c_int64), c_int64)


def pcc_kit_key_event(key: int, etype: int) -> int:
    return _abi_pcc_kit_key_event(key, etype)


_abi_pcc_kit_wrap = extern("pcc_kit_wrap", (c_int64, c_int32), c_void)


def pcc_kit_wrap(node_id: int, on: int) -> None:
    _abi_pcc_kit_wrap(node_id, on)


_abi_pcc_kit_lerp = extern("pcc_kit_lerp", (c_int64, c_int64, c_int64), c_int64)


def pcc_kit_lerp(a: int, b: int, t: int) -> int:
    return _abi_pcc_kit_lerp(a, b, t)


_abi_pcc_kit_hit = extern("pcc_kit_hit", (c_int64, c_int64, c_int64), c_int64)


def pcc_kit_hit(node_id: int, x: int, y: int) -> int:
    return _abi_pcc_kit_hit(node_id, x, y)


_abi_pcc_kit_hit_path_v1 = extern(
    "pcc_kit_hit_path_v1", (c_int64, c_int64, c_int64, c_ptr, c_int64), c_int64
)


def pcc_kit_hit_path_v1(root: int, x: int, y: int, path_out: int, capacity: int) -> int:
    return _abi_pcc_kit_hit_path_v1(root, x, y, int_to_ptr(path_out), capacity)


_abi_pcc_kit_route_event_v2 = extern(
    "pcc_kit_route_event_v2",
    (c_int64, c_int64, c_int64, c_int64, c_ptr, c_int64),
    c_int64,
)


def pcc_kit_route_event_v2(
    root: int, x: int, y: int, etype: int, path_out: int, capacity: int
) -> int:
    return _abi_pcc_kit_route_event_v2(root, x, y, etype, int_to_ptr(path_out), capacity)


_abi_pcc_kit_route_event = extern(
    "pcc_kit_route_event", (c_int64, c_int64, c_int64, c_int64), c_int64
)


def pcc_kit_route_event(root: int, x: int, y: int, etype: int) -> int:
    return _abi_pcc_kit_route_event(root, x, y, etype)


_abi_pcc_kit_hover = extern(
    "pcc_kit_hover", (c_int64, c_int64, c_int64, c_int32), c_int64
)


def pcc_kit_hover(root: int, x: int, y: int, on: int) -> int:
    return _abi_pcc_kit_hover(root, x, y, on)


_abi_pcc_kit_hovered = extern("pcc_kit_hovered", (c_int64,), c_int32)


def pcc_kit_hovered(node_id: int) -> int:
    return _abi_pcc_kit_hovered(node_id)


_abi_pcc_kit_render = extern(
    "pcc_kit_render", (c_int64, c_ptr, c_ptr, c_ptr, c_ptr, c_ptr), c_void
)


def pcc_kit_render(
    node_id: int, rects: int, colors: int, rn_out: int, texts: int, tn_out: int
) -> None:
    _abi_pcc_kit_render(node_id, int_to_ptr(rects), int_to_ptr(colors), int_to_ptr(rn_out), int_to_ptr(texts), int_to_ptr(tn_out))


_abi_pcc_kit_geometry_get = extern("pcc_kit_geometry_get", (c_int64, c_int64), c_int64)

_abi_pcc_kit_geometry_set = extern(
    "pcc_kit_geometry_set", (c_int64, c_int64, c_int64), c_void
)


def _n8(node_id: int, offset: int) -> int:
    return _abi_pcc_kit_geometry_get(node_id, offset)


def _s8(node_id: int, offset: int, value: int) -> None:
    _abi_pcc_kit_geometry_set(node_id, offset, value)
