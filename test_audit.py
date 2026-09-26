from audit.logger import create_audit_entry, print_audit_trail

audit_log = []

audit_log.append(
    create_audit_entry(
        agent="Supply Chain Mapper",
        status="COMPLETED",
        reason="Supply chain structure extracted."
    )
)

audit_log.append(
    create_audit_entry(
        agent="Risk Engine",
        status="COMPLETED",
        reason="Risk score calculated: 40 MEDIUM"
    )
)

audit_log.append(
    create_audit_entry(
        agent="Calculation Verifier",
        status="PASS",
        reason="Risk calculation independently verified."
    )
)

audit_log.append(
    create_audit_entry(
        agent="Contradiction Hunter",
        status="FAIL",
        reason="HIGH severity contradiction detected."
    )
)

audit_log.append(
    create_audit_entry(
        agent="Orchestrator",
        status="REPLAN",
        reason="Independent evidence required."
    )
)

print_audit_trail(audit_log)
