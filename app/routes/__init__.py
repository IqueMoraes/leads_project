
from flask import Flask
from app.routes.lead_route import bp_leads


def init_app(app: Flask):

    app.register_blueprint(bp_leads)