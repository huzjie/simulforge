# -*- coding: utf-8 -*-
"""A minimal YAML subset parser (no external dependency).

Supports nested maps, inline lists ``[a, b]``, block lists::

    key:
      - item
      - name: value

and inline comments (`` # comment``). Good enough for config files and recipes,
and it keeps the managed Python runtime fully self-contained.
"""


def _strip_comment(line):
    for i in range(len(line)):
        if line[i] == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i].rstrip()
    return line.rstrip()


def _scalar(v):
    if v == "true":
        return True
    if v == "false":
        return False
    if v == "null" or v == "~" or v == "":
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        pass
    try:
        return float(v)
    except (ValueError, TypeError):
        pass
    return v


def _inline_list(s):
    inner = s[1:-1].strip()
    if not inner:
        return []
    return [_scalar(x.strip()) for x in inner.split(",")]


def _add_list_item(lst, item):
    if ":" in item and not item.startswith("{"):
        k, v = item.split(":", 1)
        lst.append({k.strip(): _scalar(v.strip())})
    else:
        lst.append(_scalar(item))


def parse(text):
    root = {}
    stack = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" \t"))
        line = _strip_comment(raw.strip())
        if not line:
            continue
        if line.startswith("- "):
            item = line[2:].strip()
            while stack and stack[-1][0] >= indent:
                stack.pop()
            if not stack:
                continue
            top = stack[-1]
            container = top[1]
            if isinstance(container, dict):
                parent, key = top[2], top[3]
                lst = []
                if parent is not None and key is not None:
                    parent[key] = lst
                stack[-1] = (top[0], lst, parent, key)
                _add_list_item(lst, item)
            else:
                _add_list_item(container, item)
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1] if stack else root
        if value == "":
            placeholder = {}
            if isinstance(parent, list):
                parent.append(placeholder)
                stack.append((indent, placeholder, None, None))
            else:
                parent[key] = placeholder
                stack.append((indent, placeholder, parent, key))
        elif value.startswith("[") and value.endswith("]"):
            parent[key] = _inline_list(value)
        else:
            parent[key] = _scalar(value)
    return root
