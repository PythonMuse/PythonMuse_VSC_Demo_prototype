I read `skills/excel-export-standard/SKILL.md` and opened [formatting_standard_demo.xlsx](outputs/excel/formatting_standard_demo.xlsx) with openpyxl to inspect the actual cells. The **Formula vs Hardcoded** tab sets the two side by side.

| Row | Prior (B) | Current (C) | Correct (D) | Wrong (E) |
|---|---|---|---|---|
| Sales - Demo Widget | 42,000.00 | 51,600.00 | `=C5-B5` | 9600 |
| COGS - Demo Materials | 18,000.00 | 23,400.00 | `=C6-B6` | 5400 |

Today both columns show the same numbers: 9,600 and 5,400. The difference is what sits behind each cell.

- **Formula (column D):** click the cell and the formula bar shows `=C5-B5`. A reviewer can see where the number comes from and re-derive it.
- **Hardcoded (column E):** click the cell and the formula bar shows a bare `9600`. The number may be right, but nothing proves it.

Change Current in C5 from 51,600 to 55,000 and recalculate. D5 becomes 13,000, but E5 stays at 9,600. The workbook now disagrees with itself and nothing warns you.

The **Formatting Standard** tab shows the same rule for percentages. Cell D5 holds `=(C5-B5)/ABS(B5)`, formatted `0.0%`, and the 15% threshold in D9 is formatted `0%`.

This is **Rule 8**: variance, percentage and total cells must be formulas referencing the raw data cells. A pasted value turns the workbook into a snapshot someone has to trust. A formula makes it a calculation someone can audit.

**Changes**

No files changed.

*Show me the trace, not the total.*
