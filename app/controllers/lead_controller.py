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
        data['email'] = data['email'].lower()

        if not  data['phone']:
            raise KeyError

        if not re.fullmatch("\([0-9]{2}\)[0-9]{5}\-[0-9]{4}", data['phone']):
            raise BadRequest

        new_lead = LeadModel(**data)

        current_app.db.session.add(new_lead)
        current_app.db.session.commit()


        return jsonify(new_lead), HTTPStatus.CREATED

    
    except IntegrityError as e :
        if isinstance(e.orig, UniqueViolation):
            err = str(e.orig)
            index = err.find("(")
            key_str = err[index+1:index+6]
            return { "error": f"{key_str} já existente"}, HTTPStatus.CONFLICT

    except BadRequest:
        return {"error": "Verique o formato do valor 'phone'. Formato aceito é: (XX)XXXXX-XXXX." }, HTTPStatus.BAD_REQUEST

    except KeyError as e:
        return {"error": f"Faltando a chave necessária: {e.args[0]}"}, HTTPStatus.BAD_REQUEST

    except TypeError as e:
        return {"error": f"Há chaves excessivas na requisição. As necessárias são: 'email', 'name', 'phone'."}, HTTPStatus.BAD_REQUEST





def read_leads() -> tuple:
    try:
        leads = LeadModel.query.all()

        def sorter(element):
            return element['visits']

        serializer = [
            {
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "creation_date": lead.creation_date,
            "last_visit": lead.last_visit,
            "visits": lead.visits
        } for lead in leads]

        serializer.sort(key=sorter, reverse=True)


        if not serializer:
            raise NotFound

        return {"leads": serializer}, HTTPStatus.OK
    
    except NotFound:
        return {"error": "O banco de dados está vazio"}, HTTPStatus.NOT_FOUND
    
    



def update_lead() -> tuple:
    try:
        data = request.get_json()

        lead = LeadModel.query.filter_by(email = data['email'].lower()).one_or_none()

        if not lead:
            raise NotFound

        setattr(lead, "visits", lead.visits + 1)
        setattr(lead, "last_visit", datetime.now())

        current_app.db.session.add(lead)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT
    
    except KeyError as e:
        return {"error": f"erro na chave: {e.args[0]}"}, HTTPStatus.BAD_REQUEST

    except AttributeError as e:
        return {"error": "Informe um valor do email em formato 'string'."}, HTTPStatus.BAD_REQUEST
    
    except NotFound:
        return {"error": "Lead não encontrado"}, HTTPStatus.NOT_FOUND




def erease_lead() -> None:
    try:
        data = request.get_json()

        lead_to_delete = LeadModel.query.filter_by(email = data['email'].lower()).one_or_none()
       
        if not lead_to_delete:
            raise NotFound

        current_app.db.session.delete(lead_to_delete)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT
    
    except KeyError as e:
        return {"error": f"erro na chave: {e.args[0]}"}, HTTPStatus.BAD_REQUEST

    except AttributeError as e:
        return {"error": "Informe um valor do email em formato 'string'."}
    
    except NotFound:
        return {"error": "Lead não encontrado"}, HTTPStatus.NOT_FOUND