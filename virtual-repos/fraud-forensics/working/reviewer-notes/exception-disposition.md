# Reviewer Disposition — AP Disbursement Fraud Triage, H1 2026

**R — Review the work and evidence.** Devraj Bose (manager, Harvey & Jenz CPAs) and Maya Ortiz reviewed all 20 exceptions in `outputs/exception-report.csv` against the validations in `instructions/validation-requirements.md`. Population reconciles: 34 source rows / $346,300.00 total; 34 rows analyzed, 0 excluded (see `evidence/population-reconciliation.md`).

Per assignment scope, no item below is characterized as fraud. Each disposition is either **closed as a false positive**, **closed as a genuine processing exception**, or **open, pending further investigation.**

## SiliconSerpent Supply Co — 5 payments near the $10,000 approval threshold

**Disposition: closed, false positive.** Confirmed against five separate TensorTurtle tooling POs (PO-33210, 33244, 33290, 33325, 33350), three different project cost centers, more than one approver. Ordinary project-based tooling billing, not structuring. No further action.

## NeuralNest Components — three invoice numbers for the same $4,820.00 payment

`INV-10482`, `INV10482`, `INV 10482`, same PO, nine days apart. **Disposition: open.** Contacted NeuralNest to confirm whether this represents one invoice submitted three times (data-entry/format drift) or three genuinely separate transactions. Recommend holding any further payment to this vendor pending the vendor's own invoice-history confirmation. Reassess once NeuralNest responds.

## QuantumCoil Materials — INV-55210 paid twice

**Disposition: closed, processing error confirmed.** Same invoice number, same $12,430.00 amount, paid seven days apart under two different approvers. No PO or business justification supports a second payment. Recommend: initiate recovery of the duplicate $12,430.00 payment, and add a duplicate-invoice-number system control if AP does not already have one.

## QuantumCoil Materials — credit memo CM-1187

**Disposition: closed, correctly applied.** CM-1187 references INV-55180 explicitly on its face — that part is a fact in this export. **Whether it was actually applied to that invoice in the AP system is a stipulated finding of this scenario, not something the export itself proves**: the disbursement population contains no application record. In the fictional investigation, Devraj Bose pulled the AP system's own application record — a system this export doesn't include — and confirmed the credit posted against INV-55180, not the ERP's oldest-open-invoice default. No exception.

## BrightPath Fulfillment Services — new vendor, three payments including one on a Saturday

Vendor created 2026-02-10; $2,400 → $48,500 → $31,200 across roughly three weeks, no PO on any of the three invoices, one payment (INV-0003) landing on a Saturday. **Disposition: open.** This population alone cannot establish who created the vendor record or whether that person also approved these payments — that requires the vendor-master change log, not the AP export. Recommend: pull the vendor-master change history for V-2201, confirm a business purpose and contract for the Special-Projects cost center spend, and require a PO on any future invoice from this vendor before payment.

## Meridian Pack & Fulfillment LLC — shares banking details with BrightPath, different GL coding

Vendor created 2026-03-18; $27,800.00 payment coded to GL 6420, while BrightPath (same remit-to bank account) is coded to GL 7400. **Disposition: open**, same recommendation as BrightPath above, plus: reconcile whether V-2201 and V-2202 should be a single vendor record, and if not, document the business reason two differently named vendors share payment details.

## Quorum Digital Media — three identical $15,000.00 payments

**Disposition: closed, false positive.** Confirmed flat monthly brand-retainer contract, same PO throughout. Round, recurring amounts are the expected shape of this arrangement. No further action.

## CoreStack Software Group — payment on Memorial Day

**Disposition: closed, false positive.** Recurring automated subscription payment; the same vendor, amount, and PO recur monthly elsewhere in the population regardless of weekday. The holiday date is incidental to the automated schedule. No further action.

## Kinetic Crate Logistics — volume increase from $6,200 to $40,000 across the period

**Disposition: closed, false positive.** Confirmed against the vendor's known onboarding as a new third-party logistics provider in this period; increasing volume during a fulfillment transition is the expected pattern, not evidence of irregular activity. No further action.

---

## Summary for the Document step

**Counted by matter, not by row.** A matter is one vendor group or one discrete issue, and a single matter can cover several exception rows — SiliconSerpent's near-threshold matter alone covers five. These eight matters therefore do **not** sum to the 20 exception rows in `outputs/exception-report.csv`, and the two figures should never be presented as if they were the same unit.

| Disposition | Matters | Exception rows covered |
|---|---|---|
| Closed — false positive | 4 (SiliconSerpent near-threshold 5; Quorum round-dollar 3; CoreStack holiday timing 1; Kinetic Crate Logistics volume increase 2) | 11 |
| Closed — genuine exception, resolved | 1 (QuantumCoil duplicate payment) | 2 |
| Open — pending further investigation | 2 (NeuralNest near-duplicate invoices 3; BrightPath 3 / Meridian 1 vendor pair) | 7 |
| **Total flagged** | **7 matters** | **20 rows** |
| Reviewed but never flagged | 1 (QuantumCoil credit memo CM-1187) | 0 |

**That last row is a teaching point, not a rounding artifact.** CM-1187 was confirmed correctly applied during human review, but it never appeared in the exception report at all — Test 9 flags only credit memos with *no* stated reference, and this one states INV-55180. A matter can be resolved by review without the automated tests ever raising it, which is precisely why the review step is not just a rubber stamp on the script's output.

Two items remain open pending outside information (vendor confirmation, vendor-master change log) this population alone cannot supply. Per `plan.md`'s Document step: if investigation ultimately changes a rule (e.g., a new PO-required control for newly created vendors), that change goes through review and approval before it's adopted — the workflow does not silently "learn" it.
