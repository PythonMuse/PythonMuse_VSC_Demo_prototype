# Business Rules and Context — CodeCritters AP Disbursements

**B — Brief the AI.** This is the context given *before* execution (`plan.md` §10 B-step) — general institutional knowledge, not row-by-row answers. Note what's deliberately absent: specific PO-to-project mappings, vendor-master change history, and other facts that only surface during **Review**, once an exception is actually investigated. Briefing the AI with the *answer* to every exception in advance would defeat the point of the exercise — real business context is categorical, not row-level.

## Approval and process conventions

- **Approval threshold:** disbursements of $10,000 or more require a second approver. Payments under this threshold are single-approver.
- **Standard payment methods:** ACH for recurring/established vendors, wire for one-off or newly onboarded vendors, check for a small number of legacy suppliers (e.g., Harborview Office Supply).
- **Invoice-number convention:** CodeCritters' AP system does not enforce a single invoice-number format across vendors — vendors submit invoice numbers in whatever format their own systems produce, including inconsistent punctuation and spacing. AP does not normalize these on entry.

## Known vendor relationships

- **SiliconSerpent Supply Co** — long-standing packaging/tooling supplier for the TensorTurtle product line (GL 6410). Bills per tooling project, not on a blanket PO; **multiple concurrent tooling projects with separate POs and project managers is normal for this vendor** — the specific PO-to-project mapping for any given payment is not pre-loaded here and should be looked up during investigation, not assumed.
- **QuantumCoil Materials** and **NeuralNest Components** — established raw-materials suppliers, ordinary recurring purchase-order activity.
- **Kinetic Crate Logistics** — third-party fulfillment/logistics provider, onboarded January 2026. Volume with this vendor is expected to increase through H1 2026 as fulfillment volume transitions to them; a rising trend alone is not unusual for a vendor in its onboarding ramp.
- **Quorum Digital Media** — marketing vendor under a **flat monthly retainer contract**; recurring identical round-dollar payments are the expected shape of a retainer, not evidence of structuring.
- **CoreStack Software Group** — recurring monthly software subscription on an automated payment schedule; the payment date follows the automated schedule regardless of weekends or holidays.
- **BrightPath Fulfillment Services** and **Meridian Pack & Fulfillment LLC** — **no prior relationship history.** Neither vendor has an established pattern to compare against; treat any activity from either as new-vendor activity by definition.

## Credit memo policy

A credit memo applies **only to the specific invoice referenced on its face.** The AP system's default behavior, if a credit is entered without an explicit reference, is to apply it to the oldest open invoice for that vendor — which is the opposite of policy. Confirm the referenced invoice number before accepting any credit-memo application as correct.

## What this briefing deliberately does not include

- Which specific project or project manager each SiliconSerpent PO belongs to.
- Whether the same person created the BrightPath or Meridian vendor records and approved their payments — that requires the vendor-master change log, not the AP export.
- Any conclusion about whether BrightPath and Meridian are related. The shared remit-to bank detail is a fact in the data; what it means is not.

These are investigation questions, not briefing facts — see `reviewer-notes/exception-disposition.md` for how they get resolved.
