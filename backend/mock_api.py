"""
Enterprise OmniOps Mock API Server
Provides high-fidelity CRM, Order Management, Knowledge Base, Ticketing, and Notification
endpoints for the n8n Autonomous AI Agent.
"""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

app = FastAPI(
    title="OmniOps Enterprise Mock API",
    description="Backing service for n8n Agentic Workflow (CRM, Knowledge Base, Orders, Refunds, Tickets, Alerts)",
    version="1.0.0"
)

# Enable CORS for n8n and web dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage with seed enterprise data
CUSTOMERS_DB = {
    "sarah@cyberdyne.com": {
        "customer_id": "CUST-101",
        "name": "Sarah Connor",
        "email": "sarah@cyberdyne.com",
        "tier": "VIP Enterprise",
        "phone": "+1-555-0199",
        "account_balance": 240.00,
        "active_subscription": "Enterprise Cloud Fleet",
        "orders": ["ORD-9021", "ORD-8812"],
        "joined_date": "2024-03-15"
    },
    "CUST-101": {
        "customer_id": "CUST-101",
        "name": "Sarah Connor",
        "email": "sarah@cyberdyne.com",
        "tier": "VIP Enterprise",
        "phone": "+1-555-0199",
        "account_balance": 240.00,
        "active_subscription": "Enterprise Cloud Fleet",
        "orders": ["ORD-9021", "ORD-8812"],
        "joined_date": "2024-03-15"
    },
    "alex@gentek.org": {
        "customer_id": "CUST-102",
        "name": "Alex Mercer",
        "email": "alex@gentek.org",
        "tier": "Standard",
        "phone": "+1-555-0144",
        "account_balance": 0.00,
        "active_subscription": "Personal Pro",
        "orders": ["ORD-7744"],
        "joined_date": "2025-01-10"
    },
    "CUST-102": {
        "customer_id": "CUST-102",
        "name": "Alex Mercer",
        "email": "alex@gentek.org",
        "tier": "Standard",
        "phone": "+1-555-0144",
        "account_balance": 0.00,
        "active_subscription": "Personal Pro",
        "orders": ["ORD-7744"],
        "joined_date": "2025-01-10"
    },
    "bruce@wayneenterprises.com": {
        "customer_id": "CUST-103",
        "name": "Bruce Wayne",
        "email": "bruce@wayneenterprises.com",
        "tier": "Executive Platinum",
        "phone": "+1-555-0100",
        "account_balance": 14500.00,
        "active_subscription": "Global Mission Critical",
        "orders": ["ORD-9999"],
        "joined_date": "2023-11-01"
    },
    "CUST-103": {
        "customer_id": "CUST-103",
        "name": "Bruce Wayne",
        "email": "bruce@wayneenterprises.com",
        "tier": "Executive Platinum",
        "phone": "+1-555-0100",
        "account_balance": 14500.00,
        "active_subscription": "Global Mission Critical",
        "orders": ["ORD-9999"],
        "joined_date": "2023-11-01"
    }
}

ORDERS_DB = {
    "ORD-9021": {
        "order_id": "ORD-9021",
        "customer_id": "CUST-101",
        "item": "Quantum Server Unit Pro",
        "amount": 350.00,
        "status": "Delivered",
        "delivery_date": "2026-09-20",
        "carrier": "DHL Express",
        "tracking_code": "DHL-9912048",
        "return_eligible": True,
        "refund_issued": False
    },
    "ORD-8812": {
        "order_id": "ORD-8812",
        "customer_id": "CUST-101",
        "item": "Holographic Keyboard Cable",
        "amount": 45.00,
        "status": "Delivered",
        "delivery_date": "2026-09-24",
        "carrier": "USPS",
        "tracking_code": "US-4491028",
        "return_eligible": True,
        "refund_issued": False
    },
    "ORD-7744": {
        "order_id": "ORD-7744",
        "customer_id": "CUST-102",
        "item": "Cloud Storage Subscription (1-Year)",
        "amount": 89.00,
        "status": "Delivered",
        "delivery_date": "2026-06-10",
        "carrier": "Digital Delivery",
        "tracking_code": "DIG-8841",
        "return_eligible": False,
        "refund_issued": False
    },
    "ORD-9999": {
        "order_id": "ORD-9999",
        "customer_id": "CUST-103",
        "item": "Autonomous Security Satellite Link",
        "amount": 4200.00,
        "status": "In Transit",
        "delivery_date": "Estimated 2026-09-29",
        "carrier": "FedEx Priority",
        "tracking_code": "FX-88371902",
        "return_eligible": True,
        "refund_issued": False
    }
}

