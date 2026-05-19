from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src import view


class ViewTests(unittest.TestCase):
    def test_parse_adjacency_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            layout = Path(temp_dir) / "output.txt"
            layout.write_text("Root\n    Child\n", encoding="utf-8")

            nodes, edges = view.parse_adjacency_layout(layout)
            self.assertEqual(nodes, ["Child", "Root"])
            self.assertEqual(edges, [("Root", "Child")])

    def test_build_html_contains_node_and_edge_data(self) -> None:
        html = view.build_html("Graph", ["A", "B"], [("A", "B")])
        self.assertIn("Graph", html)
        self.assertIn('"id": "A"', html)
        self.assertIn('"from": "A"', html)


if __name__ == "__main__":
    unittest.main()
