from django.shortcuts import render, get_object_or_404, redirect

from cubogt.controller import FaseController
from cubogt.forms import TorneoForm
from cubogt.models import Torneo
from cubogt.static.constantes import CREACION


# TORNEO
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

	context = {'form': form}
	return render(request, 'cubogt/torneos/nuevo_torneo.html', context)


def torneo_ver(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list}
	return render(request, 'cubogt/torneos/torneo.html', context)


def torneo_editar(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, estado=CREACION)
	if request.method == "POST":
		form = TorneoForm(request.POST, instance=torneo)
		if form.is_valid():
			torneo = form.save(commit=False)
			# torneo.usuario = request.user
			torneo.save()
			return redirect('torneo', torneo_id=torneo.id)
	else:
		form = TorneoForm(instance=torneo)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'form': form, 'fase_activa_terminada_list': fase_activa_terminada_list}
	return render(request, 'cubogt/torneos/torneo_editar.html', context)


def torneo_borrar(request, torneo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	torneo.delete()
	return redirect('lista_torneo')
