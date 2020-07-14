from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import SelectDateWidget, SelectMultiple

from .models import *
from cubogt.static.constantes import *
from django.utils.translation import gettext as _


class TorneoForm(forms.ModelForm):
	class Meta:
		model = Torneo
		fields = ['deporte', 'nombre', 'fecha', 'descripcion', 'numero_equipos_max']

	fecha = forms.DateInput()

	def __init__(self, *args, **kwargs):
		super(TorneoForm, self).__init__(*args, **kwargs)
		self.fields['numero_equipos_max'].widget.attrs['min'] = 2
		# self.fields['fecha'].widget = SelectDateWidget()


class EquipoForm(forms.ModelForm):
	class Meta:
		model = Equipo
		fields = ['nombre', 'correo']

	def __init__(self, *args, **kwargs):
		self.torneo = kwargs.pop('torneo')
		self.editar = kwargs.pop('editar')
		if self.editar:
			self.equipo = kwargs.pop('equipo')
		super(EquipoForm, self).__init__(*args, **kwargs)

	def clean_nombre(self):
		nombre = self.cleaned_data['nombre']
		equipo_repetido_list = Equipo.objects.filter(torneo=self.torneo, nombre__iexact=nombre)
		if self.editar:
			equipo_repetido_list = equipo_repetido_list.exclude(id=self.equipo.id)
		if equipo_repetido_list:
			raise forms.ValidationError(_("Ya existe un equipo con el nombre: %(equipo)s, escoja otro nombre.\n") %
								 {'equipo': nombre})
		return nombre


class CampoForm(forms.ModelForm):
	class Meta:
		model = Campo
		fields = ['nombre']


class CampoGenerarForm(forms.Form):
	numero_campos = forms.IntegerField(label=_("Número de campos"), min_value=1, max_value=26)
	tipo_nombre = forms.ChoiceField(label=_("Nomenclatura"), choices=GENERAR_CAMPOS_CHOICES)


class FaseForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ['nombre', 'tipo_fase', 'numero_equipos_max', 'doble_partido']

	def __init__(self, *args, **kwargs):
		super(FaseForm, self).__init__(*args, **kwargs)
		self.fields['numero_equipos_max'].widget.attrs['min'] = 2


class FaseSetForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ['numero_sets']

	def __init__(self, *args, **kwargs):
		super(FaseSetForm, self).__init__(*args, **kwargs)
		self.fields['numero_sets'].widget.attrs['min'] = 1


class FasePuntoForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ['numero_puntos', 'puntos_maximos']

	def __init__(self, *args, **kwargs):
		super(FasePuntoForm, self).__init__(*args, **kwargs)
		self.fields['numero_puntos'].widget.attrs['min'] = 1
		self.fields['puntos_maximos'].widget.attrs['min'] = 1

	def clean(self):
		cleaned_data = super().clean()
		numero_puntos = cleaned_data.get("numero_puntos")
		puntos_maximos = cleaned_data.get("puntos_maximos")
		if puntos_maximos and puntos_maximos < numero_puntos:
			msg = _("Los puntos máximos tienen que ser mayores o iguales al numero de puntos.")
			self.add_error('puntos_maximos', msg)


class FaseEquipoForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ['equipos']

	def __init__(self, *args, **kwargs):
		torneo = kwargs.pop('torneo')
		super(FaseEquipoForm, self).__init__(*args, **kwargs)
		self.fields['equipos'].queryset = Equipo.objects.filter(torneo=torneo)


class FaseCampoForm(forms.ModelForm):
	class Meta:
		model = Fase
		fields = ['campos']

	def __init__(self, *args, **kwargs):
		torneo = kwargs.pop('torneo')
		fase = kwargs.pop('fase')
		otras_fases_activas = Fase.objects.filter(torneo=torneo, estado=ACTIVO).exclude(id=fase.id)
		super(FaseCampoForm, self).__init__(*args, **kwargs)
		self.fields['campos'].queryset = Campo.objects.filter(torneo=torneo).exclude(fase__in=otras_fases_activas)


class GrupoForm(forms.ModelForm):
	class Meta:
		model = Grupo
		fields = ['nombre']


class GrupoGenerarForm(forms.Form):
	numero_grupos = forms.IntegerField(label=_("Número de grupos"), min_value=1, max_value=26)
	tipo_nombre = forms.ChoiceField(label=_("Nomenclatura"), choices=GENERAR_GRUPOS_CHOICES)


class GrupoEquipoForm(forms.ModelForm):
	class Meta:
		model = Grupo
		fields = ['equipos']

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
		self.fields['desde_posicion'].widget.attrs['min'] = 1
		self.fields['numero_equipos'].widget.attrs['min'] = 1


class AscensoGeneralForm(forms.ModelForm):
	class Meta:
		model = Ascenso
		fields = ['desde_posicion', 'numero_equipos', 'proxima_fase']

	def __init__(self, *args, **kwargs):
		fase = kwargs.pop('fase')
		fase_list = Fase.objects.filter(torneo=fase.torneo, estado=CREACION).exclude(id=fase.id)
		super(AscensoGeneralForm, self).__init__(*args, **kwargs)
		self.fields['proxima_fase'].queryset = fase_list
		self.fields['desde_posicion'].widget.attrs['min'] = 1
		self.fields['numero_equipos'].widget.attrs['min'] = 1


