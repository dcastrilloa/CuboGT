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
