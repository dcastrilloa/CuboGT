from django.shortcuts import render, get_object_or_404, redirect

from cubogt.controller import FaseController, CampoController
from cubogt.forms import *


def campo_lista(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	campos_list = Campo.objects.filter(torneo=torneo_id)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'campos_list': campos_list}
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

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'form': form}
	return render(request, 'cubogt/campo/campo_nuevo.html', context)


def campo_generar(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	if request.method == "POST":
		form = CampoGenerarForm(request.POST)
		if form.is_valid():
			numero_campos = form.cleaned_data['numero_campos']
			tipo_nombre = form.cleaned_data['tipo_nombre']
			CampoController.generar_campos(torneo, numero_campos, tipo_nombre)
			return redirect('campo_lista', torneo_id=torneo.id)
	else:
		form = CampoGenerarForm()

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'form': form}
	return render(request, 'cubogt/campo/campo_generar.html', context)


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

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'form': form}
	return render(request, 'cubogt/campo/campo_editar.html', context)


def campo_borrar(request, torneo_id, campo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user, estado=CREACION)
	campo = get_object_or_404(Campo, pk=campo_id, torneo=torneo)

	campo.delete()

	return redirect('campo_lista', torneo_id=torneo.id)


def campo_fase_lista(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id)
	campos_list = Campo.objects.filter(fase=fase)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list,'fase': fase,
			   'campos_list': campos_list}
	return render(request, 'cubogt/fase_activa/campo/campo_fase_lista.html', context)


def campo_fase_editar(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=ACTIVO)
	if request.method == "POST":
		form = FaseCampoForm(request.POST, instance=fase, torneo=torneo, fase=fase)
		if form.is_valid():
			fase = form.save(commit=False)
			fase.save()
			form.save_m2m()
			FaseController.iniciar_siguiente_partido(fase)
			return redirect('campo_fase_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = FaseCampoForm(instance=fase, torneo=torneo, fase=fase)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase_activa/campo/campo_fase_editar.html', context)


def campo_fase_borrar(request, torneo_id, fase_id, campo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id,torneo=torneo, estado=ACTIVO)
	campo = get_object_or_404(Campo, pk=campo_id, torneo=torneo, fase=fase)

	fase.campos.remove(campo)

	return redirect('campo_fase_lista', torneo_id=torneo.id, fase_id=fase_id)