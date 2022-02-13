from http import HTTPStatus
from flask import jsonify, request, current_app
from app.models.lead_model import LeadModel
from datetime import datetime
import re
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation




def create_lead() -> tuple:
    try:
        data: LeadModel = request.get_json()
        data['creation_date'] = datetime.now()
        data['last_visit'] = data['creation_date']

        print(request.args.get('email'))

        if not re.fullmatch("\([0-9]{2}\)[0-9]{5}\-[0-9]{4}", data['phone']):
            raise BadRequest

        new_lead = LeadModel(**data)

        current_app.db.session.add(new_lead)
        current_app.db.session.commit()


        return jsonify(new_lead), HTTPStatus.CREATED

    
    except IntegrityError as e :
        if isinstance(e.orig, UniqueViolation):
            return { "error": f"{e.orig} já existente"}, HTTPStatus.CONFLICT

    except BadRequest:
        return {"error": "Verique o formato do valor 'phone'. Formato aceito é: (XX)XXXXX-XXXX." }, HTTPStatus.BAD_REQUEST



def read_leads() -> tuple:
    try:
        leads = LeadModel.query.all()

        def sorter(element):
            return element['visits']

        serializer = sorted([{
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "creation_date": lead.creation_date,
            "last_visit": lead.last_visit,
            "visits": lead.visits
        } for lead in leads], key=sorter, reverse=True)

        if not serializer:
            raise NotFound

        return {"leads": serializer}
    
    except NotFound:
        return {"error": "The database is empty"}, HTTPStatus.NOT_FOUND

    



def update_lead(email) -> tuple:
    try:
        data = request.args
        key = "email"
        if key is not data:
            raise BadRequest
        lead = LeadModel.query.get(email)        

        setattr(lead, key, lead.visits + 1)

        current_app.db.session.add(lead)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    except BadRequest:
        return {"error": "XX"}, HTTPStatus.BAD_REQUEST
    
    except NotFound:
        return {"error": "Lead não encontrado"}, HTTPStatus.NOT_FOUND




def erease_lead(email) -> None:
    try:
        lead_to_delete = LeadModel.query.get(email)

        current_app.db.session.delete(lead_to_delete)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT
    
    except NotFound:
        return {"error": "Lead não encontrado"}, HTTPStatus.NOT_FOUND