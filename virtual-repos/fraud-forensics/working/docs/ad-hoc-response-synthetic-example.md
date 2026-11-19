# Ad Hoc AI Response — Synthetic Instructional Example

> ## THIS IS NOT A CAPTURED AI OUTPUT.
>
> The response below was **written by the instructor** for teaching purposes. It was not produced by, obtained from, or observed in any AI product. It is not a transcript, screenshot, log, export, or paraphrase of any real tool's behavior. No AI product, model, or vendor is named, depicted, or characterized anywhere in this file, and none should be named when it is presented.
>
> It is a constructed illustration of the *shape* of an uncontrolled answer: plausible in form, and deliberately defective in specific, checkable ways that this session then dissects. **The transaction amounts in it come from `raw-data/ap-disbursements-h1-2026.csv` — but several figures are deliberately planted defects, not sourced facts:** the stated $10,000 threshold appears nowhere in the export, "roughly 30 transactions" undercounts the real 34, and the closing "$215,000" total does not reconcile even to the response's own line items. Part 3 below maps every one of these.
>
> Data is synthetic. CodeCritters Inc. is PythonMuse's standing fictional company. **Do not cite, quote, excerpt, or redistribute this as evidence of any tool's performance.**
>
> Written by Svetlana Toohey, PythonMuse, for the 2026-11-13 session "AI-Assisted Accounting Workflows: From Prompt to Controlled Process."
>
> **This file is deliberately not part of the ONBOARD workspace.** The seven folders under `assets/` (`raw-data/`, `instructions/`, `plans/`, `scripts/`, `outputs/`, `evidence/`, `reviewer-notes/`) are the governed workflow. This document sits outside them on purpose — that absence is the point being made.

Used at **SEG-4 (17–22 min)**, as the "before" half of the before/after contrast, per `plan.md` §20 Build Sequence Phase 4.

---

## Part 1 — The prompt

Exactly as narrated in `transcript.txt` SEG-4:

> Review these disbursements for potential fraud and tell me what looks suspicious.

No file scope stated. No period. No definition of "suspicious." No tests named. No threshold. No output format. No prohibition on characterization. No approval step. The same 34-row disbursement file is attached; nothing else is supplied.

---

## Part 2 — The constructed response

*Constructed instructional example. Not a captured output.*

---

I reviewed the disbursement file you shared — roughly 30 transactions across several vendors for the first half of 2026. I focused on the higher-value vendors and the ones with repeat activity. Several patterns stand out, and a few are concerning. Here's what I found, highest risk first.

**1. BrightPath Fulfillment Services — HIGH RISK. Likely shell vendor.**
This vendor was created on 2026-02-10 and received $82,100 across three wire payments in under a month: $2,400, then $48,500, then $31,200. The small first payment is a classic test transaction to confirm the account works before the real money moves. None of the three has a purchase order, and all were approved by M. Osei, who also set up the vendor. The $31,200 payment was processed on a Saturday, outside normal business hours. This has the hallmarks of a fictitious-vendor scheme and should be escalated immediately.

**2. Meridian Pack & Fulfillment LLC — HIGH RISK. Same beneficiary as BrightPath.**
Created 2026-03-18, paid $27,800 by wire, again with no PO. Meridian shares a bank account with BrightPath, which confirms the two vendor records point to the same party. The GL coding was changed to 6420 so the payments would not surface next to BrightPath's in a 7400 review. Together these two vendors account for $109,900 of likely fraudulent disbursements.

**3. SiliconSerpent Supply Co — HIGH RISK. Payment structuring.**
Five payments between February and April, all between $9,650 and $9,910 — every one just under the $10,000 approval threshold, and each one approved by the same approver. This is textbook structuring: invoices split to stay below the limit that would trigger a second signature. Total $49,030.

**4. Quorum Digital Media — MEDIUM RISK. Round-dollar invoicing.**
Three payments of exactly $15,000.00 in February, March, and April. Perfectly round, perfectly regular amounts are a common signature of fabricated invoicing, because there is no underlying quantity or rate driving the number. Worth confirming the services were actually delivered.

**5. QuantumCoil Materials — MEDIUM RISK. Duplicate payment.**
INV-55210, $12,430.00, was paid twice — on 2026-03-20 and again on 2026-03-27. I checked the population for duplicate invoice numbers, and this was the only one.

**6. CoreStack Software Group — LOW-MEDIUM RISK. Holiday payment.**
$3,200 released on 2026-05-25, Memorial Day, when approval oversight is reduced.

