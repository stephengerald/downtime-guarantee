import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt)
    return receipt


@pytest.mark.integration
def test_studionet_period_assessment(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "downtime_guarantee.py")
    terms = "At least 99.9 percent availability meets the guarantee. Below 99.9 but at least 99.0 earns SMALL_CREDIT. Below 99.0 earns LARGE_CREDIT. Missing measurements is UNVERIFIABLE."
    deployed = _ok(factory.deploy_contract_tx(args=[secondary_account.address, "Northwind Status API", terms], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    owner = factory.build_contract(address, account=default_account)
    reporter = factory.build_contract(address, account=secondary_account)
    _ok(owner.open_period(args=["August 2026", "Measure the 31-day UTC month using 44,640 total minutes."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(reporter.submit_service_record(args=[1, "The signed export covers all 44,640 minutes and records 60 unavailable minutes, yielding 99.8656 percent availability."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = _ok(reporter.assess_period(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    period = owner.get_period(args=[1]).call()
    assert period["outcome"] in ("MET", "SMALL_CREDIT", "LARGE_CREDIT", "UNVERIFIABLE")
    assert owner.get_policy(args=[]).call()["stored_evidence_only"] is True
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": period["outcome"]}, sort_keys=True))
