from django.shortcuts import render, get_object_or_404, redirect
from cubogt.models import Torneo
from cubogt.forms import *
from cubogt.static.constantes import *
from django.utils import timezone


def index(request):
	return redirect('lista_torneo')

# TORNEO
def lista_torneo(request):
	mis_torneos_list = Torneo.objects.filter(usuario=request.user)
	return render(request, 'cubogt/torneos/lista_torneos.html', context={'mis_torneos_list': mis_torneos_list})


def nuevo_torneo(request):
	if request.method == "POST":

		form = TorneoForm(request.POST)
		if form.is_valid():
			torneo = form.save(commit=False)
			torneo.usuario = request.user
			torneo.estado = CREACION
			torneo.save()
	else:
		form = TorneoForm()
	return render(request, 'cubogt/torneos/nuevo_torneo.html', {'form': form})


def torneo2(request, pk):
	torneo_aux = get_object_or_404(Torneo, pk=pk)
	return render(request, 'cubogt/torneos/torneo.html', {'torneo': torneo_aux})
