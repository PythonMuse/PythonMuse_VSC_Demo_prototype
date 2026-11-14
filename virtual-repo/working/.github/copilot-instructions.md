# Repository instructions

This repo turns raw point-of-sale exports into clean data and charts.

- Work happens through the skills in `.github/skills/`. Check for a matching
  skill before writing new code.
- Files in `data/raw/` are read-only inputs. Never edit them.
- Files in `data/processed/` and `reports/` are generated. Change the script
  that produces them, then re-run it.
- Python 3.11+, pandas, and seaborn. Run every command from the repo root.
