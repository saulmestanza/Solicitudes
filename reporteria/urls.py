# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^reporteria-notas/$', views.ReporteriaNotasCreateView.as_view(), name='reporteria-notas'),
]