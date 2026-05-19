# ztypy

Python CLI for my zettelkasten system using Typst.

## Project layout

- `main.py` - CLI entry point
- `src/txtify.py` - `.typ` files to adjacency text
- `src/view.py` - adjacency text to interactive graph view
- `src/slipify.py` - adjacency text to generated `.typ` notes
- `tests/` - `unittest` test suite

## Usage

Run commands from the repo root:

```bash
python main.py txtify slipbox
python main.py view slipbox/output.txt --port 8000
python main.py slipify layout.txt --output-dir output
```

## Run tests

```bash
python -m unittest discover -s tests -v
```
