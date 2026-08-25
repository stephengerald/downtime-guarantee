# Submission: Downtime Guarantee

Project name: Downtime Guarantee

Repository: https://github.com/stephengerald/downtime-guarantee

StudioNet contract: https://explorer-studio.genlayer.com/address/0xf88354c0f875b3a49C3E2332Da19cF2bb41594d1

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x1fc131a56baf909d39fbd3b2737cfc5a7a869a78e2e25b4aec255b60d7fb0c66

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0xce4058a90278a2e11228774ca1d198039cdc040d6e5e9ab7ab38d85bf7aecdf7

Summary: Runs reusable service-measurement periods and converts stored availability records into bounded service-credit signals.

Why it is GenLayer-native: Validators interpret a period record under fixed service-level terms and independently agree on MET, SMALL_CREDIT, LARGE_CREDIT, or UNVERIFIABLE.

Evidence/source model: Only the reporter's on-chain measurement record and the constructor-fixed service terms are judged. The contract performs no web fetch and does not claim that a self-reported record is cryptographically authentic.

Declared scope: Reusable, non-custodial prototype. Credit units are non-custodial signals. Production use needs authenticated telemetry, a correction policy, and a separately reviewed settlement adapter.

Review evidence: `AUDIT.md`, `SECURITY.md`, `SOURCE_POLICY.md`, and `deployments/studionet.json` bind the reviewed source hash to the public live result.
