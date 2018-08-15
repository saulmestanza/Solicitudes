# -*- coding: utf-8 -*-
from django.core.files.base import ContentFile

from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core import exceptions
from django.utils import timezone
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Permission
from rest_framework import serializers

from models import *

class ProcesoAlumnoItemsSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	name = serializers.CharField(required=False)
	process_id = serializers.IntegerField(required=False)
	description = serializers.CharField(required=False)

	class Meta:
		model = ProcesoAlumnoItems
		fields = (
			'id',
			'name',
			'process_id',
			'process_alumno',
			'description',
		)
		depth = 1
		read_only_fields = (
			'id', 'deleted',
			)

	def __init__(self, *args, **kwargs):
		self.is_update = kwargs.pop('is_update', False)
		super(ProcesoAlumnoItemsSerializer, self).__init__(*args, **kwargs)

	def validate(self, data):
		result = super(ProcesoAlumnoItemsSerializer, self).validate(data)
		return result


class ProcesoAlumnoSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	process_id = serializers.IntegerField(required=False)
	alumn_id = serializers.IntegerField(required=False)
	subject = serializers.CharField(required=False)

	class Meta:
		model = ProcesoAlumno
		fields = (
			'id',
			'alumn',
			'process_id',
			'alumn_id',
			'process',
			'subject',
		)
		depth = 1
		read_only_fields = (
			'id', 'deleted',
			)

	def __init__(self, *args, **kwargs):
		self.is_update = kwargs.pop('is_update', False)
		super(ProcesoAlumnoSerializer, self).__init__(*args, **kwargs)

	def validate(self, data):
		result = super(ProcesoAlumnoSerializer, self).validate(data)
		return result

