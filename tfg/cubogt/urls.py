from django.urls import *

from cubogt.views import *


urlpatterns = [
	path('', torneo_views.torneo_lista, name='index'),
	path('mis_torneos/', torneo_views.torneo_lista, name='lista_torneo'),
	path('nuevo_torneo/', torneo_views.torneo_nuevo, name='nuevo_torneo'),
	path('torneo/<int:torneo_id>/', torneo_views.torneo_ver, name='torneo'),
	path('torneo/<int:torneo_id>/editar', torneo_views.torneo_editar, name='torneo_editar'),
	path('torneo/<int:torneo_id>/borrar', torneo_views.torneo_borrar, name='torneo_borrar'),

	path('torneo/<int:torneo_id>/equipo', equipo_views.equipo_lista, name='equipo_lista'),
	path('torneo/<int:torneo_id>/equipo/nuevo', equipo_views.equipo_nuevo, name='equipo_nuevo'),
	path('torneo/<int:torneo_id>/equipo/<int:equipo_id>/editar', equipo_views.equipo_editar, name='equipo_editar'),
	path('torneo/<int:torneo_id>/equipo/<int:equipo_id>/borrar', equipo_views.equipo_borrar, name='equipo_borrar'),

	path('torneo/<int:torneo_id>/campo', campo_views.campo_lista, name='campo_lista'),
	path('torneo/<int:torneo_id>/campo/nuevo', campo_views.campo_nuevo, name='campo_nuevo'),
	path('torneo/<int:torneo_id>/campo/generar', campo_views.campo_generar, name='campo_generar'),
	path('torneo/<int:torneo_id>/campo/<int:campo_id>/editar', campo_views.campo_editar, name='campo_editar'),
	path('torneo/<int:torneo_id>/campo/<int:campo_id>/borrar', campo_views.campo_borrar, name='campo_borrar'),

	path('torneo/<int:torneo_id>/fase', fase_views.fase_lista, name='fase_lista'),
	path('torneo/<int:torneo_id>/fase/nueva', fase_views.fase_nueva, name='fase_nueva'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/editar', fase_views.fase_editar, name='fase_editar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/borrar', fase_views.fase_borrar, name='fase_borrar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>', fase_views.fase_ver, name='fase_ver'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ver_equipos', fase_views.fase_equipo_lista, name='fase_equipo_lista'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/editar_equipos', fase_views.fase_equipo_editar, name='fase_equipo_editar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ver_equipos/añadir_todos', fase_views.fase_equipo_agregar_todo, name='fase_equipo_agregar_todo'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ver_equipos/borrar_todos', fase_views.fase_equipo_borrar_todo, name='fase_equipo_borrar_todo'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ver_equipos/borrar/<int:equipo_id>', fase_views.fase_equipo_borrar, name='fase_equipo_borrar'),

	path('torneo/<int:torneo_id>/fase_iniciar', fase_views.fase_iniciar_lista, name='fase_iniciar_lista'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/iniciar', fase_views.fase_iniciar, name='fase_iniciar'),

	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo', grupo_views.grupo_lista, name='grupo_lista'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/nuevo', grupo_views.grupo_nuevo, name='grupo_nuevo'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/generar', grupo_views.grupo_generar, name='grupo_generar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/editar', grupo_views.grupo_editar, name='grupo_editar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/borrar', grupo_views.grupo_borrar, name='grupo_borrar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/ver_equipos', grupo_views.grupo_equipo_lista, name='grupo_equipo_lista'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/ver_equipos/#grupo<int:grupo_id>', grupo_views.grupo_equipo_lista_especifico, name='grupo_equipo_lista_especifico'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/ver_equipos/repartir_equipos', grupo_views.grupo_repartir_equipos, name='grupo_repartir_equipos'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/ver_equipos/borrar_todos', grupo_views.grupo_equipo_borrar_todo, name='grupo_equipo_borrar_todo'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/editar_equipos', grupo_views.grupo_equipo_editar, name='grupo_equipo_editar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/borrar_equipo/<int:equipo_id>', grupo_views.grupo_equipo_borrar, name='grupo_equipo_borrar'),

	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ascenso', ascenso_views.ascenso_lista, name='ascenso_lista'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ascenso/nuevo', ascenso_views.ascenso_nuevo, name='ascenso_nuevo'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ascenso/nuevo_general', ascenso_views.ascenso_nuevo_general, name='ascenso_nuevo_general'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ascenso/borrar_todo', ascenso_views.ascenso_borrar_todo, name='ascenso_borrar_todo'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ascenso/<int:ascenso_id>/editar', ascenso_views.ascenso_editar, name='ascenso_editar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/ascenso/<int:ascenso_id>/borrar', ascenso_views.ascenso_borrar, name='ascenso_borrar'),

	#FASE INICIADA
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/partidos_enjuego', partido_views.partido_enjuego, name='partido_enjuego'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/partidos_enjuego/<int:partido_id>/posponer', partido_views.partido_posponer, name='partido_posponer'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/partidos_enjuego/<int:partido_id>/forzar_campo/<int:campo_id>', partido_views.partido_forzar, name='partido_forzar'),

	path('torneo/<int:torneo_id>/fase/<int:fase_id>/clasificacion', clasificacion_views.clasificacion_ver, name='clasificacion_ver'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/clasificacion/grupo/<int:grupo_id>', clasificacion_views.clasificacion_ver, name='clasificacion_ver'),

	path('torneo/<int:torneo_id>/fase/<int:fase_id>/calendario', partido_views.partido_calendario, name='partido_calendario'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/calendario/grupo/<int:grupo_id>', partido_views.partido_calendario_grupo, name='partido_calendario_grupo'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/calendario/grupo/<int:grupo_id>#partido<int:partido_id>', partido_views.partido_calendario_grupo_especifico, name='partido_calendario_grupo'),

	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/partido/<int:partido_id>', partido_views.partido_ver, name='partido_ver'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/partido/<int:partido_id>/editar_resultado', partido_views.partido_editar_resultado, name='partido_editar_resultado'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/partido/<int:partido_id>/terminar', partido_views.partido_terminar, name='partido_terminar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/partido/<int:partido_id>/set/nuevo', partido_views.partido_set_nuevo, name='partido_set_nuevo'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/partido/<int:partido_id>/set/<int:set_id>/editar', partido_views.partido_set_editar, name='partido_set_editar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/grupo/<int:grupo_id>/partido/<int:partido_id>/set/<int:set_id>/borrar', partido_views.partido_set_borrar, name='partido_set_borrar'),


	path('torneo/<int:torneo_id>/fase/<int:fase_id>/campo', campo_views.campo_fase_lista, name='campo_fase_lista'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/campo/editar', campo_views.campo_fase_editar, name='campo_fase_editar'),
	path('torneo/<int:torneo_id>/fase/<int:fase_id>/campo/<int:campo_id>/borrar', campo_views.campo_fase_borrar, name='campo_fase_borrar'),



]

'''
path('post/<int:pk>/', views.post_detail, name='post_detail'),
path('post/new/', views.post_new, name='post_new'),
path('post/<int:pk>/edit/', views.post_edit, name='post_new'),
path('drafts/', views.post_draft_list, name='post_draft_list'),
path('post/<pk>/publish/', views.post_publish, name='post_publish'),
path('post/<pk>/delete', views.post_delete, name='post_remove'),
'''
