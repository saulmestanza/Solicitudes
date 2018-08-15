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


