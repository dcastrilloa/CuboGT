from django.shortcuts import redirect


# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect('lista_torneo')
	else:
		return redirect('login')
