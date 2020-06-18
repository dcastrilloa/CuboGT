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

# Estado Ascenso
ERROR = 1
REALIZADO = 2

ESTADO_ASCENSO_CHOICES = (
	(ESPERA, _("espera")),
	(ERROR, _("Tiene error")),
	(REALIZADO, _("Realizado"))
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

GENERAR_CAMPOS_CHOICES = GENERAR_GRUPOS_CHOICES

# ELIMINATORIA
TERCER_PUESTO = 3
NOMBRE_ELIMINATORIA = {
	1: _(" Final"),
	3: _(" 3º y 4º puesto"),
	2: _(" Semifinal"),
	4: _(" Cuartos de final"),
	8: _(" Octavos de final"),
	16: _(" Dieciseisavos de final"),
	32: _(" Treintaidosavos de final"),
	64: _(" Sesentaicuatroavos de final"),
	128: _(" 128avos de final"),
	256: _(" 255avos de final"),
}
