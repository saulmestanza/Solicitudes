# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^alumno-activate/(?P<token>[\w\-]+)/(?P<username>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.AlumnoActivateView.as_view(), name="alumno-activate"),
	url(r'^alumno-resend/$', views.AlumnoResendView.as_view(), name='alumno-resend'),
	url(r'^alumno-reset/$', views.AlumnoResetView.as_view(), name='alumno-reset'),
	url(r'^alumno-list/$', views.AlumnoListView.as_view(), name='alumno-list'),
	url(r'^alumno-new(?:/(?P<next>[\w\-]+))?/$', views.AlumnoCreateView.as_view(), name='alumno-new' ),
	url(r'^alumno-new-account/$', views.AlumnoNewCreateView.as_view(), name='alumno-new-account' ),
	url(r'^alumno-edit/(?P<id>[\w\-]+)/$', views.AlumnoUpdateView.as_view(), name='alumno-edit' ),
	url(r'^alumno-edit-password/(?P<id>[\w\-]+)/$', views.AlumnoPasswordUpdateView.as_view(), name='alumno-edit-password' ),
	url(r'^alumno-delete/(?P<id>[\w\-]+)/$', views.AlumnoDeleteView.as_view(), name='alumno-delete' ),

	url(r'^alumno-seguimiento/$', views.AlumnoSeguimientoListView.as_view(), name='alumno-seguimiento'),
	url(r'^alumno-seguimiento-historial/(?P<id>[\w\-]+)/$', views.HistorialCreateView.as_view(), name='alumno-seguimiento-historial'),
	url(r'^alumno-seguimiento-edit/(?P<id>[\w\-]+)/$', views.AlumnoSeguimientoItemUpdateView.as_view(), name='alumno-seguimiento-edit'),
	url(r'^alumno-tramite/$', views.AlumnoTramiteCreate.as_view(), name='alumno-tramite'),
	url(r'^alumno-seguimiento-documento/(?P<id>[\w\-]+)/$', views.HistorialStreamFilesView.as_view(), name='alumno-seguimiento-documento'),

	url(r'^proceso-alumno-new/$', views.ProcesoAlumnoCreateView.as_view(), name='alumno-proceso-new'),

	url(r'^proceso-item-new/$', views.ProcesoAlumnoItemsCreateView.as_view(), name='alumno-proceso-item-new'),
	url(r'^proceso-item-delete/(?P<id>[\w\-]+)/$', views.ProcesoAlumnoItemsDeleteView.as_view(), name='alumno-proceso-item-delete'),
]