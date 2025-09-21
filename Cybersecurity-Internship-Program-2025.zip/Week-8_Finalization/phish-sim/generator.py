import random
import uuid
from datetime import datetime, timedelta

COMPANIES = ["AcmeCorp", "NorthBridge", "Atlas HR", "Everly Services"]
TYPES = ["Security Alert", "Invoice", "Password Reset", "HR Notification", "Package Delivery"]
ACTIONS = [
    "click to review your account",
    "download the attached invoice",
    "reset your password using the link",
    "confirm your attendance",
    "track your package"
]
LINK_PLACEHOLDER = "[LINK_PLACEHOLDER]"

def make_mock_message():
    company = random.choice(COMPANIES)
    typ = random.choice(TYPES)
    action = random.choice(ACTIONS)
    days = random.randint(1, 7)
    deadline = (datetime.now() + timedelta(days=days)).strftime("%b %d, %Y")
    amount = f"{random.randint(10, 999)}.00"
    msg_id = str(uuid.uuid4())
    subject = f"{company} — {typ}"
    body = (
        f"Hello,\n\n"
        f"This is a {typ.lower()} from {company}. Please {action} by {deadline}. "
        f"If you have questions, contact {company} Support.\n\n"
        f"Details:\n"
        f"- Reference: {msg_id}\n"
        f"- Amount (if applicable): ${amount}\n\n"
        f"{LINK_PLACEHOLDER}\n\n"
        f"Thanks,\nSecurity Team"
    )
    meta = {"company": company, "type": typ, "action": action, "deadline": deadline, "msg_id": msg_id}
    return {"id": msg_id, "subject": subject, "body": body, "meta": meta}
