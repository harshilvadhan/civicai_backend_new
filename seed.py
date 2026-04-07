"""
Run this once to seed 10 sample complaints for demo:
    python scripts/seed.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from supabase import create_client
from config import settings
from datetime import datetime, timedelta
import uuid, random

sb = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

SAMPLES = [
    {"category": "Road",        "urgency": "High",   "location": "SV Road, Borivali West",      "department": "Roads Dept",         "raw_input": "Giant pothole near the bus stop causing accidents"},
    {"category": "Garbage",     "urgency": "Medium", "location": "Gorai Creek Area, Borivali",  "department": "Sanitation",         "raw_input": "Garbage overflowing for 3 days near the creek"},
    {"category": "Drainage",    "urgency": "High",   "location": "Eksar Metro Station",         "department": "Drainage Dept",      "raw_input": "Drainage blocked, flooding on platform road"},
    {"category": "Electricity", "urgency": "Low",    "location": "Shimpoli Rd, Borivali West",  "department": "Electricity Dept",   "raw_input": "Streetlight not working since last week"},
    {"category": "Water",       "urgency": "High",   "location": "IC Colony, Borivali West",    "department": "Water Dept",         "raw_input": "Water pipe burst outside building, wastage"},
    {"category": "Park",        "urgency": "Low",    "location": "Poisar Gymkhana, Kandivali",  "department": "Parks Dept",         "raw_input": "Park benches broken, children cannot sit"},
    {"category": "Road",        "urgency": "Medium", "location": "LT Road, Borivali East",      "department": "Roads Dept",         "raw_input": "Road divider damaged, dangerous for two-wheelers"},
    {"category": "Garbage",     "urgency": "High",   "location": "Dahisar Check Naka",          "department": "Sanitation",         "raw_input": "Illegal dumping on footpath blocking pedestrians"},
    {"category": "Public Safety","urgency":"High",   "location": "Kandivali Station East",      "department": "Public Safety Dept", "raw_input": "Street light completely out near dark lane, safety risk"},
    {"category": "Water",       "urgency": "Medium", "location": "Eksar Village, Borivali",     "department": "Water Dept",         "raw_input": "No water supply for 2 days in the area"},
]

STATUSES = ["Pending", "Assigned", "In Progress", "Resolved"]

def short_id():
    return str(uuid.uuid4()).upper()[:4]

for i, s in enumerate(SAMPLES):
    ticket_id = f"CMP-DEMO{i+1:02d}"
    status    = random.choice(STATUSES)
    created   = (datetime.utcnow() - timedelta(hours=random.randint(1, 48))).isoformat()

    row = {
        "ticket_id":        ticket_id,
        "raw_input":        s["raw_input"],
        "location":         s["location"],
        "image_url":        None,
        "category":         s["category"],
        "urgency":          s["urgency"],
        "formal_complaint": f"This is to formally bring to your attention that {s['raw_input'].lower()}. "
                            f"The issue is located at {s['location']} and requires immediate attention. "
                            f"Kindly depute the concerned team at the earliest.",
        "department":       s["department"],
        "reasoning":        f"Classified as {s['category']} based on citizen description.",
        "status":           status,
        "created_at":       created,
    }

    res = sb.table("complaints").insert(row).execute()
    complaint_id = res.data[0]["id"]

    # Seed initial status update
    sb.table("status_updates").insert({
        "complaint_id": complaint_id,
        "status":       "Pending",
        "note":         "Complaint submitted by citizen.",
        "updated_at":   created,
    }).execute()

    if status in ["Assigned", "In Progress", "Resolved"]:
        sb.table("status_updates").insert({
            "complaint_id": complaint_id,
            "status":       "Assigned",
            "note":         "Assigned to field team.",
        }).execute()

    if status in ["In Progress", "Resolved"]:
        sb.table("status_updates").insert({
            "complaint_id": complaint_id,
            "status":       "In Progress",
            "note":         "Team dispatched to location.",
        }).execute()

    if status == "Resolved":
        sb.table("status_updates").insert({
            "complaint_id": complaint_id,
            "status":       "Resolved",
            "note":         "Issue resolved and verified.",
        }).execute()

    print(f"✅ Seeded {ticket_id} — {s['category']} ({s['urgency']}) — {status}")

print("\n🎉 10 sample complaints seeded successfully!")
