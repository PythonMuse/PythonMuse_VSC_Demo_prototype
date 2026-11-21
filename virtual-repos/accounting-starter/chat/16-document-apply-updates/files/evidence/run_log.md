# Run log

## Run 1 - controlled test, Apr YoY only

- Script: scripts/tb_compare.py (sha256 71eccadad481)
- Plan: plan.md (sha256 6983b01c978f)
- Thresholds: YoY > $2,500 and > 15%; MoM > $2,500 and > 20%. Source: typed in the script
- Inputs: data/raw/trial_balance_2025.csv (sha256 3450df5f866d), data/raw/trial_balance_2026.csv (sha256 0b9e667b5e17)
- Rows read 32 + 32; used 32 + 32; excluded 0
- Reconciliation: 8 of 8 months balance, difference 0.00
- YoY flags: 7. MoM not run

## Run 2 - full run

- Script: scripts/tb_compare.py (sha256 71eccadad481)
- Plan: plan.md (sha256 6983b01c978f)
- Thresholds: YoY > $2,500 and > 15%; MoM > $2,500 and > 20%. Source: typed in the script
- Inputs: data/raw/trial_balance_2025.csv (sha256 3450df5f866d), data/raw/trial_balance_2026.csv (sha256 0b9e667b5e17)
- Rows read 32 + 32; used 32 + 32; excluded 0
- Reconciliation: 8 of 8 months balance, difference 0.00
- YoY flags: 21. MoM flags: 7

## Run 3 - full run

- Script: scripts/tb_compare.py (sha256 dcd7a0213b3d)
- Plan: plan.md (sha256 75ec5995965c)
- Thresholds: YoY > $2,500 and > 15%; MoM > $2,500 and > 20%. Source: plan.md front matter
- Inputs: data/raw/trial_balance_2025.csv (sha256 3450df5f866d), data/raw/trial_balance_2026.csv (sha256 0b9e667b5e17)
- Rows read 32 + 32; used 32 + 32; excluded 0
- Reconciliation: 8 of 8 months balance, difference 0.00
- YoY flags: 21. MoM flags: 7

