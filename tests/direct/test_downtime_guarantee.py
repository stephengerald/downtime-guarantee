from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "downtime_guarantee.py"
SDK = "v0.2.16"
PROMPT = "Independently assess one service measurement period"
TERMS = "For each monthly period, at least 99.9 percent availability meets the guarantee. Availability below 99.9 but at least 99.0 earns SMALL_CREDIT. Below 99.0 earns LARGE_CREDIT. Missing total-window or downtime measurements is UNVERIFIABLE."


def deploy(vm, direct_deploy, alice, bob):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), "0x" + bob.hex(), "Northwind Status API", TERMS, sdk_version=SDK)


def test_period_credit_is_recorded_and_acknowledged(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    contract.open_period("July 2026", "Measure the 31-day UTC calendar month using 44,640 total minutes.")
    direct_vm.sender = direct_bob
    contract.submit_service_record(1, "The signed monitoring export covers all 44,640 minutes and records 60 minutes unavailable, yielding 99.8656 percent availability.")
    direct_vm.mock_llm(PROMPT, json.dumps({"outcome": "SMALL_CREDIT"}))
    contract.assess_period(1)
    direct_vm.sender = direct_alice
    contract.acknowledge_period(1)
    assert contract.get_program()["total_credit_units"] == 1
    assert contract.get_period(1)["acknowledged"] is True
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_unverifiable_record_has_one_revision(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    contract.open_period("August 2026", "Measure every minute in the 31-day UTC calendar month and state both total and unavailable minutes.")
    direct_vm.sender = direct_bob
    contract.submit_service_record(1, "The export says availability was good for most of August, but it omits total monitored minutes and exact unavailable minutes required by the frozen guarantee.")
    direct_vm.mock_llm(PROMPT, json.dumps({"outcome": "UNVERIFIABLE"}))
    contract.assess_period(1)
    contract.replace_unverifiable_record(1, "The corrected export covers 44,640 total monitored minutes and 12 unavailable minutes, yielding 99.9731 percent availability.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"outcome": "MEETS_GUARANTEE"}))
    contract.assess_period(1)
    assert contract.get_period(1)["record_revised"] is True
    with direct_vm.expect_revert("only_unverifiable_record_can_be_replaced"):
        contract.replace_unverifiable_record(1, "A second replacement must not be accepted after the corrected record has already produced a settled outcome.")


def test_reporter_authority_and_bad_output_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    contract.open_period("September 2026", "Measure all 43,200 minutes in the 30-day UTC calendar month.")
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_record_reporter"):
        contract.submit_service_record(1, "An unrelated account must not be allowed to provide the official stored measurement record for this period.")
    direct_vm.sender = direct_bob
    contract.submit_service_record(1, "The complete record covers 43,200 minutes and reports zero unavailable minutes, yielding 100 percent availability.")
    direct_vm.mock_llm(PROMPT, json.dumps({"outcome": "MAYBE"}))
    with direct_vm.expect_revert("invalid_outcome"):
        contract.assess_period(1)
    assert contract.get_period(1)["outcome"] == "READY_FOR_ASSESSMENT"

