from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src import slipify


class SlipifyTests(unittest.TestCase):
    def test_parse_adjacency_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            layout = Path(temp_dir) / "layout.txt"
            layout.write_text("A\n    B\nC\n", encoding="utf-8")

            adjacency, all_nodes = slipify.parse_adjacency_layout(layout)
            self.assertEqual(adjacency["A"], ["B"])
            self.assertEqual(adjacency["C"], [])
            self.assertEqual(all_nodes, {"A", "B", "C"})

    def test_run_creates_typ_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            layout = temp_path / "layout.txt"
            out_dir = temp_path / "out"
            layout.write_text("Parent\n    Child\n", encoding="utf-8")

            result_dir = slipify.run(str(layout), str(out_dir))
            files = sorted(result_dir.glob("*.typ"))

            self.assertEqual(len(files), 2)
            content = files[0].read_text(encoding="utf-8")
            self.assertIn("#let title =", content)
            self.assertIn("= Links", content)


if __name__ == "__main__":
    unittest.main()
