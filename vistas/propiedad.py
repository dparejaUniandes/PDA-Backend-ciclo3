from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from sqlalchemy import or_, and_

from modelos import Propiedad, PropiedadSchema, db, TipoUsuario
from vistas.utils import buscar_propiedad

propiedad_schema = PropiedadSchema()

class VistaPropiedad(Resource):

    @jwt_required()
    def put(self, id_propiedad):
        if current_user.tipo == TipoUsuario.ADMINISTRADOR:
            propiedad = Propiedad.query.filter(or_(
                and_(Propiedad.id == id_propiedad,
                     Propiedad.id_administrador == current_user.id),
                and_(Propiedad.id == id_propiedad,
                     Propiedad.id_usuario == current_user.id))).first()

            for key, value in request.json.items():
                setattr(propiedad, key, value)
            db.session.commit()
            return propiedad_schema.dump(propiedad)

        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        for key, value in request.json.items():
            setattr(resultado_buscar_propiedad.propiedad, key, value)
        db.session.commit() 
        return propiedad_schema.dump(resultado_buscar_propiedad.propiedad)

    @jwt_required()
    def delete(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        Propiedad.query.filter(Propiedad.id == id_propiedad).delete()
        db.session.commit()
        return "", 204

    @jwt_required()
    def get(self, id_propiedad):
        if current_user.tipo == TipoUsuario.ADMINISTRADOR:
            return propiedad_schema.dump(Propiedad.query.filter(or_(
                and_(Propiedad.id == id_propiedad,
                     Propiedad.id_administrador == current_user.id),
                and_(Propiedad.id == id_propiedad,
                     Propiedad.id_usuario == current_user.id))).first()
            )

        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        return propiedad_schema.dump(resultado_buscar_propiedad.propiedad)
