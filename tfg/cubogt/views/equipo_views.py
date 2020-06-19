from django.shortcuts import render, get_object_or_404, redirect

from cubogt.controller import FaseController, EquipoController
from cubogt.forms import EquipoForm
from cubogt.models import Torneo, Equipo
from cubogt.static.constantes import CREACION


def equipo_lista(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	equipos_list = Equipo.objects.filter(torneo=torneo)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'equipos_list': equipos_list}
	return render(request, 'cubogt/equipo/equipos_lista.html', context)


def equipo_nuevo(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	if request.method == "POST":
		form = EquipoForm(request.POST)
		if form.is_valid():
			equipo = form.save(commit=False)
			msg_error_list = EquipoController.comprobar_equipo_nombre(torneo, equipo)
			if msg_error_list:
				fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
				context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'msg_error_list': msg_error_list}
				return render(request, 'cubogt/equipo/equipo_error.html', context)
			else:
				equipo.save()
				torneo.equipos.add(equipo)
				# TODO: Funcion para agregar el equipo a un usuario
				return redirect('equipo_lista', torneo_id=torneo.id)
	else:
		form = EquipoForm()

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'form': form}
	return render(request, 'cubogt/equipo/equipo_nuevo.html', context)


def equipo_editar(request, torneo_id, equipo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	equipo = get_object_or_404(Equipo, pk=equipo_id, torneo=torneo)
	if request.method == "POST":
		form = EquipoForm(request.POST, instance=equipo)
		if form.is_valid():
			equipo = form.save(commit=False)
			msg_error_list = EquipoController.comprobar_equipo_nombre(torneo, equipo)
			if msg_error_list:
				fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
				context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'msg_error_list': msg_error_list}
				return render(request, 'cubogt/equipo/equipo_error.html', context)
			else:
				equipo.save()
				# TODO: Funcion para agregar el equipo a un usuario
				return redirect('equipo_lista', torneo_id=torneo.id)
	else:
		form = EquipoForm(instance=equipo)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'form': form}
	return render(request, 'cubogt/equipo/equipo_editar.html', context)


def equipo_borrar(request, torneo_id, equipo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user, estado=CREACION)
	equipo = torneo.equipos.get(pk=equipo_id, torneo=torneo)

	torneo.equipos.remove(equipo)

	return redirect('equipo_lista', torneo_id=torneo.id)
