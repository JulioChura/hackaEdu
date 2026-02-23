from contenido.models import Lectura
from .models import Sesion


def get_lectura_by_id(lectura_id):
    return Lectura.objects.filter(id=lectura_id).first()


def get_session_by_id_user(session_id, user):
    return Sesion.objects.filter(id=session_id, usuario=user).first()


def get_active_session(user, lectura):
    return Sesion.objects.filter(
        usuario=user,
        lectura=lectura,
        estado__in=['INICIADA', 'EN_PROGRESO']
    ).order_by('-fecha').first()


def get_completed_session(user, lectura):
    return Sesion.objects.filter(
        usuario=user,
        lectura=lectura,
        estado='COMPLETADA'
    ).order_by('-fecha').first()


def get_latest_session_by_lectura(user, lectura_id):
    return Sesion.objects.filter(
        usuario=user,
        lectura_id=lectura_id
    ).order_by('-fecha').first()
