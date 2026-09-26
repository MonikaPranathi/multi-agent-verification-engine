from orchestration.orchestrator import decide_next_step


# Common data

calculation_failed = {
    "passed": False,
    "reported_score": 90,
    "verified_score": 80
}

calculation_passed = {
    "passed": True,
    "reported_score": 80,
    "verified_score": 80
}

evidence_failed = {
    "passed": False,
    "evidence_status": "INSUFFICIENT"
}

evidence_passed = {
    "passed": True,
    "evidence_status": "SUFFICIENT"
}

no_contradiction = {
    "result": {
        "contradiction_detected": False,
        "severity": "NONE"
    }
}

high_contradiction = {
    "result": {
        "contradiction_detected": True,
        "severity": "HIGH"
    }
}


# Scenario 1: Calculation failed

result = decide_next_step(
    calculation_failed,
    evidence_failed,
    no_contradiction
)

print("\n========== CALCULATION FAILURE ==========\n")
print(result)


# Scenario 2: High contradiction

result = decide_next_step(
    calculation_passed,
    evidence_passed,
    high_contradiction
)

print("\n========== HIGH CONTRADICTION ==========\n")
print(result)


# Scenario 3: Evidence failed

result = decide_next_step(
    calculation_passed,
    evidence_failed,
    no_contradiction
)

print("\n========== EVIDENCE FAILURE ==========\n")
print(result)


# Scenario 4: Everything passed

result = decide_next_step(
    calculation_passed,
    evidence_passed,
    no_contradiction
)

print("\n========== ALL CHECKS PASSED ==========\n")
print(result)
