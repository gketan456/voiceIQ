from langchain_core.tools import tool
from app.core.logging import get_logger

logger = get_logger(__name__)


@tool
def get_order_status(order_id: str) -> dict:
    """
    Look up the current status of a customer order.
    Use this when customer asks about their order, delivery, or shipment.
    
    Args:
        order_id: The order ID provided by the customer (e.g. ORD-123)
    """
    logger.info(f"Tool: get_order_status called with order_id={order_id}")

    mock_orders = {
        "ORD-123": {
            "order_id": "ORD-123",
            "status": "shipped",
            "carrier": "UPS",
            "tracking_number": "1Z999AA10123456784",
            "estimated_delivery": "Thursday, July 3",
            "items": ["Blue Running Shoes (Size 10)"],
        },
        "ORD-456": {
            "order_id": "ORD-456",
            "status": "processing",
            "carrier": None,
            "tracking_number": None,
            "estimated_delivery": "Monday, July 7",
            "items": ["Wireless Headphones"],
        },
    }

    if order_id not in mock_orders:
        return {"found": False, "error": f"Order {order_id} not found."}

    return {"found": True, **mock_orders[order_id]}

@tool
def search_knowledge_base(query: str) -> dict:
    """
    Search company knowledge base for answers about policies and products.
    Use this BEFORE answering any question about return policy, shipping,
    warranty, or business hours.
    
    Args:
        query: The customer's question to search for
    """
    logger.info(f"Tool: search_knowledge_base called with query='{query}'")

    knowledge = {
        "return": "We offer a 30-day hassle-free return policy. Items must be unused and in original packaging. Refunds process in 3-5 business days.",
        "shipping": "Standard shipping takes 5-7 business days and is free over $50. Express shipping is 2-3 days for $9.99.",
        "warranty": "All products include a 1-year manufacturer warranty covering defects. Electronics have a 2-year warranty.",
        "hours": "Customer support is available Monday-Friday 9AM-6PM EST and Saturday 10AM-4PM EST.",
    }

    query_lower = query.lower()
    for key, answer in knowledge.items():
        if key in query_lower:
            return {"found": True, "answer": answer}

    return {"found": False, "message": "No information found. Please escalate to human agent."}

@tool
def process_refund(order_id: str, reason: str) -> dict:
    """
    Process a refund for a customer order.
    Use this when customer explicitly asks for a refund.
    
    Args:
        order_id: The order to refund
        reason: Customer's reason for the refund
    """
    logger.info(f"Tool: process_refund called for order_id={order_id}")

    return {
        "success": True,
        "refund_reference": f"REF-{order_id}-001",
        "order_id": order_id,
        "timeline": "3-5 business days",
        "message": f"Refund approved for {order_id}. You'll receive it in 3-5 business days.",
    }

@tool
def create_support_ticket(issue: str, customer_contact: str) -> dict:
    """
    Create a support ticket for issues needing human follow-up.
    Use when customer needs a callback or issue needs investigation.
    
    Args:
        issue: Description of the customer's issue
        customer_contact: Customer's phone or email
    """
    logger.info(f"Tool: create_support_ticket issue='{issue[:30]}'")

    return {
        "success": True,
        "ticket_number": "TKT-00123",
        "issue": issue,
        "contact": customer_contact,
        "response_time": "within 24 hours",
        "message": "Ticket TKT-00123 created. We'll contact you within 24 hours.",
    }


@tool
def transfer_to_human(reason: str, summary: str) -> dict:
    """
    Transfer the conversation to a human agent.
    Use when customer asks for human, is very upset, or issue is too complex.
    Always provide a summary so customer doesn't repeat themselves.
    
    Args:
        reason: Why you're transferring
        summary: Full summary of the conversation so far
    """
    logger.info(f"Tool: transfer_to_human reason='{reason}'")

    return {
        "transfer_initiated": True,
        "wait_time": "2-3 minutes",
        "message": "Transferring you now. I've shared our conversation with the agent.",
    }

ALL_TOOLS = [
    get_order_status,
    search_knowledge_base,
    process_refund,
    create_support_ticket,
    transfer_to_human,
]


