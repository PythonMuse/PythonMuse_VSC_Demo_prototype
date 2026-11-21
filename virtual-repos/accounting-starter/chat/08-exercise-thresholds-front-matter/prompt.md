---
title: Exercise · Put the thresholds in plan.md front matter
---
Add this block to the very top of `plan.md`, exactly as written, and add the Materiality section below the page title:

```markdown
---
workflow: codecritters-tb-comparison
period: 2026-01 to 2026-04
compare_to: 2025-01 to 2025-04
yoy_threshold: { dollars: 2500, percent: 15 }
mom_threshold: { dollars: 2500, percent: 20 }
reviewer: Controller
---
## Materiality
Flag only when **both** the dollar and the percent bar are cleared.
```
