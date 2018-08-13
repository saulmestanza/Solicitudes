# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DeleteView, TemplateView
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import update_session_auth_hash
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.db.models import Q
from django.template import loader
from django.conf import settings
from django.forms.utils import ErrorList
from django.utils.timezone import datetime #important if using timezones
from forms import *
from models import *
from serializers import *
from profesor.models import *
from administrador.models import *
import json
import random
import string

# Create your views here.
class AlumnoListView(UserPassesTestMixin, ListView):
    model = Alumno
    template_name = 'alumno/alumno_list.html'

    
    def test_func(self):
        return self.request.user.is_superuser

    
    def get_queryset(self):
        return super(AlumnoListView, self).get_queryset().all()

    
    def get_context_data(self, **kwargs):
        context = super(AlumnoListView, self).get_context_data(**kwargs)
        context['tittle'] = "Alumnos"
        context['motto'] = "Tabla para visualizar Alumnos"
        context['table_id'] = "alumno"
        return context


class AlumnoCreateView(PermissionRequiredMixin, CreateView):
    form_class = AlumnoForm
    template_name = 'alumno/alumno_create.html'
    permission_required = (
        'alumno.list_alumnos', 
        'alumno.add_alumno', 
        'alumno.change_alumno', 
        'alumno.delete_alumno',
    )

    def send_mail_to_user(self, user, request):
        context = {
            'email': user.email,
            'domain': "%s%s"%('http://', request.META['HTTP_HOST']),
            'site_name': 'Seguimiento UCSG',
            'user': user,
            'protocol': 'https',
        }
        subject_template_name = 'alumno/new_account_subject.txt'
        email_template_name = 'alumno/new_account.html'
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
        return '/alumno/alumno-list/'

    def get(self, request, next=None):
        return super(AlumnoCreateView, self).get(request)

    def form_valid(self, form):
        try:
            if User.objects.filter(username=form.instance.user.username).exists():
                errors = form._errors.setdefault("email", ErrorList())
                errors.append(u"Ya existe un usuario registrado con este email")
                response = super(AlumnoCreateView, self).form_invalid(form)
            else:
                response = super(AlumnoCreateView, self).form_valid(form)
                _user_id_ = form.instance.user.id
                user = User.objects.filter(pk=_user_id_).first()
                self.send_mail_to_user(user, self.request)
        except Exception, e:
            print 'Error', e
            errors = form._errors.setdefault("email", ErrorList())
            errors.append(u"Ya existe un usuario registrado con este email")
            if form.instance.user.id:
                form.instance.user.delete()
            response = super(AlumnoCreateView, self).form_invalid(form)
        return response

    def form_invalid(self, form):
        return super(AlumnoCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AlumnoCreateView, self).get_context_data(**kwargs)
        context['tittle'] = "Alumnos"
        context['motto'] = "Formulario para crear un nuevo Alumno"
        return context


class AlumnoUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = AlumnoForm
    template_name = 'alumno/alumno_edit.html'
    success_url = '/alumno/alumno-list/'
    permission_required = (
        'alumno.list_alumnos', 
        'alumno.add_alumno', 
        'alumno.change_alumno', 
        'alumno.delete_alumno',
    )

    def get_object(self, queryset=None):
        if not Alumno.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        alumno = Alumno.objects.get(pk=self.kwargs['id'])
        if alumno.deleted:
            raise Http404
        return alumno

    def form_valid(self, form):
        clean = form.cleaned_data
        try:
            response = super(AlumnoUpdateView, self).form_valid(form)
        except Exception, e:
            print e
            errors = form._errors.setdefault("email", ErrorList())
            errors.append(u"Ya existe un usuario registrado con este email")
            response = super(AlumnoUpdateView, self).form_invalid(form)
        return response

    def form_invalid(self, form):
        return super(AlumnoUpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AlumnoUpdateView, self).get_context_data(**kwargs)
        context['tittle'] = "Alumnos"
        context['motto'] = "Formulario para editar Alumnos"
        return context