KB_ARTICLES = [
    {
        "article_id": "POL-101",
        "title": "Standard Refund & Return Policy",
        "category": "Refunds",
        "content": (
            "Customers may request a return or refund within 30 days of item delivery. "
            "Automated refund processing limit: Support agents may automatically issue refunds for orders "
            "up to $100 without manager sign-off. Any refund exceeding $100 requires creating an escalated "
            "approval ticket with priority P2. Digital subscriptions are non-refundable after 14 days."
        ),
        "tags": ["refund", "return", "policy", "threshold", "money", "100"]
    },
    {
        "article_id": "POL-102",
        "title": "VIP & Executive Customer SLA",
        "category": "VIP Support",
        "content": (
            "VIP Enterprise and Executive Platinum accounts have expedited SLA (1-hour response). "
            "For VIP customers reporting defective equipment, immediate replacement dispatch is authorized "
            "without waiting for defective item return. Automated Slack notification must be sent to the #vip-support "
            "channel whenever a VIP ticket is opened or escalated."
        ),
        "tags": ["vip", "sla", "priority", "replacement", "enterprise", "executive"]
    },
    {
        "article_id": "POL-103",
        "title": "Shipping Delays and Lost Package Protocol",
        "category": "Logistics",
        "content": (
            "If an order status is 'In Transit' and exceeds the estimated delivery date by 48 hours, "
            "the agent must query the carrier tracking API. If marked stalled or missing, issue a priority P1 "
            "investigation ticket and notify logistics."
        ),
        "tags": ["shipping", "transit", "carrier", "tracking", "lost", "delay"]
    },
    {
        "article_id": "POL-104",
        "title": "Subscription Cancellation & Grace Periods",
        "category": "Billing",
        "content": (
            "Subscription plans can be canceled anytime via the self-service dashboard or support. "
            "Annual plan cancellations requested within 14 days receive a 100% refund. Beyond 14 days, "
            "prorated credits are applied to the account balance."
        ),
        "tags": ["subscription", "cancel", "billing", "annual", "credit"]
    }
]

TICKETS_DB = []
NOTIFICATIONS_LOG = []
AUDIT_LOGS = []

def log_audit(action: str, details: Dict[str, Any]):
    log_entry = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "details": details
    }
    AUDIT_LOGS.insert(0, log_entry)
    # keep last 100 logs
    if len(AUDIT_LOGS) > 100:
        AUDIT_LOGS.pop()
    return log_entry

# Request Models
class RefundRequest(BaseModel):
    order_id: str
    customer_id: str
    amount: float
    reason: str

class TicketCreateRequest(BaseModel):
    customer_id: str
    subject: str
    description: str
    priority: str = Field(default="P2", description="P1 (Urgent), P2 (High), P3 (Normal)")
    department: str = Field(default="support", description="support, billing, logistics, executive")

class NotificationRequest(BaseModel):
    channel: str = Field(default="#support-alerts")
    message: str
    priority: str = "NORMAL"
    metadata: Optional[Dict[str, Any]] = None

# --- Endpoints ---

