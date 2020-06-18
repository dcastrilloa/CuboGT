from django.utils.translation import gettext_lazy as _
from cubogt.models import Grupo, Equipo, Fase
from cubogt.static.constantes import ABECEDARIO
from django.db.models import Count
from string import ascii_uppercase


def comprobar(fase):
	msg_error = comprobar_grupos(fase)
	msg_error.extend(comprobar_grupos_equipos(fase))
	return msg_error


def comprobar_grupos(fase):
	msg_error = []
	grupos_list = Grupo.objects.filter(fase=fase)
	if not grupos_list:
		msg_error.append(_("No hay grupos creados dentro de la fase.\n"))
	else:
		for grupo in grupos_list:
			if not grupo.equipos.count():
				msg_error.append(_("El grupo %(grupo)s no tiene ningún equipo asignado.\n") % {'grupo': grupo.nombre})
	return msg_error


def comprobar_grupos_equipos(fase):
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


def generar_grupos(fase, numero_grupos, tipo_nombre):
	if tipo_nombre == ABECEDARIO:
		for x in range(numero_grupos):
			nombre = "Grupo " + ascii_uppercase[x]
			nuevo_grupo(fase, nombre)
	else:
		for x in range(1, numero_grupos + 1):
			nombre = "Grupo " + str(x)
			nuevo_grupo(fase, nombre)
