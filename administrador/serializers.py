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