class AlumnoPasswordUpdateView(PermissionRequiredMixin, FormView):
    form_class = AlumnoSetPasswordForm
    template_name = 'alumno/alumno_create.html'
    success_url = '/alumno/alumno-list/'
    permission_required = (
        'alumno.list_alumnos', 
        'alumno.add_alumno', 
        'alumno.change_alumno', 
        'alumno.delete_alumno',
    )

    def get_form(self):
        if not Alumno.objects.filter(id=self.kwargs['id']).exists():
            raise Http404
        self.alumno = Alumno.objects.get(id=self.kwargs['id'])
        user = self.alumno.user
        if self.request.method == 'GET':
            form = self.form_class(user=user)
        elif self.request.method == 'POST':
            form = self.form_class(user=user, data=self.request.POST)
        return form

    def get_success_url(self):
        if Alumno.objects.filter(id=self.kwargs['id']).exists():
            return '/alumno/alumno-edit/%s/'%self.kwargs['id']
        else:
            return self.success_url

    def form_valid(self, form):
        form = self.get_form()
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, form.user)
        else:
            return super(AlumnoPasswordUpdateView, self).form_invalid(form)
        return super(AlumnoPasswordUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AlumnoPasswordUpdateView, self).get_context_data(**kwargs)
        context['tittle'] = "Alumnos"
        context['motto'] = u"Formulario para configurar la contraseña del Alumno %s %s"%(self.alumno.user.first_name, self.alumno.user.last_name)
        return context


class AlumnoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Alumno
    success_url = '/alumno/alumno-list/'
    permission_required = (
        'alumno.list_alumnos', 
        'alumno.add_alumno', 
        'alumno.change_alumno', 
        'alumno.delete_alumno',
    )

    def get_object(self):
        id = self.kwargs['id']
        alumno = Alumno.objects.get(id=id)
        _user_ = User.objects.filter(pk=alumno.user.id)
        _user_.delete()
        return alumno

    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)


class AlumnoProcesosListView(UserPassesTestMixin, ListView):
    model = ProcesoAlumno
    template_name = 'alumno/alumno_historial.html'

    
    def test_func(self):
        return self.request.user

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super(AlumnoProcesosListView, self).get_queryset().all()
        else:
            return super(AlumnoProcesosListView, self).get_queryset().filter(alumn_id=self.request.user.alumno.id)
    
    def get_context_data(self, **kwargs):
        context = super(AlumnoProcesosListView, self).get_context_data(**kwargs)
        context['tittle'] = "Seguimiento de Trámites"
        context['motto'] = "Bandeja de seguimiento"
        context['procesos'] = Proceso.objects.filter(deleted=False)
        context['table_id'] = "alumno"
        context['historial'] = Historial.objects.filter(deleted=False)
        context['carreras'] = Carrera.objects.filter(deleted=False)
        context['periodo'] = Periodo.objects.filter(deleted=False).first()
        return context


class ProcesoAlumnoCreateView(CreateView):
    model = ProcesoAlumno
    form_class = ProcesoAlumnoForm

    def post(self, request):
        if request.method == "POST":
            form = ProcesoAlumnoForm(request.POST)
            message = 'something wrong!'
            # process_id = request
            if(form.is_valid()):
                form.save()
                procesos = ProcesoAlumno.objects.latest('id')
                serializer = ProcesoAlumnoSerializer(procesos)
                return HttpResponse(json.dumps({'items': serializer.data}))
            else:
                print form.errors
                return HttpResponse(json.dumps({'message': message}))
        return HttpResponse(json.dumps({'message': message}))


