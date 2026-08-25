# Downtime Guarantee

Runs reusable service-measurement periods and converts stored availability records into bounded service-credit signals.

## Why GenLayer

Validators interpret a period record under fixed service-level terms and independently agree on MET, SMALL_CREDIT, LARGE_CREDIT, or UNVERIFIABLE.

## Reusable workflow

The owner opens one sequential period, the appointed reporter stores a measurement record, consensus assesses it, and the owner may acknowledge the result. Constructor parameters create a new independent instance, so the code is reusable; state is not shared between deployments.

The contract is deliberately non-custodial. It records a decision, entitlement, score, or approval signal and never transfers GEN.

## Evidence boundary

Only the reporter's on-chain measurement record and the constructor-fixed service terms are judged. The contract performs no web fetch and does not claim that a self-reported record is cryptographically authentic.

## Verify locally

```powershell
genvm-lint check contracts/downtime_guarantee.py
genvm-lint typecheck contracts/downtime_guarantee.py
pytest tests/direct -q
python tests/run_glsim.py --validators 5
```

With GLSim running in another terminal:

```powershell
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The live smoke test requires fresh test-only keys in `GENLAYER_PRIVATE_KEY`, `GENLAYER_SECONDARY_PRIVATE_KEY`. Never commit a `.env` file or use a production wallet.

```powershell
gltest tests/integration/test_studionet_smoke.py --network studionet -s -q --default-wait-interval=6000 --default-wait-retries=240
```

Use the documented 6-second StudioNet polling interval to stay comfortably below public endpoint limits.

See `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md`, and `deployments/studionet.json` for the review boundary and exact public evidence.
