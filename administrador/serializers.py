# -*- coding: utf-8 -*-
import base64

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

class ProcesoItemsSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	name = serializers.CharField(required=False)
	description = serializers.CharField(required=False)

	class Meta:
		model = ProcesoItems
		fields = (
			'id',
			'name',
			'description',
		)
		depth = 1
		read_only_fields = (
			'id', 'deleted',
			)

	def __init__(self, *args, **kwargs):
		self.is_update = kwargs.pop('is_update', False)
		super(ProcesoItemsSerializer, self).__init__(*args, **kwargs)

	def validate(self, data):
		result = super(ProcesoItemsSerializer, self).validate(data)
		return result


class FacultadSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)

	class Meta:
		model = Facultad
		fields = (
			'id',
			'name',
		)
		depth = 1
		read_only_fields = (
			'id', 'deleted',
			)

	def __init__(self, *args, **kwargs):
		self.is_update = kwargs.pop('is_update', False)
		super(FacultadSerializer, self).__init__(*args, **kwargs)

	def validate(self, data):
		result = super(FacultadSerializer, self).validate(data)
		return result


class CarreraSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	faculty = FacultadSerializer(required=False)

	class Meta:
		model = Carrera
		fields = (
			'id',
			'name',
			'faculty',
		)
		depth = 1
		read_only_fields = (
			'id', 'deleted',
			)

	def __init__(self, *args, **kwargs):
		self.is_update = kwargs.pop('is_update', False)
		super(CarreraSerializer, self).__init__(*args, **kwargs)

	def validate(self, data):
		result = super(CarreraSerializer, self).validate(data)
		return result


class CicloSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	carrer = CarreraSerializer(required=False)

	class Meta:
		model = Ciclo
		fields = (
			'id',
			'name',
			'carrer',
		)
		depth = 1
		read_only_fields = (
			'id', 'deleted',
			)

	def __init__(self, *args, **kwargs):
		self.is_update = kwargs.pop('is_update', False)
		super(CicloSerializer, self).__init__(*args, **kwargs)

	def validate(self, data):
		result = super(CicloSerializer, self).validate(data)
		return result


class MateriaSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	cicles = CicloSerializer(required=False)

	class Meta:
		model = Materia
		fields = (
			'id',
			'name',
			'description',
			'cicles',
		)
		depth = 1
		read_only_fields = (
			'id', 'deleted',
			)

	def __init__(self, *args, **kwargs):
		self.is_update = kwargs.pop('is_update', False)
		super(MateriaSerializer, self).__init__(*args, **kwargs)

	def validate(self, data):
		result = super(MateriaSerializer, self).validate(data)
		return result
