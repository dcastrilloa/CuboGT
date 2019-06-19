from django.utils.translation import gettext as _

# Torneo
CREACION = 1
ACTIVO = 2
TERMINADO = 3


# Fase
ELIMINATORIA = 1
LIGA = 2

# Tipo de Torneo
TIPO_TORNEO = (
	(1, _("Liga")),
	(2, _("Eliminatoria")),
	(3, _("Fase de grupos y eliminatorias"))
)
