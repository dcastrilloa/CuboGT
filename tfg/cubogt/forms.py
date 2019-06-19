from django import forms
from .models import *
from .controller.constantes import *


class TorneoForm(forms.ModelForm):
	class Meta:
		model = Torneo
		fields = ('deporte', 'nombre', 'fecha', 'tipo_torneo')

	tipo_torneo = forms.ChoiceField(choices=TIPO_TORNEO)

class LigaFoms(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('nombre','numero_equipos', 'numero_sets', 'numero_puntos', 'puntos_maximos', 'cambio_de_campo', 'cambio_a_los')