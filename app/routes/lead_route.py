from flask import Blueprint
from app.controllers.lead_controller import create_lead, read_leads, update_lead, erease_lead



bp_leads = Blueprint("leads", __name__, url_prefix="/leads")


bp_leads.post("")(create_lead)
bp_leads.get("")(read_leads)
bp_leads.patch("/<email>")(update_lead)
bp_leads.delete("/<email>")(erease_lead)