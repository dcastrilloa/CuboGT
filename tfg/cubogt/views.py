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


#  -----------------------------------------------------------------
#    Fase views
#  -----------------------------------------------------------------

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
	fase.equipos.clear()
	# TODO: Limpiar los grupos de esa fase sin equipos
	fase.save()
	return redirect('fase_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)


def fase_equipo_borrar(request, torneo_id, fase_id, equipo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	equipo = get_object_or_404(Equipo, pk=equipo_id, fase=fase)
	fase.equipos.remove(equipo)
	fase.save()
	return redirect('fase_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)


#  -----------------------------------------------------------------
#    Grupo views
#  -----------------------------------------------------------------

def grupo_lista(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo_list = Grupo.objects.filter(fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'grupo_list': grupo_list}
	return render(request, 'cubogt/fase/grupo/grupo_lista.html', context)


def grupo_nuevo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
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
	return render(request, 'cubogt/fase/grupo/grupo_nuevo.html', context)


def grupo_editar(request, torneo_id, fase_id, grupo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	if request.method == "POST":
		form = GrupoForm(request.POST, instance=grupo)
		if form.is_valid():
			grupo = form.save(commit=False)
			grupo.fase = fase
			grupo.save()
			form.save_m2m()
			return redirect('grupo_lista', torneo_id=torneo.id, fase_id=fase_id)
	else:
		form = GrupoForm(instance=grupo)

	context = {'torneo': torneo, 'fase': fase, 'form': form}
	return render(request, 'cubogt/fase/grupo/grupo_editar.html', context)


def grupo_borrar(request, torneo_id, fase_id, grupo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)

	grupo.delete()

	return redirect('grupo_borrar', torneo_id=torneo.id)


def grupo_equipo_lista(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo_list = Grupo.objects.filter(fase=fase)

	context = {'torneo': torneo, 'fase': fase, 'grupo_list': grupo_list}
	return render(request, 'cubogt/fase/grupo/equipo/grupo_equipos.html', context)


def grupo_equipo_editar(request, torneo_id, fase_id, grupo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
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
	return render(request, 'cubogt/fase/grupo/equipo/grupo_equipo_editar.html', context)


def grupo_equipo_borrar_todo(request, torneo_id, fase_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo_list = fase.grupo_set.all()
	for grupo in grupo_list:
		grupo.equipos.clear()
		grupo.save()
	return redirect('grupo_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)


def grupo_equipo_borrar(request, torneo_id, fase_id, grupo_id, equipo_id):
	torneo = get_object_or_404(Torneo, pk=torneo_id, usuario=request.user)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	equipo = get_object_or_404(Equipo, pk=equipo_id, grupo=grupo)
	# clasificacion = get_object_or_404(Clasificacion, grupo=grupo, equipo=equipo)
	grupo.equipos.remove(equipo)
	# TODO?: ¿Puedo borrar si tengo algo en la clasificacion?

	# clasificacion.save()
	return redirect('grupo_equipo_lista', torneo_id=torneo.id, fase_id=fase_id)
