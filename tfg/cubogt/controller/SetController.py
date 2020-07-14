from cubogt.models import Set


def get_equipo_ganador(set_partido):
	deporte = set_partido.partido.grupo.fase.torneo.deporte
	partido = set_partido.partido
	ganador = None
	if deporte.juego:
		if set_partido.juegos_local > set_partido.juegos_visitante:
			ganador = partido.equipo_local
		elif set_partido.juegos_local < set_partido.juegos_visitante:
			ganador = partido.equipo_visitante
	else:
		if set_partido.puntos_local > set_partido.puntos_visitante:
			ganador = partido.equipo_local
		elif set_partido.puntos_local < set_partido.puntos_visitante:
			ganador = partido.equipo_visitante

	return ganador


def set_comprobar_nuevo(partido):
	set_maximos = partido.grupo.fase.numero_sets
	n_set_local = Set.objects.filter(partido=partido, ganador=partido.equipo_local).count()
	n_set_visitante = Set.objects.filter(partido=partido, ganador=partido.equipo_visitante).count()
	if n_set_local > (set_maximos / 2) or n_set_visitante > (set_maximos / 2):
		return False
	else:
		return True
