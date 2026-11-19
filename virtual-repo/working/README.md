# store-sales

Quarterly sales reporting for three coffee shops. Raw point-of-sale exports go
in, tidy CSVs and charts come out. The *how* lives in two agent skills that any
coding agent (or person) can follow.

## Layout

| Path                           | What lives there                        |
|--------------------------------|-----------------------------------------|
| `.github/skills/clean-orders/` | Skill: clean and summarize raw orders   |
| `.github/skills/sales-charts/` | Skill: draw the seaborn charts          |
| `data/raw/`                    | POS exports, exactly as received        |
| `data/processed/`              | Script output, never edited by hand     |
| `reports/`                     | PNG charts built from `data/processed/` |

## Anatomy of a skill

- `SKILL.md` says when to use the skill and which steps to follow
- `references/` holds knowledge the agent reads on demand (rules, style guides)
- `scripts/` holds code the agent runs instead of rewriting it every time

## Run it yourself

```bash
pip install -r requirements.txt
python .github/skills/clean-orders/scripts/clean_orders.py
python .github/skills/clean-orders/scripts/summarize_orders.py
python .github/skills/sales-charts/scripts/plot_sales.py
```
