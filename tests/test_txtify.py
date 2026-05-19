from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src import txtify


class TxtifyTests(unittest.TestCase):
    def test_extract_children_ids_reads_links_section(self) -> None:
        content = """= #title

= Links

- 20260101010101
- nope
- 20260101010102

#bibliography(".utility/sources.yaml")
"""
        self.assertEqual(
            txtify.extract_children_ids(content),
            ["20260101010101", "20260101010102"],
        )

    def test_build_adjacency_text_uses_titles(self) -> None:
        nodes = {
            "20260101010101": txtify.Node(
                note_id="20260101010101",
                title="Alpha",
                children_ids=["20260101010102"],
            ),
            "20260101010102": txtify.Node(
                note_id="20260101010102",
                title="Beta",
                children_ids=[],
            ),
        }
        output = txtify.build_adjacency_text(nodes)
        self.assertIn("Alpha\n    Beta", output)
        self.assertIn("Beta", output)

    def test_run_writes_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "20260101010101.typ").write_text(
                '#let title = "A"\n= Links\n- 20260101010102\n',
                encoding="utf-8",
            )
            (temp_path / "20260101010102.typ").write_text(
                '#let title = "B"\n= Links\n',
                encoding="utf-8",
            )

            output_path = txtify.run(temp_dir)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
