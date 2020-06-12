from django.utils.translation import gettext_lazy as _
from cubogt.models import Grupo, Fase, Ascenso


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

def realizar_ascenso():
	# TODO, llamar cuando creo un ascenso en una fase terminada COMPROBAR ERRORES,
	#  o cuando termino el ultimo partido de una fase
	#  o dando al boron de actualizar equipos en Fase/Equipos
	pass