import json
from pathlib import Path
from APP.agents.email_agent import send_email, get_all_emails
from APP.utils.gemini_connector import  generate_email_reply

from APP.agents.inventory_agent import check_inventory



# Define the path to the flow file
FLOW_FILE = Path("APP/data/flow.json")

def run_task_flow():
    if not FLOW_FILE.exists():
        print("❌ Flow file not found.")
        return []

    with open(FLOW_FILE, "r") as f:
        flow = json.load(f)

    results = []

    for step in flow:
        keyword = step.get("keyword")
        data = step.get("data", {})

        if keyword == "email":
            print("📧 Sending email...")
            result = send_email(
                subject=data["subject"],
                sender=data["sender"],
                reciver=data["reciver"],
                body=data["body"]
            )
            results.append({"keyword": keyword, "result": result.dict()})
        
    
        elif keyword == "email_reply":
            print("🤖 Generating email reply...")
            reply =  generate_email_reply(data["email_text"])
            results.append({"keyword": keyword, "reply": reply})
        elif keyword == "check_inventory":
            print("📦 Checking inventory...")
            
            product = data.get("product")
            quantity = data.get("quantity", 0)
            result = check_inventory(product, quantity)
            results.append({"keyword": keyword, "result": result})

        else:
            print(f"⚠️ Unknown task: {keyword}")
            results.append({"keyword": keyword, "error": "Unknown task"})

    return results
