from django.shortcuts import render, get_object_or_404

from cubogt.controller import FaseController, ClasificacionController
from cubogt.models import Torneo, Fase, Grupo


def clasificacion_ver(request, torneo_id, fase_id, grupo_id=None):
	torneo = get_object_or_404(Torneo, pk=torneo_id)
	fase = get_object_or_404(Fase, pk=fase_id, torneo=torneo)
	if grupo_id:
		grupo = get_object_or_404(Grupo, pk=grupo_id, fase=fase)
	else:
		grupo = fase.grupo_set.first()

	grupo_list = fase.grupo_set.all()
	posicion_clasificacion_ascenso_list = ClasificacionController.get_posicion_clasificacion_ascenso_list(grupo)

	fase_activa_terminada_list = FaseController.get_fases_activas_terminadas(torneo)
	context = {'torneo': torneo, 'fase_activa_terminada_list': fase_activa_terminada_list, 'fase': fase,
			   'grupo_list': grupo_list, 'grupo': grupo,
			   'posicion_clasificacion_ascenso_list':posicion_clasificacion_ascenso_list}
	return render(request, 'cubogt/fase_activa/clasificacion/clasificacion_ver.html', context)
