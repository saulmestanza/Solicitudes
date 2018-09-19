# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DeleteView, TemplateView
from django.core.files import File
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import update_session_auth_hash
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect, FileResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.db.models import Q
from django.template import loader
from django.conf import settings
from django.forms.utils import ErrorList
from django.utils.timezone import datetime #important if using timezones
from models import *
from forms import *
from profesor.models import *
from administrador.models import *
from alumno.models import *
from alumno.choices import STATUS_CHOICE
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
import json
import random
import string
import os
import io


class ReporteriaNotasCreateView(PermissionRequiredMixin, FormView):
    form_class = ReporterForm
    template_name = 'reporteria/reporter_notas.html'
    success_url = '/reporteria/reporteria-notas/'
    proceso_alumno = None
    permission_required = (
        'reporteria.add_reporter',
    )

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def test_func(self):
        return self.request.user

    def generate_pdf(self, request, carrer):
        sample_style_sheet = getSampleStyleSheet()
        count = Reporter.objects.count()
        doc = SimpleDocTemplate(settings.BASE_DIR+"/reporte_%s.pdf"%(count), pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        elements = []
        I = Image(settings.BASE_DIR+'/header.png')
        I.drawHeight =  1.5*inch
        I.drawWidth = 3*inch
        elements.append(I)
        self.proceso_alumno.order_by('process__subject__cicles__carrer__name', 'process__name')
        process = Proceso.objects.filter(deleted=False)
        if not carrer:
            carrer = Carrera.objects.filter(deleted=False)
        else:
            carrer = Carrera.objects.filter(pk=carrer)

        for carrera in carrer:
            heading_carrera = Paragraph(u'%s'%(carrera.name), sample_style_sheet['Heading2'])
            for proceso in process:
                heading_proceso = Paragraph(proceso.name, sample_style_sheet['Heading3'])
                data = [
                    ["Carrera", "Materia", "Estudiante", "Docente", "Parcial", "Nota"],
                ]
                for proceso_alumn in self.proceso_alumno:
                    if proceso.name == proceso_alumn.process.name and proceso_alumn.subject.cicles.carrer.name == carrera.name:
                        myList = []
                        myList.append(proceso_alumn.subject.cicles.carrer.name)
                        myList.append(proceso_alumn.subject.name)

                        _profesor_ = ""
                        _nota_ = 0.0
                        i = 0
                        for nota in proceso_alumn.notes.all():
                            if _profesor_ == "":
                                _profesor_ = nota.profesor
                            _nota_ = _nota_ + float(nota.nota)
                            i = i+1
                        if _nota_ != 0.0:
                            _nota_ = _nota_ / i

                        myList.append("%s %s"%(proceso_alumn.alumn.user.first_name, proceso_alumn.alumn.user.last_name))

                        myList.append(_profesor_)

                        myList.append(proceso_alumn.parcial)

                        myList.append(str(_nota_))

                        data.append(myList)
                style = TableStyle(
                    [
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 0), (-1, -1), 12),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                    ]
                )
                s = getSampleStyleSheet()
                s = s["BodyText"]
                s.wordWrap = 'CJK'
                if len(data) > 1:
                    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
                    t=Table(data2)
                    t.setStyle(style)
                    elements.append(heading_carrera)
                    elements.append(heading_proceso)
                    elements.append(t)
        doc.build(elements)
        _file_ = File(open(settings.BASE_DIR+"/reporte_%s.pdf"%(count), 'rb'))
        reporte = Reporter.objects.create(
            # pdf_file = _file_,
            created_by = ("%s %s")%(self.request.user.first_name, self.request.user.last_name)
        )
        os.remove(settings.BASE_DIR+"/reporte_%s.pdf"%(count))

        document = _file_.read()
        return HttpResponse(document, content_type="application/pdf")

    def post(self, request, *args, **kwargs):
        process = request.POST.get("process", "")
        carrer = request.POST.get("carrer", "")
        periodo = request.POST.get("periodo", "")
        parcial = request.POST.get("parcial", "")
        if process:
            self.proceso_alumno = ProcesoAlumno.objects.filter(process__id=process, status = 'FN')
        else:
            self.proceso_alumno = ProcesoAlumno.objects.filter(status = 'FN')
        if carrer:
            self.proceso_alumno = self.proceso_alumno.filter(subject__cicles__carrer__id=carrer)
        if periodo:
            _periodo_ = Periodo.objects.filter(pk=periodo).first()
            self.proceso_alumno = self.proceso_alumno.filter(periodo=_periodo_.name)
        if parcial:
             self.proceso_alumno = self.proceso_alumno.filter(Q(parcial=parcial) | Q(parcial=''))
        return self.generate_pdf(self, carrer)
        # return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super(ReporteriaNotasCreateView, self).get_context_data(**kwargs)
        context['tittle'] = "Reportes"
        context['procesos'] = Proceso.objects.filter(deleted=False)
        context['carrers'] = Carrera.objects.filter(deleted=False)
        context['periodos'] = Periodo.objects.filter(deleted=False)
        context['proceso_alumno'] = self.proceso_alumno
        context['motto'] = "Reportes Notas"
        return context



class ReporteriaEstadisticasCreateView(PermissionRequiredMixin, FormView):
    model = Reporter
    form_class = ReporterForm
    template_name = 'reporteria/reporter_estadisticas.html'
    success_url = '/reporteria/reporteria-estadisticas/'
    proceso_alumno = None
    permission_required = (
        'reporteria.add_reporter',
    )

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def test_func(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ReporteriaEstadisticasCreateView, self).get_context_data(**kwargs)
        context['tittle'] = "Reportes"
        context['procesos'] = Proceso.objects.filter(deleted=False)
        context['carrers'] = Carrera.objects.filter(deleted=False)
        context['periodos'] = Periodo.objects.filter(deleted=False)
        context['materias'] = Materia.objects.filter(deleted=False)
        context['choices'] = STATUS_CHOICE
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            profesor = Profesor.objects.filter(user=self.request.user).first()
            context['profesor'] = profesor
        else:
            context['profesor'] = None
        context['profesores'] = Profesor.objects.filter(deleted=False)
        context['proceso_alumno'] = ProcesoAlumno.objects.filter(status='FN')
        context['motto'] = "Reportes Estadísticos"
        return context

