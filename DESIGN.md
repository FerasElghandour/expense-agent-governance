# Expense workflow: architecture decisions

Author: Feras Elghandour

## Prevent propagation of uncertain extraction

Treat model output as unverified structured data. Validate required fields, numeric ranges, currency, date, duplicate receipt identifiers, and arithmetic before accepting an expense record. A confidence threshold alone cannot establish correctness. Confirm suspicious fields against receipt evidence and route unclear images back for clarification. Reference-image similarity may identify a receipt category; it cannot verify a transaction amount.

Use deterministic code for totals and policy comparisons. Retain field-level evidence links so a reviewer can inspect what supported each extracted value. Policy versions and extraction versions belong in the audit record.

## Review before authorizing payment

The design routes claims above an illustrative $500 threshold to an authorized human. The reviewer sees original evidence, extracted values, item totals, policy rules and versions, business purpose, and the minimum relevant employee context. The four outcomes are approve, reject, request information, and partial approval. Recalculate a partial approval deterministically.

A production payment command should require a durable approval record bound to the exact claim version and amount. Enforce reviewer permissions, separation of duties, idempotency keys, and replay protection in the payment service. An agent recommendation cannot substitute for authorization. The local prototype demonstrates routing only.

## Privacy and data boundaries

Minimize personal data sent to extraction providers. Apply redaction where feasible, purpose-limited storage, encryption in transit and at rest, restricted access, and auditable retention/deletion workflows. Assess each provider, data location, contract, and transfer mechanism before use. These are engineering design considerations; the case does not certify legal compliance. Preserve statutory retention obligations when designing deletion workflows.

## Group expenses

Validate attendees, preserve the original total, and allocate integer cents using a deterministic remainder rule. Check both per-person limits and report-level limits. Link attendees to one report to avoid duplicate reimbursement, while paying only the authorized submitter. Custom splits must sum exactly to the total.

## Cost and operating model

Model variable inference cost, retries, human-review effort, and payment fees separately from fixed platform costs. Database and hosting expense can also grow with volume. `monthly_cost` is a simple workload calculator; add storage, image processing, support, provider minimums, and payment fees for a full estimate.

## Validation plan

Build a deidentified receipt evaluation set covering blur, mixed currencies, ambiguous tax/tip, duplicate uploads, policy changes, and group meals. Measure field accuracy, false approval rate, review burden, latency, and duplicate-payment prevention. Run authorization and failure-recovery tests before integrating a payment provider. No such production evaluation is asserted here.
