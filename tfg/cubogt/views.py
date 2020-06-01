from django.shortcuts import render, get_object_or_404, redirect
from cubogt.models import Torneo
from cubogt.forms import *
from cubogt.static.constantes import *
from django.utils import timezone


def index(request):
	return redirect('lista_torneo')


#  -----------------------------------------------------------------
#    TORNEO views
#  -----------------------------------------------------------------

def torneo_lista(request):
	mis_torneos_list = Torneo.objects.filter(usuario=request.user)
	return render(request, 'cubogt/torneos/lista_torneos.html', context={'mis_torneos_list': mis_torneos_list})


def torneo_nuevo(request):
	if request.method == "POST":

		form = TorneoForm(request.POST)
		if form.is_valid():
			torneo = form.save(commit=False)
			torneo.usuario = request.user
			torneo.estado = CREACION
			torneo.save()
			return redirect('torneo', torneo_id=torneo.id)
	else:
		form = TorneoForm()

	disenyo = "cubogt/base.html"
	context = {'form': form, 'disenyo': disenyo}
	return render(request, 'cubogt/torneos/nuevo_torneo.html', context)


def torneo_ver(request, torneo_id):
	torneo_aux = get_object_or_404(Torneo, pk=torneo_id)
	context = {'torneo': torneo_aux}
	return render(request, 'cubogt/torneos/torneo.html', context)


def torneo_editar(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	if request.method == "POST":
		form = TorneoForm(request.POST, instance=torneo)
		if form.is_valid():
			torneo = form.save(commit=False)
			# torneo.usuario = request.user
			torneo.save()
			return redirect('torneo', torneo_id=torneo.id)
	else:
		form = TorneoForm(instance=torneo)

	disenyo = "cubogt/navbar.html"
	context = {'torneo': torneo, 'form': form, 'disenyo': disenyo}
	return render(request, 'cubogt/torneos/nuevo_torneo.html', context)


def torneo_borrar(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	torneo.delete()
	return redirect('lista_torneo')


#  -----------------------------------------------------------------
#    Equipos views
#  -----------------------------------------------------------------

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
	torneo = get_object_or_404(Torneo, pk=torneo_id, usurio=request.user)
	equipo = torneo.equipos.get(pk=equipo_id)

	torneo.equipos.remove(equipo)

	return redirect('equipo_lista', torneo_id=torneo.id)


#  -----------------------------------------------------------------
#    Campos views
#  -----------------------------------------------------------------

def campo_lista(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	campos_list = Campo.objects.filter(torneo=torneo)
	context = {'torneo': torneo, 'campos_list': campos_list}
	return render(request, 'cubogt/campo/campo_lista.html', context)


def campo_nuevo(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	if request.method == "POST":
		form = CampoForm(request.POST)
		if form.is_valid():
			campo = form.save(commit=False)
			campo.torneo = torneo
			campo.save()

			return redirect('campo_lista', torneo_id=torneo.id)
	else:
		form = CampoForm()
	context = {'torneo': torneo, 'form': form}
	return render(request, 'cubogt/campo/campo_nuevo.html', context)


def campo_editar(request, torneo_id, campo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	campo = get_object_or_404(Campo, pk=campo_id, torneo=torneo)
	if request.method == "POST":
		form = CampoForm(request.POST, instance=campo)
		if form.is_valid():
			campo = form.save(commit=False)
			campo.save()
			return redirect('campo_lista', torneo_id=torneo.id)
	else:
		form = CampoForm(instance=campo)

	context = {'torneo': torneo, 'form': form}
	return render(request, 'cubogt/campo/campo_editar.html', context)


def campo_borrar(request, torneo_id, campo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	campo = get_object_or_404(Campo, pk=campo_id, torneo=torneo)

	campo.delete()

	return redirect('campo_lista', torneo_id=torneo.id)