class PartidoResultadoForm(forms.ModelForm):
	class Meta:
		model = Partido
		fields = ['resultado_local', 'resultado_visitante']

	def __init__(self, *args, **kwargs):
		super(PartidoResultadoForm, self).__init__(*args, **kwargs)
		self.fields['resultado_local'].widget.attrs['min'] = 0
		self.fields['resultado_visitante'].widget.attrs['min'] = 0


class SetJuegosForm(forms.ModelForm):
	class Meta:
		model = Set
		fields = ['juegos_local', 'juegos_visitante']

	def __init__(self, *args, **kwargs):
		partido = kwargs.pop('partido')
		super(SetJuegosForm, self).__init__(*args, **kwargs)
		self.fields['juegos_local'].label = _("Juegos de %(equipo)s") % {'equipo': partido.equipo_local}
		self.fields['juegos_visitante'].label = _("Juegos de %(equipo)s") % {'equipo': partido.equipo_visitante}

		self.fields['juegos_visitante'].widget.attrs['min'] = 0
		self.fields['juegos_local'].widget.attrs['min'] = 0
		self.fields['juegos_visitante'].widget.attrs['max'] = 7
		self.fields['juegos_local'].widget.attrs['max'] = 7

	def clean(self):
		cleaned_data = super().clean()
		juegos_local = cleaned_data.get("juegos_local")
		juegos_visitante = cleaned_data.get("juegos_visitante")
		if juegos_local != juegos_visitante:
			if juegos_local == 7 or juegos_visitante == 7:
				if abs(juegos_local-juegos_visitante) > 2:
					msg = _("Solo puede haber una diferencia de 1 o 2 juegos.")
					self.add_error('juegos_local', msg)
			elif juegos_local == 6 or juegos_visitante == 6:
				if abs(juegos_local-juegos_visitante) == 1:
					msg = _("No puede haber una diferencia de 1 juego.")
					self.add_error('juegos_local', msg)
			else:
				msg = _("Ningún jugador ha ganado el set.")
				self.add_error('juegos_local', msg)
		else:
			msg = _("No se puede introducir un empate.")
			self.add_error('juegos_local', msg)


class SetPuntosForm(forms.ModelForm):
	class Meta:
		model = Set
		fields = ['puntos_local', 'puntos_visitante']

	def __init__(self, *args, **kwargs):
		self.fase = kwargs.pop('fase')
		partido = kwargs.pop('partido')
		super(SetPuntosForm, self).__init__(*args, **kwargs)
		self.fields['puntos_local'].label = _("Puntos de %(equipo)s") % {'equipo': partido.equipo_local}
		self.fields['puntos_visitante'].label = _("Puntos de %(equipo)s") % {'equipo': partido.equipo_visitante}

		self.fields['puntos_local'].widget.attrs['min'] = 0
		self.fields['puntos_visitante'].widget.attrs['min'] = 0
		if self.fase.puntos_maximos:
			self.fields['puntos_local'].widget.attrs['max'] = self.fase.puntos_maximos
			self.fields['puntos_visitante'].widget.attrs['max'] = self.fase.puntos_maximos

	def clean(self):
		cleaned_data = super().clean()
		puntos_local = cleaned_data.get("puntos_local")
		puntos_visitante = cleaned_data.get("puntos_visitante")
		# Comprobar fin de set
		if (self.fase.numero_puntos <= puntos_local) or (self.fase.numero_puntos <= puntos_visitante):
			if abs(puntos_local - puntos_visitante) == 0:
				msg = _("No se puede introducir un empate.")
				self.add_error('puntos_local', msg)
			else:  # Partido alcanza los puntos
				if (self.fase.numero_puntos < puntos_local) or (self.fase.numero_puntos < puntos_visitante):
					# Superando el limite de fase.numero_puntos
					if puntos_local == self.fase.puntos_maximos or self.fase.puntos_maximos == puntos_visitante:
						if abs(puntos_local - puntos_visitante) > 2:
							msg = _("Al haber alcanzado la puntuacion máxima del set (%(puntos_maximos)d puntos) solo puede existir diferencia de uno o dos puntos.") % {'puntos_maximos': self.fase.puntos_maximos}
							self.add_error('puntos_local', msg)
					else:
						if abs(puntos_local - puntos_visitante) != 2:
							msg = _("Solo puede haber diferencia de 2 puntos.")
							self.add_error('puntos_local', msg)
				else:  # Igualando el fase.numero_puntos
					if abs(puntos_local-puntos_visitante) < 2:
						if abs(puntos_local-puntos_visitante) == 1:
							msg = _("No puede haber un punto de diferencia.")
		else:
			msg = _("Ningún equipo ha alcanzado los %(n_puntos)d puntos.") % {'n_puntos': self.fase.numero_puntos}
			self.add_error('puntos_local', msg)
