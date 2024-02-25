import datetime
from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from modelos import Movimiento, MovimientoSchema, db
from vistas.utils import buscar_movimiento

movimiento_schema = MovimientoSchema()


class VistaMovimiento(Resource):

    @jwt_required()
    def put(self, id_movimiento):
        resultado_buscar_movimiento = buscar_movimiento(id_movimiento, current_user.id)
        if resultado_buscar_movimiento.error:
            return resultado_buscar_movimiento.error
        movimiento = resultado_buscar_movimiento.movimiento
        if not self.es_posible_eliminar_actualizar_movimiento(movimiento):
            return {'mensaje': 'No es posible actualizar este movimiento porque esta relacionado con una propiedad'}, 400
        movimiento_schema.load(request.json, session=db.session, instance=movimiento, partial=True)
        db.session.commit() 
        return movimiento_schema.dump(movimiento)
    
    @jwt_required()
    def delete(self, id_movimiento):
        resultado_buscar_movimiento = buscar_movimiento(id_movimiento, current_user.id)
        if resultado_buscar_movimiento.error:
            return resultado_buscar_movimiento.error
        movimiento = resultado_buscar_movimiento.movimiento
        if not self.es_posible_eliminar_actualizar_movimiento(movimiento):
            return {'mensaje': 'Para eliminar este movimiento, debe eliminar la reserva asociada'}, 400
        db.session.delete(movimiento)
        db.session.commit()
        return "", 204
    
    @jwt_required()
    def get(self, id_movimiento):
        resultado_buscar_movimiento = buscar_movimiento(id_movimiento, current_user.id)
        if resultado_buscar_movimiento.error:
            return resultado_buscar_movimiento.error
        return movimiento_schema.dump(resultado_buscar_movimiento.movimiento)
    
    def es_posible_eliminar_actualizar_movimiento(self, movimiento):
        if movimiento.concepto == Movimiento.CONCEPTO_RESERVA or movimiento.concepto == Movimiento.CONCEPTO_COMISION:
            return False
        if movimiento.fecha.month < datetime.datetime.now().month:
            return False
        return True
        
    
    
