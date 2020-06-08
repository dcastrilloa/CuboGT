from cubogt.models import Grupo, Equipo, Fase
from cubogt.static.constantes import *
from django.db.models import Count
from string import ascii_uppercase


def borrar_equipo(grupo=Grupo, equipo=Equipo):
	"""Quita la relacion de un equipo con un grupo"""
	grupo.equipos.remove(equipo)


# clasificacion = get_object_or_404(Clasificacion, grupo=grupo, equipo=equipo)
# TODO?: ¿Puedo borrar si tengo algo en la clasificacion?


def borrar_equipo_de_fase(fase=Fase, equipo=Equipo):
	"""Busca un grupo de la fase y borra la relacion con el equipo"""
	grupo = Grupo.objects.filter(fase=fase, equipos=equipo)
	if grupo:
		borrar_equipo(grupo, equipo)


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
		for x in range(1, numero_grupos+1):
			nombre = "Grupo " + str(x)
			nuevo_grupo(fase, nombre)
