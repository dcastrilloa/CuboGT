from django.shortcuts import render, get_object_or_404, redirect

from cubogt.forms import AscensoForm, AscensoGeneralForm
from ..controller import AscensoController
from ..models import Torneo, Fase, Ascenso, Grupo
from ..static.constantes import ERROR, LIGA


def ascenso_lista(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, tipo_fase=LIGA)
	ascenso_list = Ascenso.objects.filter(grupo__fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'ascenso_list': ascenso_list}
	return render(request, 'cubogt/fase_creacion/ascenso/ascenso_lista.html', context)


def ascenso_nuevo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, tipo_fase=LIGA)
	if request.method == "POST":
		form = AscensoForm(request.POST, fase=fase)
		if form.is_valid():
			ascenso = form.save(commit=False)
			msg_error_list = AscensoController.ascenso_guardar(ascenso)
			if msg_error_list:
				context = {'torneo': torneo, 'fase': fase, 'msg_error_list': msg_error_list}
				return render(request, 'cubogt/fase_creacion/ascenso/ascenso_error.html', context)
			else:
				return redirect('ascenso_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = AscensoForm(fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase_creacion/ascenso/ascenso_nuevo.html', context)


def ascenso_nuevo_general(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, tipo_fase=LIGA)
	if request.method == "POST":
		form = AscensoGeneralForm(request.POST, fase=fase)
		if form.is_valid():
			msg_error_list = AscensoController.ascenso_general(fase, form=form)  # Realizo el guardado (y comprobación) dentro
			if msg_error_list:
				context = {'torneo': torneo, 'fase': fase, 'msg_error_list': msg_error_list}
				return render(request, 'cubogt/fase_creacion/ascenso/ascenso_error.html', context)
			else:
				return redirect('ascenso_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = AscensoGeneralForm(fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase_creacion/ascenso/ascenso_nuevo.html', context)


def ascenso_editar(request, torneo_id, fase_id, ascenso_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, tipo_fase=LIGA)
	grupo_list = Grupo.objects.filter(fase=fase)
	ascenso = get_object_or_404(Ascenso, pk=ascenso_id, grupo__in=grupo_list)
	if request.method == "POST":
		form = AscensoForm(request.POST, instance=ascenso, fase=fase)
		if form.is_valid():
			ascenso = form.save(commit=False)
			msg_error_list = AscensoController.ascenso_guardar(ascenso)
			if msg_error_list:
				context = {'torneo': torneo, 'fase': fase, 'msg_error_list': msg_error_list}
				return render(request, 'cubogt/fase_creacion/ascenso/ascenso_error.html', context)
			else:
				return redirect('ascenso_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = AscensoForm(instance=ascenso, fase=fase)

	AscensoController.ascenso_editar(ascenso) #Limpia los equipos que tenia ya ascendidos
	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase_creacion/ascenso/ascenso_editar.html', context)


def ascenso_borrar(request, torneo_id, fase_id, ascenso_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, tipo_fase=LIGA)
	grupo_list = Grupo.objects.filter(fase=fase)
	ascenso = get_object_or_404(Ascenso, pk=ascenso_id, grupo__in=grupo_list)
	AscensoController.ascenso_borrar(ascenso)
	return redirect('ascenso_lista', torneo_id=torneo_id, fase_id=fase_id)


def ascenso_borrar_todo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, tipo_fase=LIGA)
	AscensoController.ascenso_borrar_todo(fase)
	return redirect('ascenso_lista', torneo_id=torneo_id, fase_id=fase_id)


def ascenso_comprobar(request, torneo_id, fase_id, ascenso_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo, tipo_fase=LIGA)
	grupo_list = Grupo.objects.filter(fase=fase)
	ascenso = get_object_or_404(Ascenso, pk=ascenso_id, grupo__in=grupo_list, estado=ERROR)

	msg_error_list = AscensoController.ascenso_guardar(ascenso)
	if msg_error_list:
		context = {'torneo': torneo, 'fase': fase, 'msg_error_list': msg_error_list}
		return render(request, 'cubogt/fase_creacion/ascenso/ascenso_error.html', context)
	else:
		return redirect('ascenso_lista', torneo_id=torneo.id, fase_id=fase_id)