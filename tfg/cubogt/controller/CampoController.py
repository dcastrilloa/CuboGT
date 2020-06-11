from django.utils.translation import gettext_lazy as _
from cubogt.models import Campo


def comprobar_campo(torneo):
	msg_error = []
	campo_list = Campo.objects.filter(torneo=torneo)
	if not campo_list:
		msg_error.append(_("Tienes que crear al menos un campo para poder iniciar el torneo.\n"))
	return msg_error