@app.get("/")
def root():
    return {
        "service": "Enterprise OmniOps Mock API",
        "status": "ONLINE",
        "endpoints": [
            "/api/customers/{identifier}",
            "/api/orders/{order_id}",
            "/api/orders/refund",
            "/api/kb/search?query=...",
            "/api/tickets",
            "/api/notify",
            "/api/logs"
        ]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# 1. CRM Customer Lookup
@app.get("/api/customers/{identifier}")
def get_customer(identifier: str):
    """Fetch customer profile by email or customer_id."""
    clean_id = identifier.strip().lower()
    # Search by key or email/id match
    found = None
    for key, cust in CUSTOMERS_DB.items():
        if key.lower() == clean_id or cust["customer_id"].lower() == clean_id or cust["email"].lower() == clean_id:
            found = cust
            break
            
    if not found:
        log_audit("CUSTOMER_LOOKUP_FAILED", {"identifier": identifier})
        raise HTTPException(status_code=404, detail=f"Customer '{identifier}' not found in CRM.")
    
    log_audit("CUSTOMER_LOOKUP_SUCCESS", {"customer_id": found["customer_id"], "tier": found["tier"]})
    return {"success": True, "customer": found}

# 2. Order Lookup
@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    """Fetch order details, shipping status, and return eligibility."""
    clean_id = order_id.strip().upper()
    order = ORDERS_DB.get(clean_id)
    if not order:
        log_audit("ORDER_LOOKUP_FAILED", {"order_id": order_id})
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    
    log_audit("ORDER_LOOKUP_SUCCESS", {"order_id": clean_id, "status": order["status"]})
    return {"success": True, "order": order}

# 3. Knowledge Base Semantic / Keyword Search
@app.get("/api/kb/search")
def search_kb(query: str = Query(..., description="User search query")):
    """Simulates RAG / vector retrieval against enterprise policies."""
    tokens = query.lower().split()
    results = []
    
    for article in KB_ARTICLES:
        score = 0
        text = (article["title"] + " " + article["content"] + " " + " ".join(article["tags"])).lower()
        for token in tokens:
            if len(token) > 2 and token in text:
                score += 1
                
        if score > 0:
            results.append({
                "article_id": article["article_id"],
                "title": article["title"],
                "category": article["category"],
                "content": article["content"],
                "relevance_score": round(score / (len(tokens) + 1), 2)
            })
            
    # Sort by relevance
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    log_audit("KB_SEARCH", {"query": query, "results_found": len(results)})
    return {
        "success": True,
        "query": query,
        "articles": results if results else KB_ARTICLES[:2]  # fallback top policies
    }

# 4. Conditional Order Refund Tool (Enforces Enterprise Policy Limits)
@app.post("/api/orders/refund")
def process_refund(payload: RefundRequest):
    """
    Automated refund processor with guardrails:
    - If amount <= $100: Automatically approved & processed.
    - If amount > $100: Policy requires manager escalation ticket.
    """
    clean_id = payload.order_id.strip().upper()
    order = ORDERS_DB.get(clean_id)
    
    if not order:
        raise HTTPException(status_code=404, detail=f"Order '{payload.order_id}' not found.")
        
    if order.get("refund_issued"):
        return {
            "success": False,
            "status": "ALREADY_REFUNDED",
            "message": f"Order {clean_id} has already been refunded previously."
        }
        
    if not order.get("return_eligible"):
        return {
            "success": False,
            "status": "INELIGIBLE",
            "message": f"Order {clean_id} is marked ineligible for return/refund per company policy."
        }
        
    # Policy evaluation
    if payload.amount <= 100.00:
        order["refund_issued"] = True
        refund_id = f"REF-{str(uuid.uuid4())[:6].upper()}"
        log_audit("REFUND_AUTO_APPROVED", {
            "order_id": clean_id,
            "amount": payload.amount,
            "refund_id": refund_id
        })
        return {
            "success": True,
            "status": "APPROVED",
            "refund_id": refund_id,
            "amount_refunded": payload.amount,
            "message": f"Instant refund of ${payload.amount:.2f} approved and issued to original payment method."
        }
    else:
        # Exceeds automated threshold -> Create high-priority escalation ticket
        ticket_id = f"TICK-{str(uuid.uuid4())[:6].upper()}"
        escalation_ticket = {
            "ticket_id": ticket_id,
            "customer_id": payload.customer_id,
            "subject": f"Refund Approval Request (${payload.amount:.2f}) for Order {clean_id}",
            "description": f"Customer requested refund of ${payload.amount:.2f}. Exceeds $100 auto-limit. Reason: {payload.reason}",
            "priority": "P2",
            "department": "billing",
            "status": "PENDING_MANAGER_APPROVAL",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        TICKETS_DB.append(escalation_ticket)
        log_audit("REFUND_ESCALATED", {
            "order_id": clean_id,
            "amount": payload.amount,
            "ticket_id": ticket_id
        })
        return {
            "success": True,
            "status": "REQUIRES_APPROVAL",
            "ticket_id": ticket_id,
            "message": (
                f"Refund amount of ${payload.amount:.2f} exceeds the automated $100 limit. "
                f"Escalation ticket {ticket_id} has been opened for Finance Manager review."
            )
        }

# 5. Ticketing System
@app.post("/api/tickets")
def create_ticket(payload: TicketCreateRequest):
    """Creates a new enterprise support or escalation ticket."""
    ticket_id = f"TICK-{str(uuid.uuid4())[:6].upper()}"
    ticket = {
        "ticket_id": ticket_id,
        "customer_id": payload.customer_id,
        "subject": payload.subject,
        "description": payload.description,
        "priority": payload.priority,
        "department": payload.department,
        "status": "OPEN",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    TICKETS_DB.append(ticket)
    log_audit("TICKET_CREATED", {"ticket_id": ticket_id, "priority": payload.priority, "subject": payload.subject})
    return {"success": True, "ticket": ticket}

@app.get("/api/tickets")
def list_tickets():
    return {"success": True, "total": len(TICKETS_DB), "tickets": TICKETS_DB}

# 6. Notifications & Alerts (Slack / Email Simulation)
@app.post("/api/notify")
def send_notification(payload: NotificationRequest):
    """Simulates dispatching an urgent alert to Slack or Ops team."""
    alert_id = f"ALT-{str(uuid.uuid4())[:6].upper()}"
    alert_record = {
        "alert_id": alert_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "channel": payload.channel,
        "message": payload.message,
        "priority": payload.priority,
        "metadata": payload.metadata or {}
    }
    NOTIFICATIONS_LOG.insert(0, alert_record)
    log_audit("NOTIFICATION_DISPATCHED", {"alert_id": alert_id, "channel": payload.channel, "priority": payload.priority})
    return {
        "success": True,
        "alert_id": alert_id,
        "dispatched_to": payload.channel,
        "message": "Alert dispatched to operations channel successfully."
    }

@app.get("/api/notifications")
def list_notifications():
    return {"success": True, "notifications": NOTIFICATIONS_LOG}

# 7. Audit & Agent Observability
@app.get("/api/logs")
def get_logs():
    """Live telemetry stream of the agent's tool decisions and API executions."""
    return {"success": True, "count": len(AUDIT_LOGS), "logs": AUDIT_LOGS}
