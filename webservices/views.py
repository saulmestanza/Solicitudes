# -*- coding: utf-8 -*-
from django.http import Http404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Q
from django.template import loader
from django.utils.encoding import force_bytes
from django.http import HttpResponse, StreamingHttpResponse, Http404, FileResponse
from django.utils.translation import ugettext as _
from django.utils.timezone import datetime 
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.reverse import reverse_lazy
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle

from administrador.models import *
from administrador.serializers import *
from profesor.models import *
from alumno.models import *
from alumno.serializers import *


class CarrerasAPIView(APIView):
	DOES_NOT_EXISTS_RESPONSE = Response(
		{ "non_field_errors": ["DoesNotExist: Carrera matching query does not exist."] },
		status=status.HTTP_404_NOT_FOUND
	)

	permission_classes = (
		permissions.AllowAny,
	)
	queryset = Carrera.objects.all()
	throttle_classes = (
		UserRateThrottle,
	)

	def get(self, request, **kwargs):
		faculty_id = kwargs.get('id', None)
		if faculty_id:
			carreras = Carrera.objects.filter(faculty=faculty_id, deleted=False)
			if carreras:
				serializer = CarreraSerializer(carreras, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
		return self.DOES_NOT_EXISTS_RESPONSE


class CiclosAPIView(APIView):
	DOES_NOT_EXISTS_RESPONSE = Response(
		{ "non_field_errors": ["DoesNotExist: Ciclo matching query does not exist."] },
		status=status.HTTP_404_NOT_FOUND
	)

	permission_classes = (
		permissions.AllowAny,
	)
	queryset = Ciclo.objects.all()
	throttle_classes = (
		UserRateThrottle,
	)

	def get(self, request, **kwargs):
		carrer_id = kwargs.get('id', None)
		if carrer_id:
			carreras = Ciclo.objects.filter(carrer=carrer_id, deleted=False)
			if carreras:
				serializer = CicloSerializer(carreras, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
		return self.DOES_NOT_EXISTS_RESPONSE


class MateriaAPIView(APIView):
	DOES_NOT_EXISTS_RESPONSE = Response(
		{ "non_field_errors": ["DoesNotExist: Materia matching query does not exist."] },
		status=status.HTTP_404_NOT_FOUND
	)

	permission_classes = (
		permissions.AllowAny,
	)
	queryset = Materia.objects.all()
	throttle_classes = (
		UserRateThrottle,
	)

	def get(self, request, **kwargs):
		ciclo_id = kwargs.get('id', None)
		if ciclo_id:
			carreras = Materia.objects.filter(cicles=ciclo_id, deleted=False)
			if carreras:
				serializer = MateriaSerializer(carreras, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
		return self.DOES_NOT_EXISTS_RESPONSE


class ProfesorMateriaAPIView(APIView):
	DOES_NOT_EXISTS_RESPONSE = Response(
		{ "non_field_errors": ["DoesNotExist: Materia matching query does not exist."] },
		status=status.HTTP_404_NOT_FOUND
	)

	permission_classes = (
		permissions.AllowAny,
	)
	queryset = Materia.objects.all()
	throttle_classes = (
		UserRateThrottle,
	)

	def get(self, request, **kwargs):
		profesor_id = kwargs.get('id', None)
		if profesor_id:
			profesor = Profesor.objects.filter(pk=profesor_id).first()
			materias = []
			for subject in profesor.subjects.all():
				materias.append(subject.name)
			_materias_ = Materia.objects.filter(name__in=materias, deleted=False)
			if _materias_:
				serializer = MateriaSerializer(_materias_, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
		return self.DOES_NOT_EXISTS_RESPONSE


class ProcesoAlumnoStatsAPIView(APIView):
	DOES_NOT_EXISTS_RESPONSE = Response(
		{ "non_field_errors": ["DoesNotExist: Materia matching query does not exist."] },
		status=status.HTTP_404_NOT_FOUND
	)

	permission_classes = (
		permissions.AllowAny,
	)
	queryset = ProcesoAlumno.objects.all()
	throttle_classes = (
		UserRateThrottle,
	)

	def post(self, request, **kwargs):
		process = request.POST.get("process", "")
		carrer = request.POST.get("carrer", "")
		profesor = request.POST.get("profesor", "")
		materia = request.POST.get("materia", "")
		periodo = request.POST.get("periodo", "")
		parcial = request.POST.get("parcial", "")
		estado = request.POST.get("estado", "")
		tiempo_inicio = request.POST.get("tiempo_inicio", "")
		tiempo_fin = request.POST.get("tiempo_fin", "")

		proceso_alumno = ProcesoAlumno.objects.filter(deleted=False)

		if process:
			proceso_alumno = proceso_alumno.filter(process__id=process)
		if carrer:
			proceso_alumno = proceso_alumno.filter(subject__cicles__carrer__id=carrer)
		if periodo:
			_periodo_ = Periodo.objects.filter(pk=periodo).first()
			proceso_alumno = proceso_alumno.filter(periodo=_periodo_.name)
		if parcial:
			 proceso_alumno = proceso_alumno.filter(Q(parcial=parcial) | Q(parcial=''))
		if estado:
			proceso_alumno = proceso_alumno.filter(status=estado)
		if materia:
			proceso_alumno = proceso_alumno.filter(subject__id=materia)
		if tiempo_inicio and tiempo_fin:
			proceso_alumno = proceso_alumno.filter(creation_date__range=(tiempo_inicio, tiempo_fin))

		serializer = ProcesoAlumnoWSSerializer(proceso_alumno, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

