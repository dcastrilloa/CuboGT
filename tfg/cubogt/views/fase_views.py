from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import *
from ..controller import GrupoController



def fase_lista(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fases_list = Fase.objects.filter(torneo=torneo)
	context = {'torneo': torneo, 'fases_list': fases_list}
	return render(request, 'cubogt/fase/fase_lista.html', context)


def fase_nueva(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	if request.method == "POST":
		form = FaseForm(request.POST)
		form_set = FaseSetForm(request.POST)
		form_punto = FasePuntoForm(request.POST)
		if form.is_valid():
			# TODO: simplificar en el Form
			fase = form.save(commit=False)
			if torneo.deporte.set:
				if form_set.is_valid():
					fase_aux = form_set.save(commit=False)
					fase.numero_sets = fase_aux.numero_sets
			if torneo.deporte.punto:
				if form_punto.is_valid():
					fase_aux = form_punto.save(commit=False)
					fase.numero_puntos = fase_aux.numero_puntos
					fase.puntos_maximos = fase_aux.puntos_maximos

			fase.torneo = torneo
			fase.save()
			return redirect('fase_lista', torneo_id=torneo.id)
	else:
		form = FaseForm()
		form_set = FaseSetForm()
		form_punto = FasePuntoForm()
	context = {'torneo': torneo, 'form': form, 'form_set': form_set, 'form_punto': form_punto}
	return render(request, 'cubogt/fase/fase_nueva.html', context)


def fase_editar(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	if request.method == "POST":
		form = FaseForm(request.POST, instance=fase)
		form_set = FaseSetForm(request.POST, instance=fase)
		form_punto = FasePuntoForm(request.POST, instance=fase)
		if form.is_valid():
			fase = form.save(commit=False)
			if torneo.deporte.set:
				if form_set.is_valid():
					fase_aux = form_set.save(commit=False)
					fase.numero_sets = fase_aux.numero_sets
			if torneo.deporte.punto:
				if form_punto.is_valid():
					fase_aux = form_punto.save(commit=False)
					fase.numero_puntos = fase_aux.numero_puntos
					fase.puntos_maximos = fase_aux.puntos_maximos

			fase.save()
			return redirect('fase_lista', torneo_id=torneo.id)
	else:
		form = FaseForm(instance=fase)
		form_set = FaseSetForm(instance=fase)
		form_punto = FasePuntoForm(instance=fase)
	context = {'torneo': torneo, 'form': form, 'form_set': form_set, 'form_punto': form_punto}
	return render(request, 'cubogt/fase/fase_editar.html', context)


def fase_borrar(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)

	fase.delete()

	return redirect('fase_lista', torneo_id=torneo.id)


def fase_ver(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	context = {'torneo': torneo, 'fase': fase}
	return render(request, 'cubogt/fase/fase_ver.html', context)


def fase_equipo_lista(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	equipo_list = fase.equipos.all()

	context = {'torneo': torneo, 'fase': fase, 'equipo_list': equipo_list}
	return render(request, 'cubogt/fase/equipo/fase_equipo.html', context)


def fase_equipo_editar(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	if request.method == "POST":
		form = FaseEquipoForm(request.POST, instance=fase, torneo=torneo)
		if form.is_valid():
			fase = form.save(commit=False)
			fase.save()
			form.save_m2m()
			return redirect('fase_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = FaseEquipoForm(instance=fase, torneo=torneo)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase/equipo/fase_equipo_editar.html', context)


def fase_equipo_agregar_todo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	fase.equipos.add(*Equipo.objects.filter(torneo=torneo))
	fase.save()
	return redirect('fase_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)


def fase_equipo_borrar_todo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)

	grupos_list = fase.grupo_set.all()
	for grupo in grupos_list:
		grupo.equipos.clear()
	fase.equipos.clear()
	#fase.save()

	return redirect('fase_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)


def fase_equipo_borrar(request, torneo_id, fase_id, equipo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	equipo = get_object_or_404(Equipo, pk=equipo_id, fase=fase)

	GrupoController.borrar_equipo_de_fase(fase, equipo)
	fase.equipos.remove(equipo)
	#fase.save()

	return redirect('fase_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)
