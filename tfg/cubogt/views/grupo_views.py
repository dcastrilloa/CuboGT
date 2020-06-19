from django.shortcuts import render, get_object_or_404, redirect

from cubogt.controller import GrupoController
from cubogt.forms import GrupoForm, GrupoGenerarForm, GrupoEquipoForm
from cubogt.models import Torneo, Fase, Grupo, Equipo
from cubogt.static.constantes import CREACION, ELIMINATORIA, LIGA


def grupo_lista(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo_list = Grupo.objects.filter(fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'grupo_list': grupo_list}
	return render(request, 'cubogt/fase_creacion/grupo/grupo_lista.html', context)


def grupo_nuevo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION, tipo_fase=LIGA)
	if request.method == "POST":
		form = GrupoForm(request.POST)
		if form.is_valid():
			grupo = form.save(commit=False)
			grupo.fase = fase
			grupo.save()
			return redirect('grupo_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = GrupoForm()

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase_creacion/grupo/grupo_nuevo.html', context)


def grupo_generar(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION, tipo_fase=LIGA)
	if request.method == "POST":
		form = GrupoGenerarForm(request.POST)
		if form.is_valid():
			numero_grupos = form.cleaned_data['numero_grupos']
			tipo_nombre = form.cleaned_data['tipo_nombre']
			GrupoController.generar_grupos(fase, numero_grupos, tipo_nombre)
			return redirect('grupo_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = GrupoGenerarForm()

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase_creacion/grupo/grupo_generar.html', context)


def grupo_generar_eliminatoria(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION, tipo_fase=ELIMINATORIA)
	GrupoController.grupo_generar_eliminatoria(fase)

	return redirect('grupo_lista', torneo_id=torneo.id, fase_id=fase_id)


def grupo_editar(request, torneo_id, fase_id, grupo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	if request.method == "POST":
		form = GrupoForm(request.POST, instance=grupo)
		if form.is_valid():
			grupo = form.save(commit=False)
			grupo.save()
			return redirect('grupo_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = GrupoForm(instance=grupo)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase_creacion/grupo/grupo_editar.html', context)


def grupo_borrar(request, torneo_id, fase_id, grupo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION, tipo_fase=LIGA)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	grupo.delete()

	return redirect('grupo_lista', torneo_id=torneo.id, fase_id=fase_id)


def grupo_borrar_todo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)
	grupo_list = Grupo.objects.filter(fase=fase)
	for grupo in grupo_list:
		grupo.delete()

	return redirect('grupo_lista', torneo_id=torneo.id, fase_id=fase_id)


def grupo_equipo_lista(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo_list = Grupo.objects.filter(fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'grupo_list': grupo_list}
	return render(request, 'cubogt/fase_creacion/grupo/equipo/grupo_equipos.html', context)


def grupo_equipo_lista_especifico(request, torneo_id, fase_id, grupo_id):
	return grupo_equipo_lista(request, torneo_id, fase_id)


def grupo_equipo_editar(request, torneo_id, fase_id, grupo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	if request.method == "POST":
		form = GrupoEquipoForm(request.POST, instance=grupo, fase=fase, grupo=grupo)
		if form.is_valid():
			grupo = form.save(commit=False)
			grupo.save()
			form.save_m2m()
			return redirect('grupo_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = GrupoEquipoForm(instance=grupo, fase=fase, grupo=grupo)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase_creacion/grupo/equipo/grupo_equipo_editar.html', context)


def grupo_equipo_borrar_todo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)
	grupo_list = fase.grupo_set.all()
	for grupo in grupo_list:
		grupo.equipos.clear()
		grupo.save()
	return redirect('grupo_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)


def grupo_equipo_borrar(request, torneo_id, fase_id, grupo_id, equipo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	equipo = get_object_or_404(Equipo, pk=equipo_id, grupo=grupo)

	GrupoController.borrar_equipo(grupo, equipo)

	return redirect('grupo_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)


def grupo_repartir_equipos(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)

	GrupoController.repartir_equipos(fase)

	return redirect('grupo_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)
