from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import AscensoForm, AscensoGeneralForm
from ..controller import AscensoController
from ..static.constantes import CREACION
from ..models import Torneo, Fase, Ascenso, Grupo


def ascenso_lista(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	ascenso_list = Ascenso.objects.filter(grupo__fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'ascenso_list': ascenso_list}
	return render(request, 'cubogt/fase/ascenso/ascenso_lista.html', context)


def ascenso_nuevo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)
	if request.method == "POST":
		form = AscensoForm(request.POST, fase=fase)
		if form.is_valid():
			ascenso = form.save(commit=False)
			ascenso.save()
			return redirect('ascenso_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = AscensoForm(fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase/ascenso/ascenso_nuevo.html', context)


def ascenso_nuevo_general(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)
	if request.method == "POST":
		form = AscensoGeneralForm(request.POST, fase=fase)
		if form.is_valid():
			AscensoController.ascenso_general(fase, form)
			return redirect('ascenso_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = AscensoGeneralForm(fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase/ascenso/ascenso_nuevo.html', context)


def ascenso_editar(request, torneo_id, fase_id, ascenso_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)
	grupo_list = Grupo.objects.filter(fase=fase)
	ascenso = get_object_or_404(Ascenso, pk=ascenso_id, grupo__in=grupo_list)
	if request.method == "POST":
		form = AscensoForm(request.POST, instance=ascenso, fase=fase)
		if form.is_valid():
			ascenso = form.save(commit=False)
			ascenso.save()
			return redirect('ascenso_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = AscensoForm(instance=ascenso, fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase/ascenso/ascenso_editar.html', context)


def ascenso_borrar(request, torneo_id, fase_id, ascenso_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)
	grupo_list = Grupo.objects.filter(fase=fase)
	ascenso = get_object_or_404(Ascenso, pk=ascenso_id, grupo__in=grupo_list)

	ascenso.delete()
	return redirect('ascenso_lista', torneo_id=torneo_id, fase_id=fase_id)


def ascenso_borrar_todo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, estado=CREACION)

	AscensoController.ascenso_borrar_todo(fase)
	return redirect('ascenso_lista', torneo_id=torneo_id, fase_id=fase_id)
