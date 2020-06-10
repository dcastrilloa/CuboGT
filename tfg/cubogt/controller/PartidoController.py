from django.shortcuts import render, get_object_or_404, redirect
from cubogt.forms import FaseForm, FasePuntoForm, FaseSetForm, FaseEquipoForm
from ..controller import GrupoController
from ..models import Torneo, Fase, Equipo , Partido, Campo


def a():
	# campo= Campo.objects.filter(fase=fase).exclude(partido__estado=ACTIVO)
	# campo=Campo.objects.filter(fase=fase,libre=True)
	pass