**Summary.** Roughly $215,000 of the disbursements reviewed raise concern. The most urgent issue is the BrightPath/Meridian vendor pair, which shows the pattern of a fictitious-vendor scheme run through two related vendor records. I'd recommend freezing payments to both, pulling supporting documentation for the SiliconSerpent invoices, and looping in legal counsel before contacting either vendor.

Want me to draft a memo summarizing this for management?

---

*Constructed instructional example. Not a captured output.*

---

## Part 3 — What it gives you, and what it cannot answer

### Slide version (SEG-4, four rows)

| The answer gives you | The question it cannot answer |
|---|---|
| "Likely shell vendor." "Textbook structuring." | Did anything here become fraud? Who decided that, and on what authority? |
| "Just under the $10,000 approval threshold" | Where did that number come from? It is not in the file you gave it. |
| "This was the only duplicate." | Then what about the five rows it never mentioned? |
| "Roughly $215,000." | Out of what total? Does the list even add to that figure? |

### Full version (handout / this file)

| What the ad hoc answer has | What it omits — the control/evidence question |
|---|---|
| Vendor names and dollar amounts | Over what population? It says "roughly 30." The source is 34 rows — verify against `evidence/population-reconciliation.md`. |
| Confident risk ratings: HIGH / MEDIUM / LOW-MEDIUM | Rated against what criteria, set by whom? |
| A $10,000 approval threshold | Not present in the data. Where did it come from, and was it verified? (It happens to be correct — see `instructions/business-rules.md`. Right answer, no stated basis.) |
| "I focused on the higher-value vendors" | That is an exclusion, self-authorized, with no stated criteria. `instructions/assignment.md` states: "Exclusions: None." |
| Six vendor groups called out | What was tested and *not* found? What tests ran at all? Zero are named. |
| A duplicate invoice, correctly identified (QuantumCoil, INV-55210) | And the near-duplicates it declared did not exist? `INV-10482` / `INV10482` / `INV 10482` — three NeuralNest rows, $14,460, same PO, nine days apart — missed entirely. |
| "approved by the same approver" (SiliconSerpent) | **Factually wrong.** Three distinct approvers: R. Alvarez, T. Kim, J. Whitfield. It also never mentions that the five payments carry five distinct purchase orders and three different cost centers. Does that change the picture? |
| "shares a bank account ... which confirms" | The source has **no bank-account field**. It has a narrative note. Disclosed ≠ independently confirmed. |
| "The GL coding was changed to 6420 so the payments would not surface" | Invents a change event (no GL history in the export) and a motive. The GL difference is a fact; the motive is fabricated. |
| A cause attached to every pattern | Which of these is fully explained by context nobody supplied? |
| A confident total: "roughly $215,000" | Out of what denominator? Its own named items total closer to $219,560–$231,990 depending on how the QuantumCoil duplicate is counted — it does not even reconcile to itself. |
| Fraud-scheme vocabulary throughout | `instructions/assignment.md`: **"Do not characterize any transaction, vendor, or individual as fraudulent."** |
| A recommendation to freeze payments and call counsel | Whose decision is that, and where is it recorded? The workflow's own stopping point ends at "flagged for investigation." |
| Never mentions Kinetic Crate Logistics | Misses 2 rows / $40,000 (`material_volume_increase`). |
| Never mentions the CM-1187 credit memo | The −$1,240 credit memo is silently dropped — the one item governed by a tacit policy rule (apply only to the invoice named on its face) that no export field states. |
| An answer, in a chat window | Can a colleague reproduce it? Can you show your work in a year? |

**What it got right, and why that's the point.** This response is substantially correct — it names most of the rows the controlled workflow also flagged, gets the QuantumCoil duplicate's invoice number and both dates exactly right, and every per-group dollar figure it states is arithmetically accurate. **The problem is not that the answer is wrong. The problem is that you cannot tell which parts are wrong, and neither can anyone reading it later.**

---

## Part 4 — What replaced it

The same 34 rows, run through the ONBOARD workspace, produced instead:

`instructions/assignment.md` · `instructions/business-rules.md` · `instructions/validation-requirements.md` · `plans/approved-plan.md` · `scripts/forensic_review.py` · `outputs/exception-report.csv` · `outputs/summary.md` · `evidence/population-reconciliation.md` · `evidence/validation.md` · `evidence/execution-log.md` · `reviewer-notes/exception-disposition.md`

Eleven retained artifacts, over a read-only source population, with nine named tests, a stated threshold, a reconciled population of 34 rows / $346,300.00, an exception population of 20 rows / $286,450.00, an explicit prohibition on characterizing anything as fraudulent, and a named human's disposition of every exception matter.
