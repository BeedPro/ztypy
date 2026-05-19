from __future__ import annotations

import unittest
from unittest.mock import patch

import main


class MainCliTests(unittest.TestCase):
    def test_build_parser_has_txtify_command(self) -> None:
        parser = main.build_parser()
        args = parser.parse_args(["txtify", "."])
        self.assertEqual(args.command, "txtify")

    def test_main_prints_help_without_command(self) -> None:
        with (
            patch("argparse.ArgumentParser.print_help") as help_mock,
            patch("sys.argv", ["main.py"]),
        ):
            main.main()
            self.assertTrue(help_mock.called)

    def test_main_executes_selected_command(self) -> None:
        with (
            patch("src.txtify.run") as run_mock,
            patch("sys.argv", ["main.py", "txtify", "."]),
        ):
            main.main()
            self.assertTrue(run_mock.called)


if __name__ == "__main__":
    unittest.main()
