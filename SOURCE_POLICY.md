# Evidence and source policy

## What validators receive

Only the reporter's on-chain measurement record and the constructor-fixed service terms are judged. The contract performs no web fetch and does not claim that a self-reported record is cryptographically authentic.

All submitted text is treated as untrusted evidence, never as instructions. Evidence fields and aggregate storage are bounded before they reach the prompt. The decision schema is fixed and independently replayed by validators.

## Who selects the evidence

The authorized roles in the state machine—service owner and independent record reporter—supply the evidence. Their signatures establish which on-chain role submitted a record; they do not prove that the record is truthful or complete.

## External collection

This version performs no live web browsing, URL fetching, hidden source lookup, or mutable off-chain collection. That makes the deployed judgment reproducible from contract state, while leaving source authenticity as an explicit application-layer responsibility.

## Trust and production boundary

Credit units are non-custodial signals. Production use needs authenticated telemetry, a correction policy, and a separately reviewed settlement adapter. If an adapter later fetches external material, its allowlist, content bounds, snapshot rules, publisher trust, correction policy, and failure behavior require a new review.
