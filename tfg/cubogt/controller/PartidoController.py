from . import CampoController, ClasificacionController, FaseController
from ..models import Partido, Grupo
from ..static.constantes import LIGA, JUGANDO, ESPERA, TERMINADO


def crear_calendario(fase):
	if fase.tipo_fase is LIGA:
		crear_liga(fase)
	else:
		# TODO crear_eliminatoria(fase)
		pass


def crear_liga(fase):
	grupo_list = Grupo.objects.filter(fase=fase)
	for grupo in grupo_list:
		rondas = calcular_rondas(fase, grupo)
		equipos_list = grupo.equipos.all()
		calendario_grupo_list = crear_lista_partidos(list(equipos_list), rondas)
		crear_partido_lista(grupo, calendario_grupo_list, fase.doble_partido)


def calcular_rondas(fase, grupo):
	n_equipos = grupo.equipos.count()
	if (n_equipos % 2) == 0:
		rondas = n_equipos - 1
	else:
		rondas = n_equipos
	if fase.doble_partido:
		rondas *= 2
	return rondas


def crear_lista_partidos(teams, rounds):
	"""Devuelve una lista de listas de jornadas, dentro de esa lista de jornadas hay una tupla con los enfrentamientos
	equipo_local vs equipo_visitante"""
	if len(teams) % 2:
		teams.append(None)

	schedule = []
	for turn in range(rounds):
		pairings = []
		for i in range(int(len(teams) / 2)):
			pairings.append((teams[i], teams[len(teams) - i - 1]))
		teams.insert(1, teams.pop())
		schedule.append(pairings)

	return schedule


def crear_partido_lista(grupo, calendario_list, doble_partido):
	for jornada in range(1, len(calendario_list) + 1):
		for enfrentamiento in calendario_list[jornada - 1]:
			if enfrentamiento[0] and enfrentamiento[1]:
				if doble_partido and jornada > (len(calendario_list) / 2):
					Partido.objects.create(grupo=grupo, equipo_local=enfrentamiento[1],
										   equipo_visitante=enfrentamiento[0],
										   jornada=jornada)
				else:
					Partido.objects.create(grupo=grupo, equipo_local=enfrentamiento[0],
										   equipo_visitante=enfrentamiento[1],
										   jornada=jornada)


def get_partidos_grupo_list(grupo):
	partidos = Partido.objects.filter(grupo=grupo)
	return partidos


def get_partidos_jornadas_grupo(grupo):
	jornadas_list = []
	jornadas = calcular_rondas(grupo.fase, grupo)
	for n_jornada in range(1, jornadas + 1):
		partidos_jornada_list = Partido.objects.filter(grupo=grupo, jornada=n_jornada)
		aux = [n_jornada, partidos_jornada_list]
		jornadas_list.append(aux)
	return jornadas_list


def get_partidos_jugando_list(fase):
	partidos_jugando = Partido.objects.filter(grupo__fase=fase, estado=JUGANDO)
	return partidos_jugando


def get_partidos_espera_list(fase):
	partidos_espera = Partido.objects.filter(grupo__fase=fase, estado=ESPERA)
	return partidos_espera


def get_partidos_no_terminados_list(fase):
	partidos_espera = Partido.objects.filter(grupo__fase=fase, estado__lt=TERMINADO)
	return partidos_espera


def get_partidos_espera_equipos_no_jugando_list(fase):
	"""Devuelve una lista con los partidos que se pueden jugar sin que coincida alguno que este en juego"""
	partidos_espera_list = get_partidos_espera_list(fase)
	partidos_jugando_list = get_partidos_jugando_list(fase)
	equipos_jugando = []
	for partido_jugando in partidos_jugando_list:
		equipos_jugando.append(partido_jugando.equipo_local)
		equipos_jugando.append(partido_jugando.equipo_visitante)
	partidos_espera_equipos_no_jugando_list = partidos_espera_list.exclude(equipo_local__in=equipos_jugando) \
		.exclude(equipo_visitante__in=equipos_jugando)
	return partidos_espera_equipos_no_jugando_list


def get_partidos_con_campos_para_forzar(fase):
	"""Devuelve una lista de listas con los partidos que se pueden jugar en los campos disponibles
	[[partido,[campo,campo]],[partido,[campo]],[partido,[]]...]"""
	partidos_espera_list = get_partidos_espera_list(fase)
	campos_para_forzar_list = CampoController.get_campos_para_forzar(fase)
	partido_campo = []
	for x in range(0, len(partidos_espera_list)):
		aux = [partidos_espera_list[x], campos_para_forzar_list[x]]
		partido_campo.append(aux)
	return partido_campo


def set_partido_espera(partido):
	partido.estado = ESPERA
	partido.arbitro = None
	partido.campo = None
	partido.save()


def set_partido_jugar(partido, campo, arbitro=None):
	partido.estado = JUGANDO
	partido.campo = campo
	partido.arbitro = arbitro
	partido.save()


def set_partido_terminar(partido):
	partido.estado = TERMINADO
	partido.ganador = get_equipo_ganador(partido)
	partido.save()


def get_equipo_ganador(partido):
	ganador = None
	if partido.estado == TERMINADO:
		deporte = partido.grupo.fase.torneo.deporte
		if deporte.set:
			resultado_local = partido.get_numero_sets_local()
			resultado_visitante = partido.get_numero_sets_visitante()
		else:
			resultado_local = partido.resultado_local
			resultado_visitante = partido.resultado_visitante
		# Compruebo resultados
		if resultado_local > resultado_visitante:
			ganador = partido.equipo_local
		elif resultado_local < resultado_visitante:
			ganador = partido.equipo_visitante

	return ganador


def partido_posponer(fase, partido):
	arbitro = partido.arbitro
	campo = partido.campo
	set_partido_espera(partido)
	campo_list = CampoController.get_campo_fase_list(fase)
	if campo in campo_list:
		partidos_espera_list = get_partidos_espera_equipos_no_jugando_list(fase).exclude(pk=partido.id)
		if partidos_espera_list:
			partido_siguiente = partidos_espera_list.first()
			set_partido_jugar(partido_siguiente, campo, arbitro)
		else:  # No se puede posponer el partido
			set_partido_jugar(partido, campo, arbitro)


def partido_forzar(fase, partido, campo):
	partido_reemplazar = Partido.objects.get(grupo__fase=fase, campo=campo, estado=JUGANDO)
	arbitro = partido_reemplazar.arbitro
	set_partido_espera(partido_reemplazar)
	set_partido_jugar(partido, campo, arbitro)


def partido_terminar(partido):
	# Cambiar estado
	set_partido_terminar(partido)
	#  Actualizar clasificacion
	ClasificacionController.actualizar_clasificacion(partido)
	# Iniciar siguiente partido
	arbitro = get_equipo_ganador(partido)
	if not arbitro:
		n_equipo_local_arbitro = Partido.objects.filter(arbitro=partido.equipo_local).count()
		n_equipo_visitante_arbitro = Partido.objects.filter(arbitro=partido.equipo_visitante).count()
		if n_equipo_local_arbitro <= n_equipo_visitante_arbitro:
			arbitro = partido.equipo_local
		else:
			arbitro = n_equipo_visitante_arbitro
	fase = partido.grupo.fase
	FaseController.iniciar_siguiente_partido(fase, arbitro)
