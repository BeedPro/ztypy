#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Tuple


@dataclass(frozen=True)
class Note:
    title: str
    note_id: str


def parse_adjacency_layout(layout_path: Path) -> Tuple[Dict[str, List[str]], Set[str]]:
    """
    Parse an adjacency-list style text file.

    Main (non-indented) lines are source nodes.
    Indented lines beneath are directly connected target nodes.
    """
    adjacency: Dict[str, List[str]] = {}
    all_nodes: Set[str] = set()
    current_parent: str | None = None

    for raw in layout_path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue

        if raw[:1].isspace():
            child = raw.strip()
            if current_parent is None:
                raise ValueError(f"Found child without parent: {raw!r}")
            adjacency.setdefault(current_parent, []).append(child)
            all_nodes.add(child)
        else:
            current_parent = raw.strip()
            adjacency.setdefault(current_parent, [])
            all_nodes.add(current_parent)

    return adjacency, all_nodes


def generate_note_ids(nodes: List[str]) -> Dict[str, Note]:
    """
    Generate deterministic timestamp-like IDs in YYYYMMDDHHMMSS format.
    """
    base = datetime.now().replace(microsecond=0)
    notes: Dict[str, Note] = {}

    for index, title in enumerate(nodes):
        note_time = base + timedelta(seconds=index)
        note_id = note_time.strftime("%Y%m%d%H%M%S")
        notes[title] = Note(title=title, note_id=note_id)

    return notes


def phase_1_create_files(output_dir: Path, notes: Dict[str, Note]) -> None:
    """
    Create all files first with minimal skeleton and placeholder fields.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    base_content = (
        '#import ".utility/style.typ": style\n'
        "#show: style\n\n"
        '#let title = ""\n'
        "#let id = 0\n\n"
        "#id:ghost:\n\n"
        "= #title\n\n"
        "= Links\n\n"
        '#bibliography(".utility/sources.yaml")\n'
    )

    for note in notes.values():
        file_path = output_dir / f"{note.note_id}.typ"
        file_path.write_text(base_content, encoding="utf-8")


def phase_2_add_titles(output_dir: Path, notes: Dict[str, Note]) -> None:
    """
    Fill in title and id for every generated file.
    """
    for note in notes.values():
        file_path = output_dir / f"{note.note_id}.typ"
        content = file_path.read_text(encoding="utf-8")
        content = content.replace('#let title = ""', f'#let title = "{note.title}"', 1)
        content = content.replace("#let id = 0", f"#let id = {note.note_id}", 1)
        file_path.write_text(content, encoding="utf-8")


def phase_3_add_links(
    output_dir: Path,
    notes: Dict[str, Note],
    adjacency: Dict[str, List[str]],
) -> None:
    """
    Add forward links under '= Links' as '- YYYYMMDDHHMMSS'.
    A node lists the note IDs of nodes it links to (its children).
    """
    for title, note in notes.items():
        child_ids: Set[str] = set()
        for child in adjacency.get(title, []):
            child_ids.add(notes[child].note_id)

        note = notes[title]
        file_path = output_dir / f"{note.note_id}.typ"
        content = file_path.read_text(encoding="utf-8")

        if child_ids:
            links_block = "\n".join(f"- {link_id}" for link_id in sorted(child_ids))
        else:
            links_block = ""

        content = content.replace("= Links", f"= Links\n\n{links_block}", 1)
        file_path.write_text(content, encoding="utf-8")


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    layout_path = script_dir / "layout.txt"
    output_dir = Path.cwd() / "output"

    if not layout_path.exists():
        raise FileNotFoundError(f"Layout file not found: {layout_path}")

    adjacency, all_nodes = parse_adjacency_layout(layout_path)
    ordered_nodes = sorted(all_nodes)
    notes = generate_note_ids(ordered_nodes)

    phase_1_create_files(output_dir, notes)
    phase_2_add_titles(output_dir, notes)
    phase_3_add_links(output_dir, notes, adjacency)

    print(f"Generated {len(notes)} files in {output_dir}")


if __name__ == "__main__":
    main()
