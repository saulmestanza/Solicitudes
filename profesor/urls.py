# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^profesores-list/$', views.ProfesorListView.as_view(), name='profesores-list'),
	url(r'^profesores-new(?:/(?P<next>[\w\-]+))?/$', views.ProfesorCreateView.as_view(), name='profesores-new' ),
	url(r'^profesores-edit/(?P<id>[\w\-]+)/$', views.ProfesorUpdateView.as_view(), name='profesores-edit' ),
	url(r'^profesores-edit-password/(?P<id>[\w\-]+)/$', views.ProfesorPasswordUpdateView.as_view(), name='profesores-edit-password' ),
	url(r'^profesores-delete/(?P<id>[\w\-]+)/$', views.ProfesorDeleteView.as_view(), name='profesores-delete' ),

	url(r'^profesor-seguimiento/$', views.ProfesorProcesosListView.as_view(), name='profesor-seguimiento'),
	url(r'^proceso-profesor-edit/(?P<id>[\w\-]+)/$', views.ProfesorProcesosEditView.as_view(), name='profesor-proceso-edit'),
]