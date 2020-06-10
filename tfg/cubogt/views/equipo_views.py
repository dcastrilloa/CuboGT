from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import *


def equipo_lista(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	equipos_list = Equipo.objects.filter(torneo=torneo)
	context = {'torneo': torneo, 'equipos_list': equipos_list}
	return render(request, 'cubogt/equipo/equipos_lista.html', context)


def equipo_nuevo(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	if request.method == "POST":
		form = EquipoForm(request.POST)
		if form.is_valid():
			equipo = form.save(commit=False)
			equipo.save()
			# TODO: Funcion para agregar el equipo a un usuario
			torneo.equipos.add(equipo)
			return redirect('equipo_lista', torneo_id=torneo.id)
	else:
		form = EquipoForm()
	context = {'torneo': torneo, 'form': form}
	return render(request, 'cubogt/equipo/equipo_nuevo.html', context)


def equipo_editar(request, torneo_id, equipo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	equipo = get_object_or_404(Equipo, pk=equipo_id, torneo=torneo)
	if request.method == "POST":
		form = EquipoForm(request.POST, instance=equipo)
		if form.is_valid():
			equipo = form.save(commit=False)
			# torneo.usuario = request.user
			equipo.save()
			# TODO: Funcion para agregar el equipo a un usuario
			return redirect('equipo_lista', torneo_id=torneo.id)
	else:
		form = EquipoForm(instance=equipo)

	context = {'torneo': torneo, 'form': form}
	return render(request, 'cubogt/equipo/equipo_editar.html', context)


def equipo_borrar(request, torneo_id, equipo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user, estado=CREACION)
	equipo = torneo.equipos.get(pk=equipo_id, torneo=torneo)

	torneo.equipos.remove(equipo)

	return redirect('equipo_lista', torneo_id=torneo.id)
