I read [SKILL.md](skills/ap-disbursement-fraud-triage/SKILL.md), [approved-plan.md](plans/approved-plan.md) and [business-rules.md](instructions/business-rules.md), then ran `python scripts/forensic_review.py` as the skill's "How to run it" section specifies. The script read the source file read-only and wrote only to `outputs/` and `evidence/`.

**Reconciliation**

| | Rows | Dollars |
|---|---|---|
| Source population | 34 | $346,300.00 |
| Rows excluded | 0 | n/a |
| Analyzed | 34 | $346,300.00 |
| Exceptions requiring follow-up | 20 (58.8%) | $286,450.00 (82.7%) |

**Rows flagged per test**

| Test | Rows |
|---|---|
| `near_approval_threshold` | 5 |
| `new_vendor_in_period` | 4 |
| `near_duplicate_invoice_number` | 3 |
| `recurring_round_dollar_payment` | 3 |
| `exact_duplicate_invoice` | 2 |
| `material_volume_increase` | 2 |
| `weekend_or_holiday_payment` | 2 |
| `related_vendor_gl_inconsistency` | 1 |

The credit-memo reference check flagged nothing. The tags add up to 22 because two rows trigger two tests each: BrightPath INV-0003 (new vendor and Saturday payment) and Meridian INV-5501 (new vendor and disclosed shared banking).

**What the flags are, and are not.** These are exceptions requiring follow-up, not conclusions. Some have context in [business-rules.md](instructions/business-rules.md), such as the Quorum retainer and the CoreStack automated schedule, but the script does not resolve them. The population alone also cannot say who created the BrightPath and Meridian vendor records.

**Next step is human.** Disposition each exception in [exception-disposition.md](reviewer-notes/exception-disposition.md): false positive, genuine exception, or open pending outside information.

**Changes**

- Wrote [exception-report.csv](outputs/exception-report.csv)
- Wrote [summary.md](outputs/summary.md)
- Wrote [population-reconciliation.md](evidence/population-reconciliation.md)
