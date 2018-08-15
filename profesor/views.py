# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DeleteView
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import update_session_auth_hash
from django.contrib.auth.models import User, Group, Permission
from django.template import loader
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.db.models import Q
from django.conf import settings
from django.forms.utils import ErrorList
from django.utils.timezone import datetime #important if using timezones
from forms import *
from models import *
from alumno.models import *
from administrador.models import *
from alumno.forms import *
from SeguimientoUCSG import util

# Create your views here.
class ProfesorListView(UserPassesTestMixin, ListView):
    model = Profesor
    template_name = 'profesor/profesor_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_queryset(self):
        return super(ProfesorListView, self).get_queryset().all()

    
    def get_context_data(self, **kwargs):
        context = super(ProfesorListView, self).get_context_data(**kwargs)
        context['tittle'] = "Profesores"
        context['motto'] = "Tabla para visualizar Profesores"
        context['table_id'] = "profesor"
        return context


class ProfesorCreateView(PermissionRequiredMixin, CreateView):
    form_class = ProfesorForm
    template_name = 'profesor/profesor_create.html'
    permission_required = (
    	'profesor.list_profesors', 
    	'profesor.add_profesor', 
    	'profesor.change_profesor', 
    	'profesor.delete_profesor',
    )
    
    def send_mail_to_user(self, user, request):
        context = {
            'email': user.email,
            'domain': "%s%s"%('http://', request.META['HTTP_HOST']),
            'site_name': 'Seguimiento UCSG',
            'user': user,
            'protocol': 'https',
        }
        subject_template_name = 'profesor/new_account_subject.txt'
        email_template_name = 'profesor/new_account.html'
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        email = loader.get_template(email_template_name).render(context)
        email_message = EmailMessage(
            subject,
            email,
            to=[user.email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)

    def get_success_url(self):
        return '/profesor/profesores-list/'

    def get(self, request, next=None):
        return super(ProfesorCreateView, self).get(request)

    def form_valid(self, form):
        try:
            if User.objects.filter(username=form.instance.user.username).exists():
                errors = form._errors.setdefault("email", ErrorList())
                errors.append(u"Ya existe un usuario registrado con este email")
                response = super(ProfesorCreateView, self).form_invalid(form)
            else:
                response = super(ProfesorCreateView, self).form_valid(form)
                _user_id_ = form.instance.user.id
                user = User.objects.filter(pk=_user_id_).first()
                self.send_mail_to_user(user, self.request)
        except Exception, e:
            print 'Error', e
            errors = form._errors.setdefault("email", ErrorList())
            errors.append(u"Ya existe un usuario registrado con este email")
            if form.instance.user.id:
                form.instance.user.delete()
            response = super(ProfesorCreateView, self).form_invalid(form)
        return response

    def form_invalid(self, form):
        return super(ProfesorCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfesorCreateView, self).get_context_data(**kwargs)
        context['tittle'] = "Profesores"
        context['motto'] = "Formulario para crear un nuevo Profesor"
        return context


class ProfesorUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = ProfesorForm
    template_name = 'profesor/profesor_edit.html'
    success_url = '/profesor/profesores-list/'
    permission_required = (
    	'profesor.list_profesors', 
    	'profesor.add_profesor', 
    	'profesor.change_profesor', 
    	'profesor.delete_profesor',
    )

    def get_object(self, queryset=None):
        if not Profesor.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        profesor = Profesor.objects.get(pk=self.kwargs['id'])
        if profesor.deleted:
            raise Http404
        return profesor

    def form_valid(self, form):
        clean = form.cleaned_data
        try:
            response = super(ProfesorUpdateView, self).form_valid(form)
        except Exception, e:
            print e
            errors = form._errors.setdefault("email", ErrorList())
            errors.append(u"Ya existe un usuario registrado con este email")
            response = super(ProfesorUpdateView, self).form_invalid(form)
        return response

    def form_invalid(self, form):
        return super(ProfesorUpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfesorUpdateView, self).get_context_data(**kwargs)
        context['tittle'] = "Profesores"
        context['motto'] = "Formulario para editar Profesores"
        return context


class ProfesorPasswordUpdateView(PermissionRequiredMixin, FormView):
    form_class = ProfesorSetPasswordForm
    template_name = 'profesor/profesor_create.html'
    success_url = '/profesor/profesores-list/'
    permission_required = (
    	'profesor.list_profesors', 
    	'profesor.add_profesor', 
    	'profesor.change_profesor', 
    	'profesor.delete_profesor',
    )

    def get_form(self):
        if not Profesor.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        self.profesor = Profesor.objects.get(id=self.kwargs['id'])
        user = self.profesor.user
        if self.request.method == 'GET':
            form = self.form_class(user=user)
        elif self.request.method == 'POST':
            form = self.form_class(user=user, data=self.request.POST)
        return form

    def get_success_url(self):
        if Profesor.objects.filter(id=self.kwargs['id']).exists():
            return '/profesor/profesores-edit/%s/'%self.kwargs['id']
        else:
            return self.success_url

    def form_valid(self, form):
        form = self.get_form()
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, form.user)
        else:
            return super(ProfesorPasswordUpdateView, self).form_invalid(form)
        return super(ProfesorPasswordUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfesorPasswordUpdateView, self).get_context_data(**kwargs)
        context['tittle'] = "Profesores"
        context['motto'] = u"Formulario para configurar la contraseña del Profesor %s %s"%(self.profesor.user.first_name, self.profesor.user.last_name)
        return context


class ProfesorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Profesor
    success_url = '/profesor/profesores-list/'
    permission_required = (
    	'profesor.list_profesors', 
    	'profesor.add_profesor', 
    	'profesor.change_profesor', 
    	'profesor.delete_profesor',
    )

    def get_object(self):
        id = self.kwargs['id']
        profesor = Profesor.objects.get(id=id)
        _user_ = User.objects.filter(pk=profesor.user.id)
        _user_.delete()
        return profesor

    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)

