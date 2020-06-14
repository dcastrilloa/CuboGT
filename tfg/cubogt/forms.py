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


class CampoGenerarForm(forms.Form):
	numero_campos = forms.IntegerField(label=_("Número de campos"), min_value=1, max_value=26)
	tipo_nombre = forms.ChoiceField(label=_("Nomenclatura"), choices=GENERAR_CAMPOS_CHOICES)


class FaseForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('nombre', 'tipo_fase', 'numero_equipos_max', 'doble_partido')


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


class FaseCampoForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ('campos',)

	def __init__(self, *args, **kwargs):
		torneo = kwargs.pop('torneo')
		fase = kwargs.pop('fase')
		otras_fases_activas = Fase.objects.filter(torneo=torneo, estado=ACTIVO).exclude(id=fase.id)
		super(FaseCampoForm, self).__init__(*args, **kwargs)
		self.fields['campos'].queryset = Campo.objects.filter(torneo=torneo).exclude(fase__in=otras_fases_activas)


class GrupoForm(forms.ModelForm):
	class Meta:
		model = Grupo
		fields = ('nombre',)


class GrupoGenerarForm(forms.Form):
	numero_grupos = forms.IntegerField(label=_("Número de grupos"), min_value=1, max_value=26)
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


class AscensoForm(forms.ModelForm):
	class Meta:
		model = Ascenso
		fields = ['grupo', 'desde_posicion', 'numero_equipos', 'proxima_fase']

	def __init__(self, *args, **kwargs):
		fase = kwargs.pop('fase')
		fase_list = Fase.objects.filter(torneo=fase.torneo, estado=CREACION).exclude(id=fase.id)
		grupo_list = Grupo.objects.filter(fase=fase)
		super(AscensoForm, self).__init__(*args, **kwargs)
		self.fields['proxima_fase'].queryset = fase_list
		self.fields['grupo'].queryset = grupo_list


class AscensoGeneralForm(forms.ModelForm):
	class Meta:
		model = Ascenso
		fields = ['desde_posicion', 'numero_equipos', 'proxima_fase']

	def __init__(self, *args, **kwargs):
		fase = kwargs.pop('fase')
		fase_list = Fase.objects.filter(torneo=fase.torneo, estado=CREACION).exclude(id=fase.id)
		super(AscensoGeneralForm, self).__init__(*args, **kwargs)
		self.fields['proxima_fase'].queryset = fase_list

