#!/usr/bin/env python3
# #Human
import glob
import os
import re
import subprocess
import sys
from collections import Counter

TAG_RE = re.compile(r"(?<!\w)#[A-Za-z][\w-]*")
LEXTOK_RE = re.compile(r'"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\'|\w+|==|!=|<=|>=|->|[{}()\[\];,]|[^\s]')


def fmt_size(size_bytes):
    return f"{size_bytes / 1024:.2f} KB"


def get_loc_lextokens(text):
    lines = [line for line in text.splitlines() if line.strip()]
    tokens = LEXTOK_RE.findall(text)
    return (len(lines), len(tokens))


def get_file_text_hashtag(path):
    try:
        with open(path, "rb") as file:
            chunk = file.read(4096)
        if b"\x00" in chunk:
            return (False, None)
        text = chunk.decode("utf-8", "ignore")
        match = TAG_RE.search(text)
        return (True, match.group(0) if match else None)
    except Exception:
        return (False, None)


def get_repo_root():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


def is_path_inside_repo(path, repo_root):
    if not repo_root:
        return False
    abs_path = os.path.abspath(path)
    try:
        common = os.path.commonpath([abs_path, repo_root])
    except ValueError:
        return False
    return common == repo_root


def is_git_ignored(path, repo_root):
    if not is_path_inside_repo(path, repo_root):
        return False
    try:
        relative_path = os.path.relpath(os.path.abspath(path), repo_root)
        result = subprocess.run(
            ["git", "-C", repo_root, "check-ignore", "-q", relative_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


def tag_order_map(found_tags):
    order = {}
    for index, tag in enumerate(found_tags):
        if tag not in order:
            order[tag] = index
    return order


def get_text_file_info(path, repo_root):
    if is_git_ignored(path, repo_root):
        return None

    is_text, first_tag = get_file_text_hashtag(path)
    if not is_text:
        return None

    try:
        size_bytes = os.path.getsize(path)
        if size_bytes >= 128 * 1024:
            return None

        with open(path, encoding="utf-8", errors="ignore") as file:
            text = file.read()

        found_tags = [tag.lower() for tag in TAG_RE.findall(text)]
        tags = Counter(found_tags)
        order = tag_order_map(found_tags)
        loc, ltok = get_loc_lextokens(text)
        return {
            "name": os.path.basename(path),
            "path": path,
            "size": size_bytes,
            "loc": loc,
            "ltok": ltok,
            "first": first_tag,
            "tags": tags,
            "order": order,
        }
    except Exception:
        return None


def new_dir_node(path):
    name = os.path.basename(path.rstrip(os.sep)) or "."
    return {
        "kind": "dir",
        "name": name,
        "path": path,
        "size": 0,
        "loc": 0,
        "ltok": 0,
        "dirs": [],
        "files": [],
        "totals": Counter(),
    }


def traverse_dir(path, repo_root):
    node = new_dir_node(path)
    for item_path in sorted(glob.glob(os.path.join(path, "*"))):
        if is_git_ignored(item_path, repo_root):
            continue
        if os.path.isdir(item_path):
            child_dir = traverse_dir(item_path, repo_root)
            node["dirs"].append(child_dir)
            node["size"] += child_dir["size"]
            node["loc"] += child_dir["loc"]
            node["ltok"] += child_dir["ltok"]
            node["totals"].update(child_dir["totals"])
        elif os.path.isfile(item_path):
            file_info = get_text_file_info(item_path, repo_root)
            if file_info is None:
                continue
            node["files"].append(file_info)
            node["size"] += file_info["size"]
            node["loc"] += file_info["loc"]
            node["ltok"] += file_info["ltok"]
            node["totals"].update(file_info["tags"])
    return node


def traverse_file(path, repo_root):
    file_info = get_text_file_info(path, repo_root)
    if file_info is None:
        return None
    return {
        "kind": "dir",
        "name": os.path.basename(path),
        "path": path,
        "size": file_info["size"],
        "loc": file_info["loc"],
        "ltok": file_info["ltok"],
        "dirs": [],
        "files": [file_info],
        "totals": Counter(file_info["tags"]),
    }


def traverse(path, repo_root):
    if is_git_ignored(path, repo_root):
        return None
    if os.path.isdir(path):
        return traverse_dir(path, repo_root)
    if os.path.isfile(path):
        return traverse_file(path, repo_root)
    return None


def top_tags(file_info, limit=3):
    items = sorted(
        file_info["tags"].items(),
        key=lambda kv: (-kv[1], file_info["order"].get(kv[0], 10**9), kv[0]),
    )
    return items[:limit]


def print_file_info(file_info, indent=""):
    first_tag = f" {file_info['first']}" if file_info["first"] else ""
    tags = top_tags(file_info, limit=3)
    tags_part = ""
    if tags:
        tags_part = " (" + " ".join(f"{count}{tag}" for tag, count in tags) + ")"
    print(
        f"{indent}{file_info['name']} {fmt_size(file_info['size'])} "
        f"({file_info['loc']} LOC {file_info['ltok']} LTOK){first_tag}{tags_part}"
    )


def print_file_tree(node, indent=""):
    print(
        f"{indent}{node['name']}/ {fmt_size(node['size'])} "
        f"({node['loc']} LOC {node['ltok']} LTOK)"
    )
    next_indent = indent + "  "
    for child_dir in node["dirs"]:
        print_file_tree(child_dir, next_indent)
    for file_info in node["files"]:
        print_file_info(file_info, next_indent)


def print_hahstags(totals):
    print("== TAG TOTALS ===")
    print(" ".join(f"{count}{tag}" for tag, count in sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))))


def print_all(nodes):
    print("== FILE TREE as NAME SIZE (LOC LTOK) FirstTag (Top 3 tags) ===")
    all_totals = Counter()
    for node in nodes:
        print_file_tree(node)
        all_totals.update(node["totals"])
    print_hahstags(all_totals)


def print_usage():
    print("USAGE:")
    print("  stirr-tree.py PATH1 [PATH2 ...]")
    print("  stirr-tree.py --help")


def main(argv):
    if not argv or argv[0] in {"-h", "--help"}:
        print_usage()
        return 0

    repo_root = get_repo_root()
    nodes = []
    for raw_path in argv:
        path = os.path.normpath(raw_path)
        node = traverse(path, repo_root)
        if node is not None:
            nodes.append(node)

    print_all(nodes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
