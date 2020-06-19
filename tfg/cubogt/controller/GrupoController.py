from django.utils.translation import gettext_lazy as _
from cubogt.models import Grupo, Equipo, Fase
from cubogt.static.constantes import ABECEDARIO, LIGA, NUMEROS
from django.db.models import Count
from string import ascii_uppercase


def comprobar(fase):
	if fase.tipo_fase == LIGA:
		msg_error = comprobar_grupos_liga(fase)
		msg_error.extend(comprobar_equipos_sin_grupo(fase))
	else:  # Eliminatoria
		msg_error = comprobar_grupos_eliminatoria(fase)
	return msg_error


def comprobar_grupos_liga(fase):
	msg_error = []
	grupos_list = Grupo.objects.filter(fase=fase)
	if not grupos_list:
		msg_error.append(_("No hay grupos creados dentro de la fase.\n"))
	else:
		for grupo in grupos_list:
			if not grupo.equipos.count():
				msg_error.append(_("El grupo %(grupo)s no tiene ningún equipo asignado.\n") % {'grupo': grupo.nombre})
	return msg_error


def comprobar_grupos_eliminatoria(fase):
	msg_error = []
	grupos_list = Grupo.objects.filter(fase=fase)
	if grupos_list:  # Eliminatoria manual
		for grupo in grupos_list:
			numero_equipos = grupo.equipos.count()
			if not numero_equipos:
				msg_error.append(_("El %(grupo)s no tiene ningún equipo asignado.\n") % {'grupo': grupo.nombre})
			elif numero_equipos > 2:
				msg_error.append(_("El %(grupo)s tiene mas de 2 equipos.\n") % {'grupo': grupo.nombre})
		msg_error.extend(comprobar_equipos_sin_grupo(fase))
	return msg_error


def comprobar_equipos_sin_grupo(fase):
	msg_error = []
	grupo_list = Grupo.objects.filter(fase=fase)
	equipo_singrupo_list = Equipo.objects.filter(fase=fase).exclude(grupo__in=grupo_list)
	nombre_equipo_list = ""
	for equipo in equipo_singrupo_list:
		nombre_equipo_list += equipo.nombre + ", "

	if equipo_singrupo_list:
		msg_error.append(_("Los siguientes equipos están sin asignar a un grupo: %(equipo_list)s\n") % {'equipo_list': nombre_equipo_list[:-2]})
	return msg_error


def borrar_equipo(grupo, equipo):
	"""Quita la relación de un equipo con un grupo"""
	grupo.equipos.remove(equipo)


def repartir_equipos(fase=Fase):
	grupo_list = Grupo.objects.filter(fase=fase)
	equipo_singrupo_list = Equipo.objects.filter(fase=fase).exclude(grupo__in=grupo_list).order_by('?')
	for equipo in equipo_singrupo_list:
		grupo_list = Grupo.objects.filter(fase=fase).annotate(count=Count('equipos')).order_by('count')
		grupo_list.first().equipos.add(equipo)


def nuevo_grupo(fase, nombre):
	grupo = Grupo(nombre=nombre, fase=fase)
	grupo.save()


def generar_grupos(fase, numero_grupos, tipo_nombre, eliminatoria=False):
	prefijo = _("Grupo ")
	if eliminatoria:
		prefijo = _("Cruce ")

	if tipo_nombre == ABECEDARIO:
		for x in range(numero_grupos):
			nombre = prefijo + ascii_uppercase[x]
			nuevo_grupo(fase, nombre)
	else:
		for x in range(1, numero_grupos + 1):
			nombre = prefijo + str(x)
			nuevo_grupo(fase, nombre)


def grupo_generar_eliminatoria(fase):
	numero_grupos = get_numero_grupos_crear_eliminatoria(fase)
	generar_grupos(fase, numero_grupos, NUMEROS, eliminatoria=True)


def get_numero_grupos_crear_eliminatoria(fase):
	n_equipos = fase.equipos.count()
	orden_eliminatoria_list = bracket_seeds(n_equipos)
	n_grupos = len(orden_eliminatoria_list)//2
	return n_grupos


def bracket_seeds(num_teams):
	seeds = [1]
	while len(seeds) < num_teams:
		games = zip(seeds, (2 * len(seeds) + 1 - seed for seed in seeds))
		seeds = [team for game in games for team in game]
	return seeds


def get_numero_grupos(fase):
	return Grupo.objects.filter(fase=fase).count()