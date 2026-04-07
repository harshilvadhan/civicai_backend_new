from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ─── Enums (must match Person 3's AI output exactly) ─────────────────────────

class CategoryEnum(str, Enum):
    road        = "Road"
    garbage     = "Garbage"
    water       = "Water"
    electricity = "Electricity"
    drainage    = "Drainage"
    park        = "Park"
    safety      = "Public Safety"
    other       = "Other"

class UrgencyEnum(str, Enum):
    low    = "Low"
    medium = "Medium"
    high   = "High"

class StatusEnum(str, Enum):
    pending     = "Pending"
    assigned    = "Assigned"
    in_progress = "In Progress"
    resolved    = "Resolved"


# ─── Complaint Schemas ────────────────────────────────────────────────────────

class ComplaintCreate(BaseModel):
    """
    Person 1 (Frontend) sends this after user confirms the AI draft.
    AI fields come pre-filled from Person 3's engine output.
    """
    # Citizen inputs
    raw_input:          str
    location:           str
    image_url:          Optional[str] = None

    # AI fields — Person 3 guarantees these (strict Pydantic on their side too)
    category:           CategoryEnum
    urgency:            UrgencyEnum
    formal_complaint:   str
    suggested_department: str
    reasoning:          str


class ComplaintOut(BaseModel):
    """What we return to citizen on successful submission."""
    id:          str
    ticket_id:   str
    status:      StatusEnum
    category:    CategoryEnum
    urgency:     UrgencyEnum
    department:  str
    created_at:  datetime


class TrackResponse(BaseModel):
    """Full tracking view for a citizen."""
    ticket_id:          str
    status:             StatusEnum
    category:           CategoryEnum
    urgency:            UrgencyEnum
    department:         str
    formal_complaint:   str
    location:           str
    image_url:          Optional[str]
    reasoning:          str
    created_at:         datetime
    timeline:           List[dict]   # list of status_updates rows


# ─── Officer Schemas ──────────────────────────────────────────────────────────

class StatusUpdate(BaseModel):
    """Officer sends this to move a complaint forward."""
    status: StatusEnum
    note:   Optional[str] = ""


class OfficerLogin(BaseModel):
    email:    str
    password: str
