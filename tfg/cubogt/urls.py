from django.urls import *
from cubogt import views

urlpatterns = [
	path('', views.index, name='index'),
	path('mis_torneos/', views.lista_torneo, name='lista_torneo'),
	path('nuevo_torneo/', views.nuevo_torneo, name='nuevo_torneo'),
	path('torneo/<int:pk>/', views.torneo2, name='torneo'),
]
# path('nuevo_torneo/<id>/liga/', views.nueva_liga, name='nueva_liga'),
"""
path('post/<int:pk>/', views.post_detail, name='post_detail'),
path('post/new/', views.post_new, name='post_new'),
path('post/<int:pk>/edit/', views.post_edit, name='post_new'),
path('drafts/', views.post_draft_list, name='post_draft_list'),
path('post/<pk>/publish/', views.post_publish, name='post_publish'),
path('post/<pk>/delete', views.post_delete, name='post_remove'),
"""
