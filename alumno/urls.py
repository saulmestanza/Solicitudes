# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^alumno-create/$', views.AlumnoCreate.as_view(), name='alumno-create'),

	url(r'^alumno-seguimiento/$', views.AlumnoHistorialListView.as_view(), name='alumno-seguimiento'),
	url(r'^alumno-tramite/$', views.AlumnoTramiteCreate.as_view(), name='alumno-tramite'),
]