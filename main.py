from agents.supply_chain_mapper import supply_chain_mapper
from tools.risk_engine import calculate_risk
from agents.action_planner import create_action_plan

from verification.evidence_store import get_demo_evidence
from verification.calculation_verifier import verify_risk
from verification.evidence_verifier import verify_evidence
from verification.contradiction_hunter import detect_contradictions

from orchestration.orchestrator import decide_next_step
from agents.self_correction import self_correct

from contradiction_resolver import resolve_contradiction
from independent_evidence import collect_independent_evidence

from audit.logger import create_audit_entry


def extract_claim(value):
    """
    Convert different contradiction claim formats into a simple string.
    """

    if isinstance(value, dict):
        return (
            value.get("claim")
            or value.get("text")
            or value.get("statement")
            or ""
        )

    if isinstance(value, str):
        return value

    return str(value)


def normalize_contradiction(first_contradiction, affected_claims=None):
    """
    Convert different contradiction formats into:

    {
        "claim1": "...",
        "claim2": "..."
    }
    """

    def extract_claim(value):

        if isinstance(value, dict):
            return (
                value.get("claim")
                or value.get("text")
                or value.get("statement")
                or ""
            )

        if isinstance(value, str):
            return value

        return str(value)


    # Format 1: claims
    if isinstance(first_contradiction, dict):

        if "claims" in first_contradiction:

            claims = first_contradiction["claims"]

            if isinstance(claims, list) and len(claims) >= 2:

                return {
                    "claim1": extract_claim(claims[0]),
                    "claim2": extract_claim(claims[1])
                }


        # Format 2: claims_in_conflict
        if "claims_in_conflict" in first_contradiction:

            claims = first_contradiction["claims_in_conflict"]

            if isinstance(claims, list) and len(claims) >= 2:

                return {
                    "claim1": extract_claim(claims[0]),
                    "claim2": extract_claim(claims[1])
                }


        # Format 3: claim_1 / claim_2
        if (
            "claim_1" in first_contradiction
            and "claim_2" in first_contradiction
        ):

            return {
                "claim1": extract_claim(
                    first_contradiction["claim_1"]
                ),
                "claim2": extract_claim(
                    first_contradiction["claim_2"]
                )
            }


        # Format 4: claim_a / claim_b
        if (
            "claim_a" in first_contradiction
            and "claim_b" in first_contradiction
        ):

            return {
                "claim1": extract_claim(
                    first_contradiction["claim_a"]
                ),
                "claim2": extract_claim(
                    first_contradiction["claim_b"]
                )
            }


        # Format 5: claim1 / claim2
        if (
            "claim1" in first_contradiction
            and "claim2" in first_contradiction
        ):

            return {
                "claim1": extract_claim(
                    first_contradiction["claim1"]
                ),
                "claim2": extract_claim(
                    first_contradiction["claim2"]
                )
            }


    # Format 6:
    # contradictions itself is a string,
    # so use affected_claims as the real claims.
    if affected_claims:

        if (
            isinstance(affected_claims, list)
            and len(affected_claims) >= 2
        ):

            return {
                "claim1": extract_claim(affected_claims[0]),
                "claim2": extract_claim(affected_claims[1])
            }


    return {
        "claim1": "",
        "claim2": ""
    }

