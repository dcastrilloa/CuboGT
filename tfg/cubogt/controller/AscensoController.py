from cubogt.models import Grupo, Equipo, Fase, Ascenso
from cubogt.static.constantes import *
from django.db.models import Count


def ascenso_general(fase, form):
	grupo_list = Grupo.objects.filter(fase=fase)
	numero_equipos = form.cleaned_data['numero_equipos']
	desde_posicion = form.cleaned_data['desde_posicion']
	proxima_fase = form.cleaned_data['proxima_fase']
	for grupo in grupo_list:
		ascenso = Ascenso(numero_equipos=numero_equipos, desde_posicion=desde_posicion, proxima_fase=proxima_fase,
						  grupo=grupo)
		ascenso.save()


def ascenso_borrar_todo(fase=Fase):
	grupo_list = Grupo.objects.filter(fase=fase)
	ascenso_list = Ascenso.objects.filter(grupo__in=grupo_list)
	for ascenso in ascenso_list:
		ascenso.delete()