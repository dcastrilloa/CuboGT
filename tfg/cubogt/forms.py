from django import forms
from .models import *
from cubogt.static.constantes import *


class TorneoForm(forms.ModelForm):
	class Meta:
		model = Torneo
		fields = ('deporte', 'nombre', 'fecha', 'descripcion')

	fecha = forms.DateInput()
