from django import forms
from .models import *
from .controller.constantes import *


class TorneoForm(forms.ModelForm):
	class Meta:
		model = Torneo
		fields = ('deporte', 'nombre', 'fecha', 'descripcion')

	fecha = forms.DateInput()
