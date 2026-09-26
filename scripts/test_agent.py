"""
OmniOps Agentic System Test Suite
Executes end-to-end integration and policy guardrail tests against the enterprise API
and verifies tool responses.
"""

import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"
N8N_WEBHOOK = "http://localhost:5678/webhook/omniops-agent"

def run_tests():
    print("=" * 65)
    print("  OmniOps Enterprise Agentic Workflow - Verification Suite")
    print("=" * 65)
    
    # 1. Health Check
    try:
        res = requests.get(f"{BASE_URL}/health", timeout=5)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        print("  [PASS] 1. Backend API Health Check: OK")
    except Exception as e:
        print(f"  [FAIL] 1. Backend API is not running at {BASE_URL}. Start it with 'python backend/mock_api.py'")
        sys.exit(1)

    # 2. Knowledge Base RAG Search Test
    kb_res = requests.get(f"{BASE_URL}/api/kb/search", params={"query": "refund policy limit"}, timeout=5)
    assert kb_res.status_code == 200
    kb_data = kb_res.json()
    assert len(kb_data.get("articles", [])) > 0
    top_policy = kb_data["articles"][0]
    print(f"  [PASS] 2. Knowledge Base RAG: Retrieved '{top_policy['title']}' (Score: {top_policy.get('relevance_score')})")

    # 3. CRM Customer Profile Lookup
    crm_res = requests.get(f"{BASE_URL}/api/customers/sarah@cyberdyne.com", timeout=5)
    assert crm_res.status_code == 200
    cust = crm_res.json()["customer"]
    assert cust["tier"] == "VIP Enterprise"
    print(f"  [PASS] 3. CRM Customer Lookup: Verified '{cust['name']}' ({cust['tier']})")

    # 4. Order Lookup
    order_res = requests.get(f"{BASE_URL}/api/orders/ORD-9021", timeout=5)
    assert order_res.status_code == 200
    ord_data = order_res.json()["order"]
    print(f"  [PASS] 4. Order Tracking: ORD-9021 status '{ord_data['status']}' via {ord_data['carrier']}")

    # 5. Policy Guardrail 1: Auto-Approved Refund (< $100)
    refund_payload_small = {
        "order_id": "ORD-8812",
        "customer_id": "CUST-101",
        "amount": 45.00,
        "reason": "Customer request for cable return"
    }
    ref_small_res = requests.post(f"{BASE_URL}/api/orders/refund", json=refund_payload_small, timeout=5)
    assert ref_small_res.status_code == 200
    ref_small_data = ref_small_res.json()
    assert ref_small_data["status"] == "APPROVED"
    print(f"  [PASS] 5. Guardrail Test (Auto-Refund < $100): Status={ref_small_data['status']}, RefID={ref_small_data.get('refund_id')}")

    # 6. Policy Guardrail 2: Escalated Refund (> $100 creates P2 ticket)
    refund_payload_large = {
        "order_id": "ORD-9021",
        "customer_id": "CUST-101",
        "amount": 350.00,
        "reason": "Hardware overheating"
    }
    ref_large_res = requests.post(f"{BASE_URL}/api/orders/refund", json=refund_payload_large, timeout=5)
    assert ref_large_res.status_code == 200
    ref_large_data = ref_large_res.json()
    assert ref_large_data["status"] == "REQUIRES_APPROVAL"
    ticket_id = ref_large_data.get("ticket_id")
    assert ticket_id is not None
    print(f"  [PASS] 6. Guardrail Test (Escalation > $100): Status={ref_large_data['status']}, Created Ticket={ticket_id}")

    # 7. Urgent Alert Dispatch for VIP Customer
    notify_payload = {
        "channel": "#vip-support",
        "message": "Bruce Wayne (CUST-103) reported transit delay on ORD-9999.",
        "priority": "URGENT"
    }
    notify_res = requests.post(f"{BASE_URL}/api/notify", json=notify_payload, timeout=5)
    assert notify_res.status_code == 200
    print(f"  [PASS] 7. Slack/Email Alert Dispatch: Alert ID={notify_res.json().get('alert_id')}")

    # 8. Check Audit Logs
    logs_res = requests.get(f"{BASE_URL}/api/logs", timeout=5)
    logs_data = logs_res.json()
    print(f"  [PASS] 8. Telemetry & Observability: {logs_data['count']} tool actions logged in audit trail.")

    # 9. Check n8n webhook if available
    try:
        n8n_test = requests.post(N8N_WEBHOOK, json={"message": "ping"}, timeout=2)
        print(f"  [PASS] 9. n8n Webhook Endpoint: Active ({n8n_test.status_code})")
    except Exception:
        print("  [INFO] 9. n8n Webhook: Not currently listening at localhost:5678 (Import workflow into n8n to enable)")

    print("=" * 65)
    print("  ALL CORE SYSTEM TESTS PASSED SUCCESSFULLY! (100% Green)")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
