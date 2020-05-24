from django.utils.translation import gettext as _
from django.db import models

# Torneo

# Estado Torneo

CREACION = 0
ACTIVO = 1
TERMINADO = 2

ESTADO_TORNEO_CHOICES = (
	(CREACION, _("Creación")),
	(ACTIVO, _("Activo")),
	(TERMINADO, _("Terminado"))

)


class Deporte(models.TextChoices):
	FUTBOL = 'futbol', _("Fútbol")
	BALONCESTO = 'baloncesto', _("Baloncesto")
	VOLEIBOL = 'voleibol', _("Voleibol")
	BALONMANO = 'balonmano', _("Balonmano")
	WATERPOLO = 'waterpolo', _("Waterpolo")
	TENIS = 'tenis', _("Tenis")


# Fase
ELIMINATORIA = 1
LIGA = 2

# Tipo de Torneo
TIPO_TORNEO = (
	(1, _("Liga")),
	(2, _("Eliminatoria")),
	(3, _("Fase de grupos y eliminatorias"))
)
