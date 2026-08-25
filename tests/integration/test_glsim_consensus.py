from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Independently assess one service measurement period"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"outcome": "SMALL_CREDIT"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_service_credit_period():
    owner, reporter = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "downtime_guarantee.py")
    terms = "At least 99.9 percent availability meets the guarantee. Below 99.9 but at least 99.0 earns SMALL_CREDIT. Below 99.0 earns LARGE_CREDIT. Missing measurements is UNVERIFIABLE."
    deployed = factory.deploy_contract_tx(args=[reporter.address, "Northwind Status API", terms], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    service = factory.build_contract(address, account=owner)
    record_writer = factory.build_contract(address, account=reporter)
    ok(service.open_period(args=["July 2026", "Measure the 31-day UTC calendar month using 44,640 total minutes."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(record_writer.submit_service_record(args=[1, "The signed export covers all 44,640 minutes and records 60 unavailable minutes, yielding 99.8656 percent availability."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(record_writer.assess_period(args=[1]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(service.acknowledge_period(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert service.get_program(args=[]).call()["total_credit_units"] == 1

