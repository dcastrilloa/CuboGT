from django import forms
from .models import *
from cubogt.static.constantes import *


class TorneoForm(forms.ModelForm):
	class Meta:
		model = Torneo
		fields = ('deporte', 'nombre', 'fecha', 'descripcion', 'numero_equipos')
	fecha = forms.DateInput()


class EquipoForm(forms.ModelForm):
	class Meta:
		model = Equipo
		fields = ('nombre', 'correo')


class CampoForm(forms.ModelForm):
	class Meta:
		model = Campo
		fields = ('nombre',)


class FaseForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('nombre', 'tipo_fase', 'numero_equipos','doble_partido')


class FaseSetForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('numero_sets',)


class FasePuntoForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('numero_puntos', 'puntos_maximos')

