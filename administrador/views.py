# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import update_session_auth_hash
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext as _
from django.http import Http404
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
from django.conf import settings
from django.forms.utils import ErrorList
from django.template import RequestContext
from django.shortcuts import *
from rest_framework import status
from rest_framework.response import Response
from forms import *
from serializers import *
from models import *
from axes.utils import reset
from SeguimientoUCSG import util
import json


class LoginView(FormView):
    form_class = LoginForm
    alert_message = None
    template_name = 'administrador/login.html'
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.GET.get('next')
                if next is not None:
                    return redirect(next)
                return redirect('/')
            else:
                self.alert_message = {'class': 'alert alert-danger',
                'mod': 'Error:',
                'message': u'Cuenta deshabilitada.'}
                return self.get(request)
        else:
            self.alert_message = {'class': 'alert alert-danger',
            'mod': 'Error:',
            'message': u'Usuario o contraseña incorrecta.'}
            return self.get(request)
        return render(request, "/")

    
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['alert_message'] = self.alert_message
        context['tittle'] = _(u"Iniciar Sesión")
        return context


class LogoutView(LoginView):
    def get(self, request):
        logout(request)
        return super(LogoutView,self).get(request)

    
    def get_context_data(self, **kwargs):
        context = super(LogoutView, self).get_context_data(**kwargs)
        if not self.alert_message:
            context['alert_message'] = {'class': 'alert alert-success',
            'mod': 'Sesión cerrada:',
            'message': u'La sesión fue cerrada exitosamente.'}
        context['tittle'] = _(u"Cierre de Sesión")
        return context


class LockedOutView(FormView):
    form_class = AxesCaptchaForm
    success_url = '/administrador/login/'
    template_name = 'administrador/locked_out.html'

    def form_valid(self, form):
        ip = util.get_client_ip(self.request)
        reset(ip=ip)
        return super(LockedOutView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LockedOutView, self).get_context_data(**kwargs)
        context['alert_message'] = {'class': 'alert alert-danger',
        'mod': _('Usuario Bloqueado:'),
        'message': _(u'El siguiente formulario permitirá desbloquear el usuario.')}
        context['tittle'] = _(u"Usuario Bloqueado")
        context['motto'] = "El siguiente formulario permitirá desbloquear el usuario."
        return context


class UsersListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'administrador/users_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_queryset(self):
        return super(UsersListView, self).get_queryset().filter( Q(is_staff=True) | Q(is_superuser=True) )

    
    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['tittle'] = "Usuarios"
        context['motto'] = "Tabla para visualizar Usuarios"
        context['table_id'] = "users"
        return context


