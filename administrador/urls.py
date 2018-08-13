# -*- coding: utf-8 -*-
from django.conf.urls import url
from axes.decorators import watch_login
from . import views

urlpatterns = [
	url(r'^login/$', watch_login(views.LoginView.as_view()), name='administrador-login'),
	url(r'^logout/$', watch_login(views.LogoutView.as_view()), name='administrador-logout'),
	url(r'^locked/$', views.LockedOutView.as_view(), name='locked_out'),
	#
	url(r'^users-list/$', views.UsersListView.as_view(), name='administrador-users-list'),
	url(r'^user-new/$', views.UserCreate.as_view(), name='administrador-user-new'),
	url(r'^user-edit/(?P<username>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.UserUpdate.as_view(), name='administrador-user-edit'),
	url(r'^user-edit-password/(?P<username>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.UserUpdatePassword.as_view(), name='administrador-user-edit-password'),
	#
	url(r'^permissions-list/$', views.PermissionsListView.as_view(), name='administrador-permissions-list'),
	url(r'^permission-new/$', views.PermissionCreate.as_view(), name='administrador-permission-new'),
	url(r'^permission-edit/(?P<codename>[\w\-\_\.]+)/$', views.PermissionUpdate.as_view(), name='administrador-permission-edit'),
	url(r'^permission-delete/(?P<codename>[\w\-\_\.]+)/$', views.PermissionDelete.as_view(), name='administrador-permission-delete'),
	#
	url(r'^groups-list/$', views.GroupsListView.as_view(), name='administrador-groups-list'),
	url(r'^group-new/$', views.GroupCreate.as_view(), name='administrador-group-new'),
	url(r'^group-edit/(?P<id>[\d\-]+)/$', views.GroupUpdate.as_view(), name='administrador-group-edit'),
	url(r'^group-delete/(?P<id>[\d\-]+)/$', views.GroupDelete.as_view(), name='administrador-group-delete'),

	url(r'^faculties-list/$', views.FacultadListView.as_view(), name='administrador-faculties-list'),
	url(r'^faculties-new/$', views.FacultadCreate.as_view(), name='administrador-faculties-new'),
	url(r'^faculties-edit/(?P<id>[\d\-]+)/$', views.FacultadUpdate.as_view(), name='administrador-faculties-edit'),
	url(r'^faculties-delete/(?P<id>[\d\-]+)/$', views.FacultadDelete.as_view(), name='administrador-faculties-delete'),

	url(r'^carrera-list/$', views.CarreraListView.as_view(), name='administrador-carrera-list'),
	url(r'^carrera-new/$', views.CarreraCreate.as_view(), name='administrador-carrera-new'),
	url(r'^carrera-edit/(?P<id>[\d\-]+)/$', views.CarreraUpdate.as_view(), name='administrador-carrera-edit'),
	url(r'^carrera-delete/(?P<id>[\d\-]+)/$', views.CarreraDelete.as_view(), name='administrador-carrera-delete'),

	url(r'^ciclo-list/$', views.CicloListView.as_view(), name='administrador-ciclo-list'),
	url(r'^ciclo-new/$', views.CicloCreate.as_view(), name='administrador-ciclo-new'),
	url(r'^ciclo-edit/(?P<id>[\d\-]+)/$', views.CicloUpdate.as_view(), name='administrador-ciclo-edit'),
	url(r'^ciclo-delete/(?P<id>[\d\-]+)/$', views.CicloDelete.as_view(), name='administrador-ciclo-delete'),

	url(r'^materia-list/$', views.MateriaListView.as_view(), name='administrador-materia-list'),
	url(r'^materia-new/$', views.MateriaCreate.as_view(), name='administrador-materia-new'),
	url(r'^materia-edit/(?P<id>[\d\-]+)/$', views.MateriaUpdate.as_view(), name='administrador-materia-edit'),
	url(r'^materia-delete/(?P<id>[\d\-]+)/$', views.MateriaDelete.as_view(), name='administrador-materia-delete'),

	url(r'^periodo-list/$', views.PeriodoListView.as_view(), name='administrador-periodo-list'),
	url(r'^periodo-new/$', views.PeriodoCreate.as_view(), name='administrador-periodo-new'),
	url(r'^periodo-edit/(?P<id>[\d\-]+)/$', views.PeriodoUpdate.as_view(), name='administrador-periodo-edit'),
	url(r'^periodo-delete/(?P<id>[\d\-]+)/$', views.PeriodoDelete.as_view(), name='administrador-periodo-delete'),

	url(r'^proceso-list/$', views.ProcesoListView.as_view(), name='administrador-proceso-list'),
	url(r'^proceso-new/$', views.ProcesoCreate.as_view(), name='administrador-proceso-new'),
	url(r'^proceso-view/(?P<id>[\d\-]+)/$', views.ProcesoView.as_view(), name='administrador-proceso-view'),
	url(r'^proceso-edit/(?P<id>[\d\-]+)/$', views.ProcesoUpdate.as_view(), name='administrador-proceso-edit'),
	url(r'^proceso-delete/(?P<id>[\d\-]+)/$', views.ProcesoDelete.as_view(), name='administrador-proceso-delete'),
	
	url(r'^proceso-item-list/$', views.ProcesoItemsListView.as_view(), name='administrador-proceso-item-list'),
	url(r'^proceso-item-new/$', views.ProcesoItemCreate.as_view(), name='administrador-proceso-item-new'),
	url(r'^proceso-item-edit/(?P<id>[\d\-]+)/$', views.ProcesoItemUpdate.as_view(), name='administrador-proceso-item-edit'),
	url(r'^proceso-item-delete/(?P<id>[\d\-]+)/$', views.ProcesoItemDelete.as_view(), name='administrador-proceso-item-delete'),


]