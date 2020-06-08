from django import forms
from .models import *
from cubogt.static.constantes import *
from django.utils.translation import gettext as _


class TorneoForm(forms.ModelForm):
	class Meta:
		model = Torneo
		fields = ('deporte', 'nombre', 'fecha', 'descripcion', 'numero_equipos_max')

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
		fields = ('nombre', 'tipo_fase', 'numero_equipos_max', 'doble_partido')


# def __init__(self, *args, **kwargs):
# TODO: unificar FaseSetForm FasePuntoForm self.fields['numero_sets'].disabled


class FaseSetForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('numero_sets',)


class FasePuntoForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('numero_puntos', 'puntos_maximos')


class FaseEquipoForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('equipos',)

	def __init__(self, *args, **kwargs):
		torneo = kwargs.pop('torneo')
		super(FaseEquipoForm, self).__init__(*args, **kwargs)
		self.fields['equipos'].queryset = Equipo.objects.filter(torneo=torneo)
# TODO?: Preguntar si quiero excluir a los equipos que ya están dentro de la fase del torneo


class GrupoForm(forms.ModelForm):
	class Meta:
		model = Grupo
		fields = ('nombre',)


class GrupoGenerarForm(forms.Form):
	numero_grupos = forms.IntegerField(label=_("Número de grupos"), min_value=1)
	tipo_nombre = forms.ChoiceField(label=_("Nomenclatura"), choices=GENERAR_GRUPOS_CHOICES)


class GrupoEquipoForm(forms.ModelForm):
	class Meta:
		model = Grupo
		fields = ('equipos',)

	def __init__(self, *args, **kwargs):
		fase = kwargs.pop('fase')
		grupo = kwargs.pop('grupo')
		grupo_list = Grupo.objects.filter(fase=fase).exclude(id=grupo.id)
		super(GrupoEquipoForm, self).__init__(*args, **kwargs)
		self.fields['equipos'].queryset = Equipo.objects.filter(fase=fase).exclude(grupo__in=grupo_list)
# TODO?: Preguntar si quiero excuir a los equipos que ya estan dentro de un grupo de la fase
