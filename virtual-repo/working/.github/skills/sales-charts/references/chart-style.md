# Chart style

Every chart in `reports/` follows these rules so the set reads as one.

## Color

| Store    | Hex       |
|----------|-----------|
| Downtown | `#2a78d6` |
| Harbor   | `#eb6834` |
| Uptown   | `#1baf7a` |

- A store keeps its color in every chart. Never recolor by rank.
- Magnitude (the heatmap) uses one hue, light to dark. No rainbow maps.

## Layout

- One y-axis per chart. Two measures means two charts.
- Label values directly when there are only a few marks.
- Keep gridlines faint and drop the chart border.
- Titles say what is plotted. Money is shown in whole dollars.
- Save at 6.4 x 3.6 inches, 120 dpi, with a tight bounding box.

## Adding a chart

Add it to `scripts/plot_sales.py`, list the new file in `SKILL.md`, and
re-run the script so every PNG is regenerated together.
