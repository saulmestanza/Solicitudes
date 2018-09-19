# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^carreras/(?P<id>[\d]+)/$', views.CarrerasAPIView.as_view(), name="carreras-api"),
	url(r'^ciclos/(?P<id>[\d]+)/$', views.CiclosAPIView.as_view(), name="ciclos-api"),
	url(r'^materia/(?P<id>[\d]+)/$', views.MateriaAPIView.as_view(), name="materia-api"),
	url(r'^profesor-materia/(?P<id>[\d]+)/$', views.ProfesorMateriaAPIView.as_view(), name="profesor-materia-api"),
	url(r'^proceso-stats/$', views.ProcesoAlumnoStatsAPIView.as_view(), name="proceso-stats"),
	url(r'^proceso/$', views.ProcesoStatsAPIView.as_view(), name="proceso"),
]