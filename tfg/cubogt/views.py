from django.shortcuts import render, get_object_or_404, redirect
from .models import Torneo
from .forms import *
from .controller.constantes import *
from django.utils import timezone


def index (request):
	return redirect('login')


def mis_torneos(request):
	mis_torneos_list = Torneo.objects.filter(usuario=request.user)
	return render(request, 'cubogt/mis_torneos/mis_torneos.html', context={'mis_torneos_list': mis_torneos_list})


def nuevo_torneo(request):
	if request.method == "POST":

		form = TorneoForm(request.POST)
		if form.is_valid():
			torneo = form.save(commit=False)
			torneo.usuario = request.user
			torneo.estado = CREACION
			torneo.save()
			if torneo.tipo_torneo == 1:
				return redirect('nueva_liga', id=torneo.id)
			elif torneo.tipo_torneo == 2:
				return redirect('nueva_eliminatoria', id=torneo.id)
			else:
				return redirect('nueva_fase_grupos', id=torneo.id)
	else:
		form = TorneoForm()
	return render(request, 'cubogt/nuevo_torneo/nuevo_torneo.html', {'form': form})


"""
def nueva_liga (request):
	if request.method == "POST":
		form = LigaFoms(request.POST)
		if form.is_valid():
			fase = form.save(commit=False)
			fase.tipo_fase = LIGA
			fase.save()
			if torneo.tipo_torneo == 1:
				return redirect('nueva_liga', id=torneo.id)
			elif
				return redirect('nueva_eliminatoria', id=torneo.id)
			else:
				return redirect('nueva_fase_grupos', id=torneo.id)
	else:
		form = PostForm()
	return render(request, 'blog/post_new.html', {'form': form})
"""