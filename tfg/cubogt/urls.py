from django.urls import *
from cubogt import views

urlpatterns = [
	path('', views.index, name='index'),
	path('mis_torneos/', views.torneo_lista, name='lista_torneo'),
	path('nuevo_torneo/', views.torneo_nuevo, name='nuevo_torneo'),
	path('torneo/<int:torneo_id>/', views.torneo_ver, name='torneo'),
	path('torneo/<int:torneo_id>/editar', views.torneo_editar, name='torneo_editar'),
	path('torneo/<int:torneo_id>/borrar', views.torneo_borrar, name='torneo_borrar'),

	path('torneo/<int:torneo_id>/equipos', views.equipo_lista, name='equipo_lista'),
	path('torneo/<int:torneo_id>/equipo/nuevo', views.equipo_nuevo, name='equipo_nuevo'),
	path('torneo/<int:torneo_id>/equipo/<int:equipo_id>/editar', views.equipo_editar, name='equipo_editar'),
	path('torneo/<int:torneo_id>/equipo/<int:equipo_id>/borrar', views.equipo_borrar, name='equipo_borrar'),

	path('torneo/<int:torneo_id>/campos', views.campo_lista, name='campo_lista'),
	path('torneo/<int:torneo_id>/campo/nuevo', views.campo_nuevo, name='campo_nuevo'),
	path('torneo/<int:torneo_id>/campo/<int:campo_id>/editar', views.campo_editar, name='campo_editar'),
	path('torneo/<int:torneo_id>/campo/<int:campo_id>/borrar', views.campo_borrar, name='campo_borrar'),

]

"""
path('post/<int:pk>/', views.post_detail, name='post_detail'),
path('post/new/', views.post_new, name='post_new'),
path('post/<int:pk>/edit/', views.post_edit, name='post_new'),
path('drafts/', views.post_draft_list, name='post_draft_list'),
path('post/<pk>/publish/', views.post_publish, name='post_publish'),
path('post/<pk>/delete', views.post_delete, name='post_remove'),
"""
