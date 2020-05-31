from django import forms
from .models import *
from cubogt.static.constantes import *


class TorneoForm(forms.ModelForm):
	class Meta:
		model = Torneo
		fields = ('deporte', 'nombre', 'fecha', 'descripcion','numero_equipos')

	fecha = forms.DateInput()


class EquipoForm(forms.ModelForm):
	class Meta:
		model = Equipo
		fields = ('nombre', 'correo')