def run_pipeline(disruption: str):

    audit_log = []

    print("\n======================================")
    print("   MULTI-AGENT VERIFICATION ENGINE")
    print("======================================")


    # ==========================================================
    # 1. SUPPLY CHAIN MAPPING
    # ==========================================================

    print("\n[1] SUPPLY CHAIN MAPPING")

    mapping_result = supply_chain_mapper(disruption)

    if not mapping_result["success"]:

        return {
            "status": "FAILED",
            "stage": "mapping",
            "error": mapping_result.get("error")
        }

    supply_chain = mapping_result["data"]

    print(supply_chain)

    audit_log.append(
        create_audit_entry(
            agent="Supply Chain Mapper",
            status="COMPLETED",
            output_data=supply_chain,
            reason="Supply chain structure extracted."
        )
    )


    # ==========================================================
    # 2. RISK CALCULATION
    # ==========================================================

    print("\n[2] RISK CALCULATION")

    risk = calculate_risk(supply_chain)

    print(risk)


    # ==========================================================
    # 3. ACTION PLANNING
    # ==========================================================

    print("\n[3] ACTION PLANNING")

    action_plan_result = create_action_plan(
        supply_chain,
        risk
    )

    print("\nDEBUG ACTION PLAN RESULT:")
    print(action_plan_result)

    if not action_plan_result["success"]:

        return {
            "status": "FAILED",
            "stage": "action_planning",
            "error": action_plan_result.get(
                "error",
                "Unknown action planner error"
            ),
            "raw_response": action_plan_result.get(
                "raw_response"
            )
        }

    action_plan = action_plan_result["plan"]

    print(action_plan)


    # ==========================================================
    # 4. CALCULATION VERIFICATION
    # ==========================================================

    print("\n[4] CALCULATION VERIFICATION")

    calculation_verification = verify_risk(
        supply_chain,
        risk
    )

    print(calculation_verification)


    # ==========================================================
    # 5. EVIDENCE VERIFICATION
    # ==========================================================

    print("\n[5] EVIDENCE VERIFICATION")

    evidence_verification = verify_evidence(
        supply_chain,
        risk,
        action_plan
    )

    print(evidence_verification)


    # ==========================================================
    # 6. EVIDENCE COLLECTION
    # ==========================================================

    print("\n[6] EVIDENCE COLLECTION")

    evidence = get_demo_evidence()

    for item in evidence:
        print(item)


    # ==========================================================
    # 7. CONTRADICTION DETECTION
    # ==========================================================

    print("\n[7] CONTRADICTION DETECTION")

    contradiction_result = detect_contradictions(
        evidence
    )

    print(contradiction_result)


    # ==========================================================
    # 8. ORCHESTRATOR DECISION
    # ==========================================================

    print("\n[8] ORCHESTRATOR DECISION")

    decision = decide_next_step(
        calculation_verification,
        evidence_verification,
        contradiction_result
    )

    print(decision)


    # ==========================================================
    # 9. SELF-CORRECTION
    # ==========================================================

    if decision["decision"] == "REPLAN":

        print("\n[9] SELF-CORRECTION")

        correction = self_correct(
            supply_chain,
            risk,
            action_plan,
            evidence_verification
        )

        print(correction)

        if correction.get("success"):

            action_plan = correction["corrected_plan"]


            # ==================================================
            # 10. RE-VERIFICATION
            # ==================================================

            print("\n[10] RE-VERIFICATION")

            evidence_verification = verify_evidence(
                supply_chain,
                risk,
                action_plan
            )

            print(evidence_verification)


            # ==================================================
            # 11. CONTRADICTION RE-CHECK
            # ==================================================

            print("\n[11] CONTRADICTION RE-CHECK")

            contradiction_result = detect_contradictions(
                evidence
            )

            print(contradiction_result)


    # ==========================================================
    # 12. CONTRADICTION PREPARATION / NORMALIZATION
    # ==========================================================

    print("\n[12] CONTRADICTION RESOLUTION")

    contradiction = None
    independent_evidence = []

    contradiction_detected = (
        contradiction_result.get("result", {})
        .get("contradiction_detected", False)
    )


    if contradiction_detected:

        contradictions = (
            contradiction_result
            .get("result", {})
            .get("contradictions", [])
        )

        if contradictions:

            first_contradiction = contradictions[0]

            contradiction = normalize_contradiction(
                  first_contradiction,
                  contradiction_result
                  .get("result", {})
                  .get("affected_claims", [])
            )

            print("\nContradiction Passed to Resolver:")
            print(contradiction)


            # ==============================================
            # Independent Evidence
            # ==============================================

            independent_evidence = collect_independent_evidence(
                contradiction
            )

            print("\nIndependent Evidence Collected:")

            for item in independent_evidence:
                print(item)

        else:

            print(
                "Contradiction was detected but no contradiction "
                "details were provided."
            )

    else:

        print("No contradiction detected.")


    # ==========================================================
    # 13. CONTRADICTION RESOLUTION
    # ==========================================================

    print("\n[13] CONTRADICTION RESOLUTION")

    if contradiction_detected and contradiction:

        resolution_result = resolve_contradiction(
            contradiction,
            independent_evidence
        )

        print(resolution_result)

    else:

        resolution_result = {
            "resolved": True,
            "status": "NO_CONTRADICTION",
            "reason": "No contradiction detected."
        }

        print(resolution_result)


    # ==========================================================
    # 14. FINAL DECISION
    # ==========================================================

    print("\n[14] FINAL DECISION")

    if contradiction_detected:

        if resolution_result.get("resolved"):

            final_decision = {
                "decision": "PROCEED",
                "next_action": "continue_with_verified_plan",
                "reason": (
                    "The contradiction was resolved using "
                    "independent evidence."
                )
            }

        else:

            final_decision = {
                "decision": "REPLAN",
                "next_action": "collect_more_independent_evidence",
                "reason": (
                    "The contradiction remains unresolved. "
                    "More independent evidence is required."
                )
            }

    else:

        final_decision = {
            "decision": "PROCEED",
            "next_action": "continue_with_verified_plan",
            "reason": "No contradiction was detected."
        }

    print(final_decision)


    # ==========================================================
    # FINAL RESULT
    # ==========================================================

    return {

        "supply_chain": supply_chain,

        "risk": risk,

        "action_plan": action_plan,

        "calculation_verification":
            calculation_verification,

        "evidence_verification":
            evidence_verification,

        "contradiction_result":
            contradiction_result,

        "resolution_result":
            resolution_result,

        "decision":
            final_decision
    }


# ==============================================================
# LOCAL TEST
# ==============================================================

if __name__ == "__main__":

    disruption = """
    Severe flooding has disrupted a component supplier
    in Chennai. Production and transportation may be affected.
    """

    result = run_pipeline(disruption)

    print("\n======================================")
    print("           FINAL RESULT")
    print("======================================")

    print(result)
