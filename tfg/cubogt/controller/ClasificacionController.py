from django.db.models import Q, Count, Sum
from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import FaseForm, FasePuntoForm, FaseSetForm, FaseEquipoForm
from . import CampoController
from ..controller import GrupoController
from ..models import Torneo, Fase, Equipo, Partido, Campo, Grupo, Clasificacion, Set, Juego, Ascenso
from ..static.constantes import LIGA, ELIMINATORIA, JUGANDO, ESPERA, TERMINADO


def actualizar_clasificacion(partido):
	if partido.estado == TERMINADO:
		grupo = partido.grupo
		actualizar_clasificacion_equipo(partido.equipo_local, grupo)
		actualizar_clasificacion_equipo(partido.equipo_visitante, grupo)


def actualizar_clasificacion_equipo(equipo, grupo):
	deporte = grupo.fase.torneo.deporte
	clasificacion = Clasificacion.objects.get(grupo=grupo, equipo=equipo)
	# Partidos
	n_partidos_local = Partido.objects.filter(grupo=grupo, equipo_local=equipo, estado=TERMINADO).count()
	n_partidos_visitante = Partido.objects.filter(grupo=grupo, equipo_visitante=equipo, estado=TERMINADO).count()
	n_partidos_juegados = n_partidos_local + n_partidos_visitante
	clasificacion.partidos_jugados = n_partidos_juegados

	n_partidos_ganado = Partido.objects.filter(grupo=grupo, ganador=equipo, estado=TERMINADO).count()
	clasificacion.partidos_ganados = n_partidos_ganado
	n_partidos_empatado = Partido.objects.filter(Q(equipo_local=equipo) | Q(equipo_visitante=equipo),
												 grupo=grupo, ganador=None, estado=TERMINADO).count()
	clasificacion.partidos_empatados = n_partidos_empatado
	clasificacion.partidos_perdidos = n_partidos_juegados - n_partidos_ganado - n_partidos_empatado

	# Sets:
	if deporte.set:
		n_sets_totales = Set.objects.filter(Q(partido__equipo_local=equipo) | Q(partido__equipo_visitante=equipo),
											partido__grupo=grupo, partido__estado=TERMINADO).count()
		n_sets_favor = Set.objects.filter(partido__grupo=grupo, ganador=equipo, partido__estado=TERMINADO).count()
		clasificacion.sets_favor = n_sets_favor
		clasificacion.sets_contra = n_sets_totales - n_sets_favor

		# Puntos de set: Voley, barminton, pinpong
		query_set_local = Set.objects.filter(partido__equipo_local=equipo, partido__grupo=grupo,
											 partido__estado=TERMINADO)
		query_set_visitante = Set.objects.filter(partido__equipo_visitante=equipo, partido__grupo=grupo,
												 partido__estado=TERMINADO)
		if deporte.punto:
			n_puntos_favor_local = query_set_local.aggregate(sumatorio=Sum('puntos_local'))
			n_puntos_favor_visitante = query_set_visitante.aggregate(sumatorio=Sum('puntos_visitante'))
			if not n_puntos_favor_local['sumatorio']:
				n_puntos_favor_local['sumatorio'] = 0
			if not n_puntos_favor_visitante['sumatorio']:
				n_puntos_favor_visitante['sumatorio'] = 0
			clasificacion.puntos_favor = n_puntos_favor_local['sumatorio'] + n_puntos_favor_visitante['sumatorio']

			n_puntos_contr_local = query_set_local.aggregate(sumatorio=Sum('puntos_visitante'))
			n_puntos_contra_visitante = query_set_visitante.aggregate(sumatorio=Sum('puntos_local'))
			if not n_puntos_contr_local['sumatorio']:
				n_puntos_contr_local['sumatorio'] = 0
			if not n_puntos_contra_visitante['sumatorio']:
				n_puntos_contra_visitante['sumatorio'] = 0
			clasificacion.puntos_contra = n_puntos_contr_local['sumatorio'] + n_puntos_contra_visitante['sumatorio']

		# Juegos
		else:
			n_juegos_favor_local = query_set_local.aggregate(sumatorio=Sum('juegos_local'))
			n_juegos_favor_visitante = query_set_visitante.aggregate(sumatorio=Sum('juegos_visitante'))
			if not n_juegos_favor_local['sumatorio']:
				n_juegos_favor_local['sumatorio'] = 0
			if not n_juegos_favor_visitante['sumatorio']:
				n_juegos_favor_visitante['sumatorio'] = 0
			clasificacion.puntos_favor = n_juegos_favor_local['sumatorio'] + n_juegos_favor_visitante['sumatorio']

			n_juegos_contr_local = query_set_local.aggregate(sumatorio=Sum('juegos_visitante'))
			n_juegos_contra_visitante = query_set_visitante.aggregate(sumatorio=Sum('juegos_local'))
			if not n_juegos_contr_local['sumatorio']:
				n_juegos_contr_local['sumatorio'] = 0
			if not n_juegos_contra_visitante['sumatorio']:
				n_juegos_contra_visitante['sumatorio'] = 0
			clasificacion.puntos_contra = n_juegos_contr_local['sumatorio'] + n_juegos_contra_visitante['sumatorio']

	# Resultado
	else:
		query_partido_local = Partido.objects.filter(equipo_local=equipo, grupo=grupo, estado=TERMINADO)
		query_partido_visitante = Partido.objects.filter(equipo_visitante=equipo, grupo=grupo, estado=TERMINADO)

		n_resultado_favor_local = query_partido_local.aggregate(sumatorio=Sum('resultado_local'))
		n_resultado_favor_visitante = query_partido_visitante.aggregate(sumatorio=Sum('resultado_visitante'))
		if not n_resultado_favor_local['sumatorio']:
			n_resultado_favor_local['sumatorio'] = 0
		if not n_resultado_favor_visitante['sumatorio']:
			n_resultado_favor_visitante['sumatorio'] = 0
		clasificacion.puntos_favor = n_resultado_favor_local['sumatorio'] + n_resultado_favor_visitante['sumatorio']

		n_resultado_contr_local = query_partido_local.aggregate(sumatorio=Sum('resultado_visitante'))
		n_resultado_contra_visitante = query_partido_visitante.aggregate(sumatorio=Sum('resultado_local'))
		if not n_resultado_contr_local['sumatorio']:
			n_resultado_contr_local['sumatorio'] = 0
		if not n_resultado_contra_visitante['sumatorio']:
			n_resultado_contra_visitante['sumatorio'] = 0
		clasificacion.puntos_contra = n_resultado_contr_local['sumatorio'] + n_resultado_contra_visitante['sumatorio']
	# Puntos de Juegos
	# Guardar
	clasificacion.save()


def get_posicion_clasificacion_ascenso_list(grupo):
	posicion_clasificacion_ascenso_list=[]
	clasificacion_list = Clasificacion.objects.filter(grupo=grupo)
	ascenso_list = Ascenso.objects.filter(grupo=grupo)
	for posicion in range(1, len(clasificacion_list) + 1):
		ascenso_aux = None
		for ascenso in ascenso_list:
			if posicion in ascenso.get_posiciones_array():
				ascenso_aux = ascenso
				break
			else:
				ascenso_aux = None

		aux = [posicion, clasificacion_list[posicion-1], ascenso_aux]
		posicion_clasificacion_ascenso_list.append(aux)
	return posicion_clasificacion_ascenso_list
