---
name: sales-charts
description: >-
  Draw the standard seaborn sales charts (revenue by store, monthly trend,
  category heatmap) from the processed CSVs. Use when asked to plot, chart,
  visualize, or refresh the reports folder.
---

# Sales charts

Render the PNGs in `reports/` from the files in `data/processed/`.

## Steps

1. If `data/processed/` is missing or older than `data/raw/`, run the
   `clean-orders` skill first. Never chart raw data.
2. Read [chart-style.md](references/chart-style.md) before changing a chart.
3. Run from the repo root:
   `python .github/skills/sales-charts/scripts/plot_sales.py`
4. Open each PNG and check it against the style rules before reporting back.

## Charts

| File                   | seaborn call | Question it answers         |
|------------------------|--------------|-----------------------------|
| `revenue_by_store.png` | `barplot`    | Which store sells the most? |
| `monthly_trend.png`    | `lineplot`   | How is each store trending? |
| `category_heatmap.png` | `heatmap`    | What sells where?           |
