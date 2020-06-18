from django.urls import *
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('', include('django.contrib.auth.urls')),
]