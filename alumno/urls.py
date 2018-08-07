# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^alumno-list/$', views.AlumnoListView.as_view(), name='alumno-list'),
	url(r'^alumno-new(?:/(?P<next>[\w\-]+))?/$', views.AlumnoCreateView.as_view(), name='alumno-new' ),
	url(r'^alumno-edit/(?P<id>[\w\-]+)/$', views.AlumnoUpdateView.as_view(), name='alumno-edit' ),
	url(r'^alumno-edit-password/(?P<id>[\w\-]+)/$', views.AlumnoPasswordUpdateView.as_view(), name='alumno-edit-password' ),
	url(r'^alumno-delete/(?P<id>[\w\-]+)/$', views.AlumnoDeleteView.as_view(), name='alumno-delete' ),

	url(r'^alumno-seguimiento/$', views.AlumnoProcesosListView.as_view(), name='alumno-seguimiento'),
	url(r'^alumno-tramite/$', views.AlumnoTramiteCreate.as_view(), name='alumno-tramite'),

	url(r'^proceso-alumno-new/$', views.ProcesoAlumnoCreateView.as_view(), name='alumno-proceso-new'),
	url(r'^proceso-alumno-edit/(?P<id>[\w\-]+)/$', views.ProcesoAlumnoEditView.as_view(), name='alumno-proceso-edit'),

	url(r'^proceso-item-new/$', views.ProcesoAlumnoItemsCreateView.as_view(), name='alumno-proceso-item-new'),
]