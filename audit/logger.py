from datetime import datetime


def create_audit_entry(
    agent,
    status,
    input_data=None,
    output_data=None,
    reason=None
):
    return {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "status": status,
        "input": input_data,
        "output": output_data,
        "reason": reason
    }


def print_audit_trail(audit_log):

    print("\n")
    print("======================================")
    print("           AUDIT TRAIL")
    print("======================================")

    for entry in audit_log:

        print("\n--------------------------------------")

        print(f"Agent  : {entry['agent']}")
        print(f"Status : {entry['status']}")

        if entry.get("reason"):
            print(f"Reason : {entry['reason']}")

        print(f"Time   : {entry['timestamp']}")

    print("\n======================================")
    print("        END OF AUDIT TRAIL")
    print("======================================")
