"""Draw the standard sales charts. Style: ../references/chart-style.md"""
import os

import pandas as pd
import seaborn as sns

COLORS = {"Downtown": "#2a78d6", "Harbor": "#eb6834", "Uptown": "#1baf7a"}
clean = pd.read_csv("data/processed/orders_clean.csv")
monthly = pd.read_csv("data/processed/monthly_summary.csv")
sns.set_theme(style="whitegrid", rc={"figure.figsize": (6.4, 3.6)})
os.makedirs("reports", exist_ok=True)

def save(ax, name, title, ylabel="Revenue ($)"):
    ax.set(title=title, xlabel="", ylabel=ylabel)
    ax.tick_params(axis="y", rotation=0)
    sns.despine(ax=ax, left=True)
    ax.figure.savefig(f"reports/{name}", dpi=120, bbox_inches="tight")
    ax.figure.clf()
    print(f"wrote reports/{name}")

ax = sns.barplot(clean, x="store", y="revenue", hue="store", palette=COLORS,
                 estimator="sum", errorbar=None, width=0.5, saturation=1)
for bars in ax.containers:
    ax.bar_label(bars, fmt="${:,.0f}", padding=3)
save(ax, "revenue_by_store.png", "Revenue by store, Q1 2026")

ax = sns.lineplot(monthly, x="month", y="revenue", hue="store", palette=COLORS,
                  hue_order=list(COLORS), marker="o", linewidth=2)
save(ax, "monthly_trend.png", "Monthly revenue by store")

mix = clean.pivot_table("revenue", "store", "category", aggfunc="sum")
ax = sns.heatmap(mix, annot=True, fmt=",.0f", cmap="Blues", cbar=False, linewidths=2)
save(ax, "category_heatmap.png", "Revenue by store and category ($)", ylabel="")
