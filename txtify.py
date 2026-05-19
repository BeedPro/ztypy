#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


FILENAME_RE = re.compile(r"^(\d{14})\.typ$")
TITLE_RE = re.compile(r'^#let\s+title\s*=\s*"(.*)"\s*$')


@dataclass
class Node:
    note_id: str
    title: str
    children_ids: List[str]


def extract_title(content: str, file_path: Path) -> str:
    for line in content.splitlines():
        match = TITLE_RE.match(line.strip())
        if match:
            return match.group(1)
    raise ValueError(f"Missing '#let title = \"...\"' in {file_path}")


def extract_children_ids(content: str) -> List[str]:
    lines = content.splitlines()
    links_index = None

    for idx, line in enumerate(lines):
        if line.strip() == "= Links":
            links_index = idx
            break

    if links_index is None:
        return []

    children: List[str] = []
    for line in lines[links_index + 1 :]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("=") or stripped.startswith("#bibliography"):
            break
        if stripped.startswith("- "):
            link_id = stripped[2:].strip()
            if re.fullmatch(r"\d{14}", link_id):
                children.append(link_id)

    return children


def load_nodes_from_directory(typ_dir: Path) -> Dict[str, Node]:
    typ_files = sorted(typ_dir.glob("*.typ"))
    if not typ_files:
        raise ValueError(f"No .typ files found in {typ_dir}")

    nodes: Dict[str, Node] = {}
    invalid_names: List[str] = []

    for path in typ_files:
        match = FILENAME_RE.fullmatch(path.name)
        if not match:
            invalid_names.append(path.name)
            continue

        note_id = match.group(1)
        content = path.read_text(encoding="utf-8")
        title = extract_title(content, path)
        children_ids = extract_children_ids(content)
        nodes[note_id] = Node(note_id=note_id, title=title, children_ids=children_ids)

    if invalid_names:
        invalid_list = "\n".join(f"- {name}" for name in invalid_names)
        raise ValueError(
            "Found .typ files with invalid names. Expected YYYYMMDDHHMMSS.typ:\n"
            f"{invalid_list}"
        )

    return nodes


def build_adjacency_text(nodes: Dict[str, Node]) -> str:
    id_to_title = {node.note_id: node.title for node in nodes.values()}
    ordered_nodes = [nodes[note_id] for note_id in sorted(nodes)]

    blocks: List[str] = []
    for node in ordered_nodes:
        block_lines = [node.title]
        for child_id in sorted(set(node.children_ids)):
            child_title = id_to_title.get(child_id)
            if child_title is not None:
                block_lines.append(f"    {child_title}")
        blocks.append("\n".join(block_lines))

    return "\n\n".join(blocks) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate adjacency list output.txt from Typst notes directory."
    )
    parser.add_argument("directory", help="Directory containing .typ files")
    args = parser.parse_args()

    typ_dir = Path(args.directory).resolve()
    if not typ_dir.exists() or not typ_dir.is_dir():
        raise FileNotFoundError(f"Directory not found: {typ_dir}")

    nodes = load_nodes_from_directory(typ_dir)
    adjacency_text = build_adjacency_text(nodes)

    output_path = typ_dir / "output.txt"
    output_path.write_text(adjacency_text, encoding="utf-8")
    print(f"Wrote adjacency list to {output_path}")


if __name__ == "__main__":
    main()
