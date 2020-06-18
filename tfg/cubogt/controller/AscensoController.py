from django.utils.translation import gettext_lazy as _

from cubogt.controller import FaseController
from cubogt.models import Grupo, Ascenso, Clasificacion
from cubogt.static.constantes import TERMINADO, CREACION, ERROR, ESPERA, REALIZADO


def comprobar(fase):
	msg_error = []
	msg_error2 = []
	msg_error2_aux = []
	grupo_list = Grupo.objects.filter(fase=fase)
	if grupo_list:
		for grupo in grupo_list:
			ascenso_list = Ascenso.objects.filter(grupo=grupo)
			if ascenso_list:
				msg_error2_aux = []
				posiciones = ""
				for ascenso in ascenso_list:
					ultimo_clasificado = ascenso.desde_posicion + ascenso.numero_equipos - 1
					if ultimo_clasificado > grupo.equipos.count():
						msg_error.append(
							_("El grupo: %(grupo)s tiene %(n_equipos)d equipo y se quiere ascender un equipo en la "
							  "posición %(posicion)d\n") % \
							{'grupo': grupo.nombre, 'n_equipos': grupo.equipos.count(),
							 'posicion': ultimo_clasificado})
					for x in range(ascenso.desde_posicion, ascenso.desde_posicion + ascenso.numero_equipos):
						if str(x) in posiciones:
							msg_error2_aux.append(
								_("Hay dos o mas ascensos que tienen el mismo rango de posiciones en un mismo "
								  "grupo: %(grupo)s\n") % {'grupo': grupo.nombre})
							break
						else:
							posiciones += str(x)
			msg_error2.extend(msg_error2_aux)
	msg_error.extend(msg_error2)
	return msg_error


def ascenso_comprobar(ascenso):
	msg_error = []
	posiciones_error = []
	grupo = ascenso.grupo
	ascenso_list = Ascenso.objects.filter(grupo=grupo).exclude(pk=ascenso.id)
	array_posiciones = ascenso.get_posiciones_array()
	# Compruebo que longitud
	if array_posiciones[-1] > grupo.equipos.count():
		ascenso.estado = ERROR
		msg_error.append(
			_("El grupo: %(grupo)s tiene %(n_equipos)d equipos y se quiere ascender un equipo en la "
			"posición %(posicion)d.\n") % {'grupo': grupo.nombre, 'n_equipos': grupo.equipos.count(), 'posicion': array_posiciones[-1]})
	# Compruebo coincidencias
	for ascenso_aux in ascenso_list:
		for posicion in array_posiciones:
			if posicion in ascenso_aux.get_posiciones_array():
				ascenso.estado = ERROR
				posiciones_error.append(posicion)
				if ascenso_aux.estado == ESPERA:
					ascenso_aux.estado = ERROR
					ascenso_aux.save()
	if posiciones_error:
		msg_error.append(_("El ascenso tiene las posicion/es: %(posicion)s en conflicto con otros ascensos.\n") % \
			{'posicion': str(posiciones_error)})

	if not msg_error:
		fase = ascenso.grupo.fase
		if fase.estado != TERMINADO:
			ascenso.estado = ESPERA
		else:  # Fase Terminada
			ascenso.estado = REALIZADO
			realizar_ascenso(ascenso)
	return msg_error


def ascenso_guardar(ascenso):
	msg_error_list = ascenso_comprobar(ascenso)
	ascenso.save()
	return msg_error_list


def ascenso_general(fase, form=None, numero_equipos=0, desde_posicion=0, proxima_fase=None):
	grupo_list = Grupo.objects.filter(fase=fase)
	if form:
		numero_equipos = form.cleaned_data['numero_equipos']
		desde_posicion = form.cleaned_data['desde_posicion']
		proxima_fase = form.cleaned_data['proxima_fase']
	msg_error = []
	for grupo in grupo_list:
		ascenso = Ascenso(numero_equipos=numero_equipos, desde_posicion=desde_posicion, proxima_fase=proxima_fase,
						  grupo=grupo)
		msg_error_aux = ascenso_guardar(ascenso)
		msg_error.extend(msg_error_aux)
	return msg_error


def ascenso_editar(ascenso):
	if ascenso.estado == REALIZADO:
		borrar_equipos_ascendidos(ascenso)


def ascenso_borrar(ascenso):
	if ascenso.estado == REALIZADO:
		borrar_equipos_ascendidos(ascenso)
	ascenso.delete()


def ascenso_borrar_todo(fase):
	grupo_list = Grupo.objects.filter(fase=fase)
	ascenso_list = Ascenso.objects.filter(grupo__in=grupo_list)
	for ascenso in ascenso_list:
		ascenso_borrar(ascenso)


def realizar_ascenso_fase(fase):
	#  AUTOMATICO fase tras el ultimo partido de una fase
	ascenso_list = Ascenso.objects.filter(grupo__fase=fase)
	for ascenso in ascenso_list:
		ascenso_guardar(ascenso)  # Comprueba el ascenso y luego guarda el estado


def realizar_ascenso(ascenso):
	grupo = ascenso.grupo
	clasificacion = Clasificacion.objects.filter(grupo=grupo)
	for posicion in ascenso.get_posiciones_array():
		equipo = clasificacion[posicion - 1].equipo
		FaseController.fase_equipo_nuevo(ascenso.proxima_fase, equipo)


def recibir_ascenso(fase):
	ascenso_list = Ascenso.objects.filter(proxima_fase=fase)
	for ascenso in ascenso_list:
		grupo = ascenso.grupo
		clasificacion = Clasificacion.objects.filter(grupo=grupo)
		for posicion in ascenso.get_posiciones_array():
			equipo = clasificacion[posicion - 1].equipo
			FaseController.fase_equipo_nuevo(fase, equipo)


def borrar_equipos_ascendidos(ascenso):
	grupo = ascenso.grupo
	clasificacion = Clasificacion.objects.filter(grupo=grupo)
	for posicion in ascenso.get_posiciones_array():
		equipo = clasificacion[posicion - 1].equipo
		if ascenso.proxima_fase.estado == CREACION:
			FaseController.borrar_equipo_de_fase(ascenso.proxima_fase, equipo)
