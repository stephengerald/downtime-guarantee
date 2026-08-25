# Architecture

## State machine

The owner opens one sequential period, the appointed reporter stores a measurement record, consensus assesses it, and the owner may acknowledge the result.

The relevant roles are service owner and independent record reporter. Write methods enforce role, phase, uniqueness, and bounded-storage rules before any state transition.

## Consensus boundary

Validators interpret a period record under fixed service-level terms and independently agree on MET, SMALL_CREDIT, LARGE_CREDIT, or UNVERIFIABLE. The leader returns a small JSON schema; validators independently rerun the same decision function and accept only exact enum or bitmask values. Malformed model output raises a tagged model error and writes no decision.

## Deterministic boundary

Enrollment, authorization, commitments, counters, phase changes, caps, masks, and any score or credit arithmetic are deterministic contract logic. Only semantic interpretation of the stored evidence occurs inside `run_nondet_unsafe`.

## Off-chain boundary

Wallet custody, identity verification, indexing, notifications, private file storage, source authentication, money movement, legal process, and user-interface behavior are outside this repository. Credit units are non-custodial signals. Production use needs authenticated telemetry, a correction policy, and a separately reviewed settlement adapter.