class ProcesoAlumnoEditView(PermissionRequiredMixin, UpdateView):
    model = ProcesoAlumno
    form_class = ProcesoAlumnoCompleteForm

    template_name = 'alumno/alumno_edit.html'
    success_url = '/alumno/alumno-seguimiento/'
    permission_required = (
        'reporteria.add_reporter',
    )

    def send_mail_to_user(self, alumno, profesor, proceso_alumno, request):
        context = {
            'domain': "%s%s"%('http://', request.META['HTTP_HOST']),
            'site_name': 'Seguimiento UCSG',
            'protocol': 'https',
            'alumno': alumno,
            'profesor': profesor,
            'proceso_alumno': proceso_alumno,
            'today':datetime.today(),
            'link': reverse('alumno-seguimiento'),
        }
        _user_ = User.objects.filter(is_superuser=True).first()
        email_template_name = 'alumno/edit_process.html'
        subject = proceso_alumno
        email = loader.get_template(email_template_name).render(context)
        email_message = EmailMessage(
            subject,
            email,
            to=[alumno.user.email, profesor.user.email, _user_.email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)

    def test_func(self):
        return self.request.user
        
    def get_object(self, queryset=None):
        if not ProcesoAlumno.objects.filter(pk=self.kwargs['id']).exists():
            raise Http404
        proceso = ProcesoAlumno.objects.get(pk=self.kwargs['id'])
        if proceso.deleted:
            raise Http404
        return proceso

    def form_valid(self, form):
        clean = form.cleaned_data
        try:
            response = super(ProcesoAlumnoEditView, self).form_valid(form)

            proceso_alumno = ProcesoAlumno.objects.filter(pk=self.kwargs['id']).first()
            alumno = Alumno.objects.filter(pk=proceso_alumno.alumn_id).first()
            materia = Materia.objects.filter(name=proceso_alumno.subject).first()
            profesor = Profesor.objects.filter(subjects=materia).first()

            historial = Historial.objects.create(
                process=proceso_alumno, 
                name="Tramite en Estado %s"%(proceso_alumno.status_verbose()), 
                description="Tramite en Estado %s"%(proceso_alumno.status_verbose()),
                reviewed_by = ("%s %s")%(self.request.user.first_name, self.request.user.last_name),
                approved_by = ("%s %s")%(self.request.user.first_name, self.request.user.last_name),
            )
            historial.save()
            
            self.send_mail_to_user(alumno, profesor, proceso_alumno, self.request)

        except Exception, e:
            print e
            errors = form._errors.setdefault("error", ErrorList())
            errors.append(u"Ya existe un usuario registrado con este email")
            response = super(ProcesoAlumnoEditView, self).form_invalid(form)
        return response

    def form_invalid(self, form):
        return super(ProcesoAlumnoEditView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ProcesoAlumnoEditView, self).get_context_data(**kwargs)
        context['tittle'] = "Proceso"
        context['motto'] = "Formulario para editar Procesos de Alumnos"
        return context


class ProcesoAlumnoItemsCreateView(CreateView):
    model = ProcesoAlumnoItems
    form_class = ProcesoAlumnoItemsForm

    def post(self, request):
        if request.method == "POST":
            form = ProcesoAlumnoItemsForm(request.POST)
            message = 'something wrong!'
            # process_id = request
            if(form.is_valid()):
                form.save()
                proceos_items = ProcesoAlumnoItems.objects.latest('id')
                serializer = ProcesoAlumnoItemsSerializer(proceos_items)
                return HttpResponse(json.dumps({'items': serializer.data}))
            else:
                print form.errors
                return HttpResponse(json.dumps({'message': message}))
        return HttpResponse(json.dumps({'message': message}))


class AlumnoTramiteCreate(UserPassesTestMixin, CreateView):
    model = ProcesoAlumno
    fields = '__all__'
    template_name = 'alumno/alumno_tramite_create.html'
    success_url = '/alumno/alumno-seguimiento/'

    
    def test_func(self):
        return self.request.user.is_active

    def send_mail_to_user(self, alumno, profesor, proceso_alumno, request):
        context = {
            'domain': "%s%s"%('http://', request.META['HTTP_HOST']),
            'site_name': 'Seguimiento UCSG',
            'protocol': 'https',
            'alumno': alumno,
            'profesor': profesor,
            'proceso_alumno': proceso_alumno,
            'today':datetime.today(),
            'link': reverse('alumno-seguimiento'),
        }
        _user_ = User.objects.filter(is_superuser=True).first()
        email_template_name = 'alumno/create_process.html'
        subject = proceso_alumno
        email = loader.get_template(email_template_name).render(context)
        email_message = EmailMessage(
            subject,
            email,
            to=[alumno.user.email, profesor.user.email, _user_.email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)

    def post(self, request):
        if request.method == "POST":
            alumn_id = request.POST.get("alumno_id", "")
            if alumn_id:
                alumno = Alumno.objects.filter(pk=alumn_id).first()
            else:
                alumno = Alumno.objects.filter(user_id=self.request.user.id).first()
            proceso_alumno = ProcesoAlumno.objects.filter(alumn__id=alumno.id).latest('id')
            materia = Materia.objects.filter(name=proceso_alumno.subject).first()
            profesor = Profesor.objects.filter(subjects=materia).first()

            historial = Historial.objects.create(process=proceso_alumno, name="Tramite Ingresado", description="Tramite Ingresado por el Alumno %s %s"%(alumno.user.first_name, alumno.user.last_name))
            historial.save()
            
            self.send_mail_to_user(alumno, profesor, proceso_alumno, request)
        return HttpResponseRedirect(reverse('alumno-seguimiento'))
    
    def get_context_data(self, **kwargs):
        context = super(AlumnoTramiteCreate, self).get_context_data(**kwargs)
        context['tittle'] = "Crear Solicitud"
        context['motto'] = "Llene todos los datos"

        context['periodos'] = Periodo.objects.all()
        context['procesos'] = Proceso.objects.all()
        context['ciclos'] = Ciclo.objects.all()
        context['carreras'] = Carrera.objects.all()

        if self.request.user.is_superuser:
            context['materias'] = Materia.objects.all()
            context['alumnos'] = Alumno.objects.all()
        else:
            alumno = Alumno.objects.filter(user=self.request.user).first()
            context['materias'] = alumno.subjects.all()

        form = context['form']
        for field in form.fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
            if form.fields[field].help_text:
                form.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                form.fields[field].widget.attrs['data-placement'] = 'top'
                form.fields[field].widget.attrs['title'] = form.fields[field].help_text
        return context
    

class AlumnoNewCreateView(CreateView):
    form_class = AlumnoNewForm
    template_name = 'alumno/alumno_create.html'

    def send_mail_to_user(self, alumno, request):
        link = reverse_lazy('alumno-activate', kwargs={'token':alumno.token, 'username':alumno.user.username})
        context = {
            'email': alumno.user.email,
            'domain': "%s%s"%('http://', request.META['HTTP_HOST']),
            'site_name': 'Seguimiento UCSG',
            'alumno': alumno,
            'link': "%s%s%s"%('http://', request.META['HTTP_HOST'],link),
            'protocol': 'https',
        }
        subject_template_name = 'alumno/new_account_subject.txt'
        email_template_name = 'alumno/new_account_activate.html'
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        email = loader.get_template(email_template_name).render(context)
        email_message = EmailMessage(
            subject,
            email,
            to=[alumno.user.email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)
    
    def get_success_url(self):
        return reverse('alumno-resend')

    def get(self, request, next=None):
        return super(AlumnoNewCreateView, self).get(request)

    def form_valid(self, form):
        try:
            if User.objects.filter(username=form.instance.user.username).exists():
                errors = form._errors.setdefault("email", ErrorList())
                errors.append(u"Ya existe un usuario registrado con este email")
                response = super(AlumnoNewCreateView, self).form_invalid(form)
            else:
                response = super(AlumnoNewCreateView, self).form_valid(form)
                _user_id_ = form.instance.user.id
                user = User.objects.filter(pk=_user_id_).first()
                alumno = Alumno.objects.filter(user=user).first()
                token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
                alumno.token = token
                alumno.save()
                self.send_mail_to_user(alumno, self.request)
        except Exception, e:
            print 'Error', e
            errors = form._errors.setdefault("email", ErrorList())
            errors.append(u"Ya existe un usuario registrado con este email")
            if form.instance.user.id:
                form.instance.user.delete()
            response = super(AlumnoNewCreateView, self).form_invalid(form)
        return response

    def form_invalid(self, form):
        return super(AlumnoNewCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AlumnoNewCreateView, self).get_context_data(**kwargs)
        context['tittle'] = "Alumnos"
        context['motto'] = "Formulario para crear un nuevo Alumno"
        return context


class AlumnoActivateView(ListView):
    model = Alumno
    template_name = 'alumno/alumno_activate.html'

    def send_mail_to_user(self, alumno, request):
        link = reverse_lazy('alumno-activate', kwargs={'token':alumno.token, 'username':alumno.user.username})
        context = {
            'email': alumno.user.email,
            'domain': "%s%s"%('http://', request.META['HTTP_HOST']),
            'site_name': 'Seguimiento UCSG',
            'alumno': alumno,
            'link': "%s%s%s"%('http://', request.META['HTTP_HOST'],link),
            'protocol': 'https',
        }
        subject_template_name = 'alumno/new_account_subject.txt'
        email_template_name = 'alumno/new_account_activate.html'
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        email = loader.get_template(email_template_name).render(context)
        email_message = EmailMessage(
            subject,
            email,
            to=[alumno.user.email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        user = User.objects.filter(username=username).first()
        token = kwargs.get('token', None)
        try:
            alumno = Alumno.objects.get(user__username=username)
            if alumno.token == token:
                alumno.is_active = True
                alumno.save()
                login(request, user)
                next = request.GET.get('next')
                if next is not None:
                    return redirect(next)
                return redirect('/')
            else:
                token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
                alumno.token = token
                alumno.save()
                self.send_mail_to_user(alumno, self.request)
                raise Http404
        except Exception as e:
            raise Http404


class AlumnoResendView(TemplateView):
    alert_message = {'class': 'alert alert-warning', 'mod': 'Aviso:', 'message': u'Para poder ingresar al sistema debe de activar su cuenta, se ha enviado el link de activación al correo electrónico ingresado anteriormente. Porfavor revisar.'}
    template_name = 'alumno/alumno_resend.html'

    def send_mail_to_user(self, alumno, request):
        link = reverse_lazy('alumno-activate', kwargs={'token':alumno.token, 'username':alumno.user.username})
        context = {
            'email': alumno.user.email,
            'domain': "%s%s"%('http://', request.META['HTTP_HOST']),
            'site_name': 'Seguimiento UCSG',
            'alumno': alumno,
            'link': "%s%s%s"%('http://', request.META['HTTP_HOST'],link),
            'protocol': 'https',
        }
        subject_template_name = 'alumno/new_account_subject.txt'
        email_template_name = 'alumno/new_account_activate.html'
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        email = loader.get_template(email_template_name).render(context)
        email_message = EmailMessage(
            subject,
            email,
            to=[alumno.user.email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)

    def post(self, request):
        if request.method == "POST":
            email = request.POST.get("id_email", "")
            if email:
                user = User.objects.filter(email=email).first()
                if user:
                    alumno = Alumno.objects.filter(user=user).first()
                    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
                    alumno.token = token
                    alumno.save()
                    self.send_mail_to_user(alumno, self.request)
                    self.alert_message = {'class': 'alert alert-success',
                    'mod': 'Envío exitoso:',
                    'message': u'El correo ha sido enviado.'}
                else:
                    self.alert_message = {'class': 'alert alert-danger',
                    'mod': 'Envio exitoso:',
                    'message': u'Ingrese un correo electrónico válido.'}
            else:
                self.alert_message = {'class': 'alert alert-danger',
                'mod': 'Error:',
                'message': u'Ingrese un correo electrónico.'}
            return self.get(request)

    def get_success_url(self):
        return "/"

    def get(self, request, next=None):
        return super(AlumnoResendView, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(AlumnoResendView, self).get_context_data(**kwargs)
        context['alert_message'] = self.alert_message
        context['tittle'] = "Alumnos"
        context['motto'] = "Reenviar Correo Activación"
        return context


class AlumnoResetView(TemplateView):
    alert_message = None
    template_name = 'alumno/alumno_reset.html'

    def send_mail_to_user(self, user, token, request):
        link = reverse('administrador-login')
        context = {
            'email': user.email,
            'domain': "%s%s"%('http://', request.META['HTTP_HOST']),
            'site_name': 'Seguimiento UCSG',
            'user': user,
            'token': token,
            'link': "%s%s%s"%('http://', request.META['HTTP_HOST'],link),
            'protocol': 'https',
        }
        email_template_name = 'alumno/account_reset.html'
        subject = 'Recuperar Contraseña'
        email = loader.get_template(email_template_name).render(context)
        email_message = EmailMessage(
            subject,
            email,
            to=[user.email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)

    def post(self, request):
        if request.method == "POST":
            email = request.POST.get("id_email", "")
            if email:
                user = User.objects.filter(email=email).first()
                if user:
                    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
                    user.set_password(token)
                    user.save()
                    self.send_mail_to_user(user, token, self.request)
                    self.alert_message = {'class': 'alert alert-success',
                    'mod': 'Cambio exitoso:',
                    'message': u'Se ha enviado un correo con tu nueva contraseña.'}
                else:
                    self.alert_message = {'class': 'alert alert-danger',
                    'mod': 'Envio exitoso:',
                    'message': u'Ingrese un correo electrónico válido.'}
            else:
                self.alert_message = {'class': 'alert alert-danger',
                'mod': 'Error:',
                'message': u'Ingrese un correo electrónico.'}
            return self.get(request)

    def get_success_url(self):
        return "/"

    def get(self, request, next=None):
        return super(AlumnoResetView, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(AlumnoResetView, self).get_context_data(**kwargs)
        context['alert_message'] = self.alert_message
        context['tittle'] = "Alumnos"
        context['motto'] = "Recuperar Contraseña"
        return context