class UserCreate(UserPassesTestMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'administrador/user_create.html'
    success_url = '/administrador/users-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def form_valid(self, form):
        try:
            context = self.get_context_data()
            userprofile = context['userprofile']

            if not User.objects.filter(username=form.instance.username).exists() and userprofile.is_valid():
                self.object = form.save()
                for group_ in form.cleaned_data['groups']:
                    self.object.groups.add(group_)
                userprofile.instance.user = self.object
                userprofile.save()
                response = super(UserCreate, self).form_valid(form)
            else:
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
                response = super(UserCreate, self).form_invalid(form)
        except Exception as e:
            print e
            errors = form._errors.setdefault("username", ErrorList())
            errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
            response = super(UserCreate, self).form_invalid(form)
        return response

    
    def form_invalid(self, form):
        return super(UserCreate, self).form_invalid(form)

    
    def get_context_data(self, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        context['tittle'] = _("Usuarios")
        context['motto'] = _("Formulario para crear un nuevo Usuario")
        if self.request.POST:
            context['userprofile'] = UserProfileForm(self.request.POST)
        else:
            context['userprofile'] = UserProfileForm()
        return context


class UserUpdate(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'administrador/user_create.html'
    success_url = '/administrador/users-list/'

    
    def test_func(self):
        if self.request.user.is_superuser:
            self.form_class = UserForm
            self.success_url = '/administrador/users-list/'
        else:
            self.form_class = UserStaffForm
            self.success_url = '/'
        return self.request.user.is_active

    
    def form_valid(self, form):
        context = self.get_context_data()
        userprofile = context['userprofile']

        if form.is_valid() and userprofile.is_valid():
            self.object = form.save()
            if UserProfile.objects.filter(user=self.object).exists():
                UserProfile.objects.filter(user=self.object).update(**userprofile.cleaned_data)
            else:
                userprofile.instance.user = self.object
                userprofile.save()
            response = super(UserUpdate, self).form_valid(form)
        else:
            response = super(UserUpdate, self).form_invalid(form)
        return response

    
    def get_object(self, queryset=None):
        if not User.objects.filter(username=self.kwargs['username']).exists():
            raise Http404
        _user = User.objects.get(username=self.kwargs['username'])
        return _user

    
    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['tittle'] = _("Usuarios")
        context['motto'] = _("Formulario para editar un Usuario existente")
        if self.request.POST:
            context['userprofile'] = UserProfileForm(self.request.POST)
        else:
            _user = self.get_object()
            if hasattr(_user, 'userprofile'):
                context['userprofile'] = UserProfileForm(instance=_user.userprofile)
            else:
                context['userprofile'] = UserProfileForm()
        return context


class UserUpdatePassword(UserPassesTestMixin, FormView):
    form_class = PasswordChangeForm
    template_name = 'administrador/user_create.html'
    success_url = '/administrador/users-list/'

    
    def test_func(self):
        if self.request.user.is_superuser:
            self.success_url = '/administrador/users-list/'
        else:
            self.success_url = '/'
        return self.request.user.is_active

    
    def get_form(self):
        if not User.objects.filter(username=self.kwargs['username']).exists():
            raise Http404
        user = User.objects.get(username=self.kwargs['username'])
        if self.request.method == 'GET':
            form = self.form_class(user=user)
        elif self.request.method == 'POST':
            form = self.form_class(user=user, data=self.request.POST)
        return form

    
    def get_success_url(self):
        if User.objects.filter(username=self.kwargs['username']).exists():
            return '/administrador/user-edit/%s/'%self.kwargs['username']
        else:
            return self.success_url

    
    def form_valid(self, form):
        form = self.get_form()
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, form.user)
        else:
            return super(UserUpdatePassword, self).form_invalid(form)
        return super(UserUpdatePassword, self).form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super(UserUpdatePassword, self).get_context_data(**kwargs)
        context['tittle'] = _("Usuarios")
        context['motto'] = _(u"Formulario para cambiar contraseña a un Usuario existente")
        return context


class PermissionsListView(UserPassesTestMixin, ListView):
    model = Permission
    template_name = 'administrador/permissions_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(PermissionsListView, self).get_context_data(**kwargs)
        context['tittle'] = "Permisos"
        context['motto'] = "Tabla para visualizar Permisos"
        context['table_id'] = "permissions"
        return context


class PermissionCreate(UserPassesTestMixin, CreateView):
    model = Permission
    fields = '__all__'
    template_name = 'administrador/permission_create.html'
    success_url = '/administrador/permissions-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(PermissionCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Permisos"
        context['motto'] = "Formulario para crear un nuevo Permiso"

        form = context['form']
        for field in form.fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
            if form.fields[field].help_text:
                form.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                form.fields[field].widget.attrs['data-placement'] = 'top'
                form.fields[field].widget.attrs['title'] = form.fields[field].help_text
        return context


class PermissionUpdate(UserPassesTestMixin, UpdateView):
    model = Permission
    fields = '__all__'
    template_name = 'administrador/permission_create.html'
    success_url = '/administrador/permissions-list/'    

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self, queryset=None):
        if not Permission.objects.filter(codename=self.kwargs['codename']).exists():
            raise Http404
        permission = Permission.objects.get(codename=self.kwargs['codename'])
        return permission

    
    def get_context_data(self, **kwargs):
        context = super(PermissionUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Permisos"
        context['motto'] = "Formulario para editar un Permiso existente"

        form = context['form']
        for field in form.fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
            if form.fields[field].help_text:
                form.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                form.fields[field].widget.attrs['data-placement'] = 'top'
                form.fields[field].widget.attrs['title'] = form.fields[field].help_text
        return context


class PermissionDelete(UserPassesTestMixin, DeleteView):
    model = Permission
    success_url = '/administrador/permissions-list/#permissions'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not Permission.objects.filter(codename=self.kwargs['codename']).exists():
            raise Http404
        permission = Permission.objects.get(codename=self.kwargs['codename'])
        return permission

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)
        

class GroupsListView(UserPassesTestMixin, ListView):
    model = Group
    template_name = 'administrador/groups_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(GroupsListView, self).get_context_data(**kwargs)
        context['tittle'] = "Grupos de Roles"
        context['motto'] = "Tabla para visualizar Grupos de Roles"
        context['table_id'] = "groups"
        return context


class GroupCreate(UserPassesTestMixin, CreateView):
    model = Group
    fields = '__all__'
    template_name = 'administrador/group_create.html'
    success_url = '/administrador/groups-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(GroupCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Grupos de Roles"
        context['motto'] = "Formulario para crear un nuevo Grupo de Roles"

        form = context['form']
        for field in form.fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
            if form.fields[field].help_text:
                form.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                form.fields[field].widget.attrs['data-placement'] = 'top'
                form.fields[field].widget.attrs['title'] = form.fields[field].help_text
        return context


class GroupUpdate(UserPassesTestMixin, UpdateView):
    model = Group
    fields = '__all__'
    template_name = 'administrador/group_create.html'
    success_url = '/administrador/groups-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self, queryset=None):
        if not Group.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        group = Group.objects.get(pk=self.kwargs['id'])
        return group

    
    def get_context_data(self, **kwargs):
        context = super(GroupUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Grupos de Roles"
        context['motto'] = "Formulario para editar un Grupo de Roles existente"

        form = context['form']
        for field in form.fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
            if form.fields[field].help_text:
                form.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                form.fields[field].widget.attrs['data-placement'] = 'top'
                form.fields[field].widget.attrs['title'] = form.fields[field].help_text
        return context


class GroupDelete(UserPassesTestMixin, DeleteView):
    model = Group
    success_url = '/administrador/groups-list/#groups'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not Group.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        group = Group.objects.get(pk=self.kwargs['id'])
        return group

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)


### FACULTAD ###


class FacultadListView(UserPassesTestMixin, ListView):
    model = Facultad
    template_name = 'administrador/faculties_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(FacultadListView, self).get_context_data(**kwargs)
        context['tittle'] = "Facultades"
        context['motto'] = "Tabla para visualizar Facultades"
        context['table_id'] = "faculties"
        return context


class FacultadCreate(UserPassesTestMixin, CreateView):
    model = Facultad
    form_class = FacultadForm
    template_name = 'administrador/faculties_create.html'
    success_url = '/administrador/faculties-list/'

    def form_invalid(self, form):
        return super(FacultadCreate, self).form_invalid(form)

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            if not Facultad.objects.filter(name=form.instance.name).exists():
                self.object = form.save()
                response = super(FacultadCreate, self).form_valid(form)
            else:
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
                response = super(FacultadCreate, self).form_invalid(form)
        except Exception as e:
            print e
            errors = form._errors.setdefault("name", ErrorList())
            errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
            response = super(FacultadCreate, self).form_invalid(form)
        return response
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(FacultadCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Facultades"
        context['motto'] = "Formulario para crear nuevas Facultades"
        if self.request.POST:
            context['facultad'] = FacultadForm(self.request.POST)
        else:
            context['facultad'] = FacultadForm()
        return context


class FacultadUpdate(UserPassesTestMixin, UpdateView):
    model = Facultad
    form_class = FacultadForm
    template_name = 'administrador/faculties_create.html'
    success_url = '/administrador/faculties-list/'

    
    def form_valid(self, form):
        context = self.get_context_data()
        facultad = context['facultad']

        if form.is_valid() and facultad.is_valid():
            self.object = form.save()
            if Facultad.objects.filter(pk=self.object.id).exists():
                _faculty_ = Facultad.objects.filter(pk=self.object.id)
            	facultad.cleaned_data.pop('carrer', [])
            	Facultad.objects.filter(pk=self.object.id).update(**facultad.cleaned_data)
            response = super(FacultadUpdate, self).form_valid(form)
        else:
            response = super(FacultadUpdate, self).form_invalid(form)
        return response

    
    def get_object(self, queryset=None):
        if not Facultad.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        faculty = Facultad.objects.get(id=self.kwargs['id'])
        return faculty

    
    def get_context_data(self, **kwargs):
        context = super(FacultadUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Facultades"
        context['motto'] = "Formulario para editar facultades existente"
        if self.request.POST:
            context['facultad'] = FacultadForm(self.request.POST)
        else:
            facultad = self.get_object()
            if hasattr(facultad, 'facultad'):
                context['facultad'] = FacultadForm(instance=facultad)
            else:
                context['facultad'] = FacultadForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser


class FacultadDelete(UserPassesTestMixin, DeleteView):
    model = Facultad
    success_url = '/administrador/faculties-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not Facultad.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        faculty = Facultad.objects.get(pk=self.kwargs['id'])
        return faculty

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)


### CARRERA ###


class CarreraListView(UserPassesTestMixin, ListView):
    model = Carrera
    template_name = 'administrador/carrera_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(CarreraListView, self).get_context_data(**kwargs)
        context['tittle'] = "Carreras"
        context['motto'] = "Tabla para visualizar Carreras"
        context['table_id'] = "carrera"
        return context


class CarreraCreate(UserPassesTestMixin, CreateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'administrador/carrera_create.html'
    success_url = '/administrador/carrera-list/'

    def form_invalid(self, form):
        return super(CarreraCreate, self).form_invalid(form)

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            if not Carrera.objects.filter(name=form.instance.name).exists():
                self.object = form.save()
                response = super(CarreraCreate, self).form_valid(form)
            else:
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
                response = super(CarreraCreate, self).form_invalid(form)
        except Exception as e:
            print e
            errors = form._errors.setdefault("name", ErrorList())
            errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
            response = super(CarreraCreate, self).form_invalid(form)
        return response
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(CarreraCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Carreras"
        context['motto'] = "Formulario para crear nuevas Carreras"
        if self.request.POST:
            context['carrera'] = CarreraForm(self.request.POST)
        else:
            context['carrera'] = CarreraForm()
        return context


class CarreraUpdate(UserPassesTestMixin, UpdateView):
    model = Carrera
    form_class = CarreraForm
    template_name = 'administrador/carrera_create.html'
    success_url = '/administrador/carrera-list/'

    
    def form_valid(self, form):
        context = self.get_context_data()
        carrera = context['carrera']

        if form.is_valid() and carrera.is_valid():
            self.object = form.save()
            if Carrera.objects.filter(pk=self.object.id).exists():
                _carrera_ = Carrera.objects.filter(pk=self.object.id)
            	carrera.cleaned_data.pop('cicles', [])
            	Carrera.objects.filter(pk=self.object.id).update(**carrera.cleaned_data)
            response = super(CarreraUpdate, self).form_valid(form)
        else:
            response = super(CarreraUpdate, self).form_invalid(form)
        return response

    
    def get_object(self, queryset=None):
        if not Carrera.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        faculty = Carrera.objects.get(id=self.kwargs['id'])
        return faculty

    
    def get_context_data(self, **kwargs):
        context = super(CarreraUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Carreras"
        context['motto'] = "Formulario para editar carreras existente"
        if self.request.POST:
            context['carrera'] = CarreraForm(self.request.POST)
        else:
            carrera = self.get_object()
            if hasattr(carrera, 'carrera'):
                context['carrera'] = CarreraForm(instance=carrera)
            else:
                context['carrera'] = CarreraForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser


class CarreraDelete(UserPassesTestMixin, DeleteView):
    model = Carrera
    success_url = '/administrador/carrera-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not Carrera.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        carrera = Carrera.objects.get(pk=self.kwargs['id'])
        return carrera

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)


### CICLO ###


class CicloListView(UserPassesTestMixin, ListView):
    model = Ciclo
    template_name = 'administrador/ciclo_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(CicloListView, self).get_context_data(**kwargs)
        context['tittle'] = "Ciclos"
        context['motto'] = "Tabla para visualizar Ciclos"
        context['table_id'] = "ciclo"
        return context


class CicloCreate(UserPassesTestMixin, CreateView):
    model = Ciclo
    form_class = CicloForm
    template_name = 'administrador/ciclo_create.html'
    success_url = '/administrador/ciclo-list/'

    def form_invalid(self, form):
        return super(CicloCreate, self).form_invalid(form)

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            if not Ciclo.objects.filter(name=form.instance.name, carrer_id=form.instance.carrer_id).exists():
                self.object = form.save()
                response = super(CicloCreate, self).form_valid(form)
            else:
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
                response = super(CicloCreate, self).form_invalid(form)
        except Exception as e:
            print e
            errors = form._errors.setdefault("name", ErrorList())
            errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
            response = super(CicloCreate, self).form_invalid(form)
        return response
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(CicloCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Ciclos"
        context['motto'] = "Formulario para crear nuevos Ciclos"
        if self.request.POST:
            context['ciclo'] = CicloForm(self.request.POST)
        else:
            context['ciclo'] = CicloForm()
        return context


class CicloUpdate(UserPassesTestMixin, UpdateView):
    model = Ciclo
    form_class = CicloForm
    template_name = 'administrador/ciclo_create.html'
    success_url = '/administrador/ciclo-list/'

    
    def form_valid(self, form):
        context = self.get_context_data()
        ciclo = context['ciclo']

        if form.is_valid() and ciclo.is_valid():
            self.object = form.save()
            if Ciclo.objects.filter(pk=self.object.id).exists():
            	_ciclo_ = Ciclo.objects.filter(pk=self.object.id)
            	ciclo.cleaned_data.pop('subjects', [])
            	Ciclo.objects.filter(pk=self.object.id).update(**ciclo.cleaned_data)
            response = super(CicloUpdate, self).form_valid(form)
        else:
            response = super(CicloUpdate, self).form_invalid(form)
        return response

    
    def get_object(self, queryset=None):
        if not Ciclo.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        faculty = Ciclo.objects.get(id=self.kwargs['id'])
        return faculty

    
    def get_context_data(self, **kwargs):
        context = super(CicloUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Ciclos"
        context['motto'] = "Formulario para editar ciclos existente"
        if self.request.POST:
            context['ciclo'] = CicloForm(self.request.POST)
        else:
            ciclo = self.get_object()
            if hasattr(ciclo, 'ciclo'):
                context['ciclo'] = CicloForm(instance=materia)
            else:
                context['ciclo'] = CicloForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser


class CicloDelete(UserPassesTestMixin, DeleteView):
    model = Ciclo
    success_url = '/administrador/ciclo-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not Ciclo.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        ciclo = Ciclo.objects.get(pk=self.kwargs['id'])
        return ciclo

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)


### MATERIA ###


class MateriaListView(UserPassesTestMixin, ListView):
    model = Materia
    template_name = 'administrador/materia_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(MateriaListView, self).get_context_data(**kwargs)
        context['tittle'] = "Materias"
        context['motto'] = "Tabla para visualizar Materias"
        context['table_id'] = "materia"
        return context


class MateriaCreate(UserPassesTestMixin, CreateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'administrador/materia_create.html'
    success_url = '/administrador/materia-list/'

    def form_invalid(self, form):
        return super(MateriaCreate, self).form_invalid(form)

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            if not Materia.objects.filter(name=form.instance.name).exists():
                self.object = form.save()
                response = super(MateriaCreate, self).form_valid(form)
            else:
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
                response = super(MateriaCreate, self).form_invalid(form)
        except Exception as e:
            print e
            errors = form._errors.setdefault("name", ErrorList())
            errors.append(_(u"Ya existe un usuario registrado con este nombre de usuario"))
            response = super(MateriaCreate, self).form_invalid(form)
        return response
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(MateriaCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Materias"
        context['motto'] = "Formulario para crear nuevas Materias"
        context['faculties'] = Facultad.objects.filter(deleted=False)
        context['carrers'] = Carrera.objects.filter(deleted=False)
        context['cicles'] = Ciclo.objects.filter(deleted=False)
        if self.request.POST:
            context['materia'] = MateriaForm(self.request.POST)
        else:
            context['materia'] = MateriaForm()
        return context


class MateriaUpdate(UserPassesTestMixin, UpdateView):
    model = Materia
    form_class = MateriaForm
    template_name = 'administrador/materia_edit.html'
    success_url = '/administrador/materia-list/'

    
    def form_valid(self, form):
        context = self.get_context_data()
        materia = context['materia']

        if form.is_valid() and materia.is_valid():
            self.object = form.save()
            if Materia.objects.filter(pk=self.object.id).exists():
                Materia.objects.filter(pk=self.object.id).update(**materia.cleaned_data)
            response = super(MateriaUpdate, self).form_valid(form)
        else:
            response = super(MateriaUpdate, self).form_invalid(form)
        return response

    
    def get_object(self, queryset=None):
        if not Materia.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        subject = Materia.objects.get(id=self.kwargs['id'])
        return subject

    
    def get_context_data(self, **kwargs):
        context = super(MateriaUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Materias"
        context['motto'] = "Formulario para editar materias existente"
        context['faculties'] = Facultad.objects.filter(deleted=False)
        context['carrers'] = Carrera.objects.filter(deleted=False)
        context['cicles'] = Ciclo.objects.filter(deleted=False)
        context['subject'] = self.get_object()
        if self.request.POST:
            context['materia'] = MateriaForm(self.request.POST)
        else:
            materia = self.get_object()
            if hasattr(materia, 'materia'):
                context['materia'] = MateriaForm(instance=materia)
            else:
                context['materia'] = MateriaForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser


class MateriaDelete(UserPassesTestMixin, DeleteView):
    model = Materia
    success_url = '/administrador/materia-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not Materia.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        materia = Materia.objects.get(pk=self.kwargs['id'])
        return materia

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)



### PROCESO ###


class ProcesoListView(UserPassesTestMixin, ListView):
    model = Proceso
    template_name = 'administrador/proceso_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(ProcesoListView, self).get_context_data(**kwargs)
        context['tittle'] = "Procesos"
        context['motto'] = "Tabla para visualizar Procesos"
        context['table_id'] = "materia"
        return context


class ProcesoView(UserPassesTestMixin, ListView):
    model = Proceso
    template_name = 'administrador/proceso_view.html'

    
    def test_func(self):
        return self.request.user.is_active

    def get_object(self, queryset=None):
        if not Proceso.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        _proceso_ = Proceso.objects.get(id=self.kwargs['id'])
        return _proceso_
    
    def get_context_data(self, **kwargs):
        context = super(ProcesoView, self).get_context_data(**kwargs)
        proceso = self.get_object()
        context['tittle'] = proceso.name
        context['motto'] = "Detalle del Proceso %s"%(proceso.name)
        context['table_id'] = "materia"
        context['proceso'] = proceso
        return context


class ProcesoCreate(UserPassesTestMixin, CreateView):
    model = Proceso
    form_class = ProcesoForm
    template_name = 'administrador/proceso_create.html'
    success_url = '/administrador/proceso-list/'

    def form_invalid(self, form):
        return super(ProcesoCreate, self).form_invalid(form)

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            if not Proceso.objects.filter(name=form.instance.name).exists():
                self.object = form.save()
                response = super(ProcesoCreate, self).form_valid(form)
            else:
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(_(u"Ya existe un proceso registrado con este nombre"))
                response = super(ProcesoCreate, self).form_invalid(form)
        except Exception as e:
            print e
            errors = form._errors.setdefault("name", ErrorList())
            errors.append(_(u"Ya existe un proceso registrado con este nombre"))
            response = super(ProcesoCreate, self).form_invalid(form)
        return response
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(ProcesoCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Procesos"
        context['motto'] = "Formulario para crear nuevos Procesos"
        context['proceso_items'] = ProcesoItems.objects.all()
        if self.request.POST:
            context['proceso'] = ProcesoForm(self.request.POST)
        else:
            context['proceso'] = ProcesoForm()
        return context


class ProcesoUpdate(UserPassesTestMixin, UpdateView):
    model = Proceso
    form_class = ProcesoForm
    template_name = 'administrador/proceso_editar.html'
    success_url = '/administrador/proceso-list/'

    
    def form_valid(self, form):
        context = self.get_context_data()
        proceso = context['proceso']

        if form.is_valid() and proceso.is_valid():
            self.object = form.save()
            if Proceso.objects.filter(pk=self.object.id).exists():
                _proceso_ = Proceso.objects.filter(pk=self.object.id)
                proceso.cleaned_data.pop('proceso_items', [])
                Proceso.objects.filter(pk=self.object.id).update(**proceso.cleaned_data)
            response = super(ProcesoUpdate, self).form_valid(form)
        else:
            response = super(ProcesoUpdate, self).form_invalid(form)
        return response

    
    def get_object(self, queryset=None):
        if not Proceso.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        _proceso_ = Proceso.objects.get(id=self.kwargs['id'])
        return _proceso_

    
    def get_context_data(self, **kwargs):
        context = super(ProcesoUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Procesos"
        context['motto'] = "Formulario para editar procesos existente"
        context['proceso_items'] = ProcesoItems.objects.all()
        context['proceso_'] = self.get_object()
        if self.request.POST:
            context['proceso'] = ProcesoForm(self.request.POST)
        else:
            proceso = self.get_object()
            if hasattr(proceso, 'proceso'):
                context['proceso'] = ProcesoForm(instance=proceso)
            else:
                context['proceso'] = ProcesoForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser


class ProcesoDelete(UserPassesTestMixin, DeleteView):
    model = Proceso
    success_url = '/administrador/proceso-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not Proceso.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        proceso = Proceso.objects.get(pk=self.kwargs['id'])
        return proceso

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)



### PROCESO ITEMS ###


class ProcesoItemsListView(UserPassesTestMixin, ListView):
    model = ProcesoItems
    template_name = 'administrador/proceso_items_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(ProcesoItemsListView, self).get_context_data(**kwargs)
        context['tittle'] = "Procesos"
        context['motto'] = "Tabla para visualizar Procesos"
        context['table_id'] = "materia"
        return context


class ProcesoItemCreate(UserPassesTestMixin, CreateView):
    model = ProcesoItems
    form_class = ProcesoItemsForm
    template_name = 'administrador/proceso_item_crear.html'
    success_url = '/administrador/proceso-item-list/'

    def post(self, request):
        if request.method == "POST":
            form = ProcesoItemsForm(request.POST)
            message = 'something wrong!'
            if(form.is_valid()):
                form.save()
                proceos_items = ProcesoItems.objects.filter(deleted=False)
                serializer = ProcesoItemsSerializer(proceos_items, many=True)
                return HttpResponse(json.dumps({'items': serializer.data}))
            else:
                return HttpResponse(json.dumps({'message': message}))
        return HttpResponse(json.dumps({'message': message}))

    def form_invalid(self, form):
        return super(ProcesoItemCreate, self).form_invalid(form)

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            if not ProcesoItems.objects.filter(name=form.instance.name).exists():
                self.object = form.save()
                response = super(ProcesoItemCreate, self).form_valid(form)
            else:
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(_(u"Ya existe un proceso registrado con este nombre"))
                response = super(ProcesoItemCreate, self).form_invalid(form)
        except Exception as e:
            print e
            errors = form._errors.setdefault("name", ErrorList())
            errors.append(_(u"Ya existe un proceso registrado con este nombre"))
            response = super(ProcesoItemCreate, self).form_invalid(form)
        return response
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(ProcesoItemCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Procesos"
        context['motto'] = "Formulario para crear nuevas Procesos"
        if self.request.POST:
            context['proceso'] = ProcesoItemsForm(self.request.POST)
        else:
            context['proceso'] = ProcesoItemsForm()
        return context


class ProcesoItemUpdate(UserPassesTestMixin, UpdateView):
    model = ProcesoItems
    form_class = ProcesoItemsForm
    template_name = 'administrador/proceso_item_crear.html'
    success_url = '/administrador/proceso-item-list/'

    
    def form_valid(self, form):
        context = self.get_context_data()
        proceso = context['proceso']

        if form.is_valid() and proceso.is_valid():
            self.object = form.save()
            if ProcesoItems.objects.filter(pk=self.object.id).exists():
                ProcesoItems.objects.filter(pk=self.object.id).update(**proceso.cleaned_data)
            response = super(ProcesoItemUpdate, self).form_valid(form)
        else:
            response = super(ProcesoItemUpdate, self).form_invalid(form)
        return response

    
    def get_object(self, queryset=None):
        if not ProcesoItems.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        _proceso_ = ProcesoItems.objects.get(id=self.kwargs['id'])
        return _proceso_

    
    def get_context_data(self, **kwargs):
        context = super(ProcesoItemUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Procesos"
        context['motto'] = "Formulario para editar procesos existente"
        if self.request.POST:
            context['proceso'] = ProcesoItemsForm(self.request.POST)
        else:
            proceso = self.get_object()
            if hasattr(proceso, 'proceso'):
                context['proceso'] = ProcesoItemsForm(instance=proceso)
            else:
                context['proceso'] = ProcesoItemsForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser


class ProcesoItemDelete(UserPassesTestMixin, DeleteView):
    model = ProcesoItems
    success_url = '/administrador/proceso-item-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not ProcesoItems.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        proceso = ProcesoItems.objects.get(pk=self.kwargs['id'])
        return proceso

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)


### PERIODO ###


class PeriodoListView(UserPassesTestMixin, ListView):
    model = Periodo
    template_name = 'administrador/periodo_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_context_data(self, **kwargs):
        context = super(PeriodoListView, self).get_context_data(**kwargs)
        context['tittle'] = "Periodos"
        context['motto'] = "Tabla para visualizar Periodos"
        context['table_id'] = "materia"
        return context


class PeriodoCreate(UserPassesTestMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'administrador/periodo_crear.html'
    success_url = '/administrador/periodo-list/'

    def form_invalid(self, form):
        return super(PeriodoCreate, self).form_invalid(form)

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            if not Periodo.objects.filter(name=form.instance.name).exists():
                self.object = form.save()
                response = super(PeriodoCreate, self).form_valid(form)
            else:
                errors = form._errors.setdefault("name", ErrorList())
                errors.append(_(u"Ya existe un periodo registrado con este nombre"))
                response = super(PeriodoCreate, self).form_invalid(form)
        except Exception as e:
            print e
            errors = form._errors.setdefault("name", ErrorList())
            errors.append(_(u"Ya existe un periodo registrado con este nombre"))
            response = super(PeriodoCreate, self).form_invalid(form)
        return response
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super(PeriodoCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Periodos"
        context['motto'] = "Formulario para crear nuevos Periodos"
        if self.request.POST:
            context['periodo'] = PeriodoForm(self.request.POST)
        else:
            context['periodo'] = PeriodoForm()
        return context


class PeriodoUpdate(UserPassesTestMixin, UpdateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'administrador/periodo_crear.html'
    success_url = '/administrador/periodo-list/'

    
    def form_valid(self, form):
        context = self.get_context_data()
        periodo = context['periodo']

        if form.is_valid() and periodo.is_valid():
            self.object = form.save()
            if Periodo.objects.filter(pk=self.object.id).exists():
                _periodo_ = Periodo.objects.filter(pk=self.object.id)
                periodo.cleaned_data.pop('carrer', [])
                Periodo.objects.filter(pk=self.object.id).update(**periodo.cleaned_data)
            response = super(PeriodoUpdate, self).form_valid(form)
        else:
            response = super(PeriodoUpdate, self).form_invalid(form)
        return response

    
    def get_object(self, queryset=None):
        if not Periodo.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        _periodo_ = Periodo.objects.get(id=self.kwargs['id'])
        return _periodo_

    
    def get_context_data(self, **kwargs):
        context = super(PeriodoUpdate, self).get_context_data(**kwargs)
        context['tittle'] = "Periodos"
        context['motto'] = "Formulario para editar periodos existente"
        if self.request.POST:
            context['periodo'] = PeriodoForm(self.request.POST)
        else:
            periodo = self.get_object()
            if hasattr(periodo, 'periodo'):
                context['periodo'] = PeriodoForm(instance=periodo)
            else:
                context['periodo'] = PeriodoForm()
        return context

    def test_func(self):
        return self.request.user.is_superuser


class PeriodoDelete(UserPassesTestMixin, DeleteView):
    model = Periodo
    success_url = '/administrador/periodo-list/'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_object(self):
        if not Periodo.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        proceso = Periodo.objects.get(pk=self.kwargs['id'])
        return proceso

    
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)

