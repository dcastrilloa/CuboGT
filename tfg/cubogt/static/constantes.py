from django.utils.translation import gettext as _
from django.db import models

# Torneo

# Estado Torneo y Fase

CREACION = 0
ACTIVO = 1
TERMINADO = 2

ESTADO_CHOICES = (
	(CREACION, _("Creación")),
	(ACTIVO, _("Activo")),
	(TERMINADO, _("Terminado"))

)

# Estado Partido
ESPERA = 0
JUGANDO = 1

ESTADO_PARTIDO_CHOICES = (
	(ESPERA, _("En espera")),
	(JUGANDO, _("Jugándose")),
	(TERMINADO, _("Terminado"))

)


class DeporteChoices(models.TextChoices):
	FUTBOL = 'futbol', _("Fútbol")
	BALONCESTO = 'baloncesto', _("Baloncesto")
	VOLEIBOL = 'voleibol', _("Voleibol")
	BALONMANO = 'balonmano', _("Balonmano")
	WATERPOLO = 'waterpolo', _("Waterpolo")
	TENIS = 'tenis', _("Tenis")


# Fase
LIGA = 1
ELIMINATORIA = 2

TIPO_FASE = (
	(1, _("Liga")),
	(2, _("Eliminatoria"))
)

# Tipo de Torneo
TIPO_TORNEO = (
	(1, _("Liga")),
	(2, _("Eliminatoria")),
	(3, _("Fase de grupos y eliminatorias"))
)


ABECEDARIO = '1'
NUMEROS = '2'
GENERAR_GRUPOS_CHOICES = (
	(ABECEDARIO, _("Abecedario")),
	(NUMEROS, _("Numeros"))
)
