# Generator

Builds the SVG sheets in `../assets` and `../README.md`.

```bash
python3 generator/gen.py
```

Language data lives in `data/langs.json` (bytes per language across public repos); refresh it from the
GitHub API when needed. Text and palette are defined at the top of `gen.py`.
