from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import *


def campo_lista(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	campos_list = Campo.objects.filter(torneo=torneo_id)
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
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user, estado=CREACION)
	campo = get_object_or_404(Campo, pk=campo_id, torneo=torneo)

	campo.delete()

	return redirect('campo_lista', torneo_id=torneo.id)
