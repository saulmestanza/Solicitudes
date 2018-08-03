# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy, ugettext as _, ungettext
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.files.base import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy, ugettext as _
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.core.files.base import File
# from magic import from_buffer

import json
import urllib2
import mimetypes
import socket

from math import sin, cos, sqrt, atan2, radians
"""
@deconstructible
class FileValidator(object):
    DEFAULT_CONTENT_TYPE = 'application/x-empty'

    error_messages = {
     'max_size': _(u"Max file size exceed %(max_size)s."
                  u" The file size is %(size)s."),
     'min_size': _(u"Min file size unreached %(min_size)s."
                  u" The file size is %(size)s."),
     'content_type': _(u"Content type %(content_type)s unsupported."),
    }
    
    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types
    
    def __call__(self, data):
        params = {}
        error_list = []
        if hasattr(data, 'size'):
            data_size = data.size
        elif hasattr(data, '__len__'):
            data_size = len(data)
        else:
            data_size = 0
        if self.max_size is not None and data_size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size), 
                'size': filesizeformat(data_size),
            }
            error_list.append( 
                ValidationError(self.error_messages['max_size'], 'max_size', params)
            )
        if self.min_size is not None and data_size < self.min_size:
            params = {
                'min_size': filesizeformat(self.mix_size),
                'size': filesizeformat(data_size)
            }
            error_list.append( 
                ValidationError(self.error_messages['min_size'], 'min_size', params)
            )
        if self.content_types:
            content_type = self.content_type_from_data(data)
            if content_type not in self.content_types:
                params = { 'content_type': content_type }
                error_list.append(
                    ValidationError(self.error_messages['content_type'], 'content_type', params)
                )
        if error_list != []:
            raise ValidationError(error_list)

    @classmethod
    def content_type_from_data(cls, data):
        SIZE = 1024
        content_type = cls.DEFAULT_CONTENT_TYPE
        if isinstance(data, File):
            data.open('rb')
            content_type = from_buffer(data.read(SIZE), mime=True)
        elif hasattr(data, 'file'):
            if hasattr(data.file, 'name'):
                content_type = from_buffer(open(data.file.name, 'rb').read(SIZE), mime=True)
        elif hasattr(data, 'name'):
            content_type = from_buffer(open(data.name, 'rb').read(SIZE), mime=True)
        elif type(data).__name__ == 'str' or type(data).__name__ == 'unicode':
            content_type = from_buffer(data[:SIZE], mime=True)
        print(content_type)
        return content_type

    def __eq__(self, other):
        return isinstance(other, FileValidator)


def validate_file(value, max_size=None, min_size=None, content_types=()):
    FileValidator(max_size=max_size, min_size=min_size, content_types=content_types)(value)


class Base64BufferValidator(FileValidator):
    docstring for Base64BufferValidator

    def __call__(self, data):
        data = base64.b64decode(data)
        super(Base64BufferValidator, self).__call__(data)
"""

def get_client_ip(request):
    """
     Método para obtener el ip del usuario.

    :returns: el ip del usuario. 
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IPUserCORSCheckerMixin:
    """docstring for IPUserCORSChecker"""

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip  
  
    @classmethod
    def is_valid_ip(cls, ip_address):
        """ Check Validity of an IP address """
        valid = True
        try:
            socket.inet_aton(ip_address.strip())
        except:
            valid = False
        return valid

    @classmethod
    def get_ip_address_from_request(cls, request):
        """ Makes the best attempt to get the client's real IP or return the loopback """
        PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.' )
        ip_address = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if x_forwarded_for and ',' not in x_forwarded_for:
            if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and cls.is_valid_ip(x_forwarded_for):
                ip_address = x_forwarded_for.strip()
        else:
            ips = [ip.strip() for ip in x_forwarded_for.split(',')]
            for ip in ips:
                if ip.startswith(PRIVATE_IPS_PREFIX):
                    continue
                elif not cls.is_valid_ip(ip):
                    continue
                else:
                    ip_address = ip
                    break
        if not ip_address:
            x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
            if x_real_ip:
                if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and cls.is_valid_ip(x_real_ip):
                    ip_address = x_real_ip.strip()
        if not ip_address:
            remote_addr = request.META.get('REMOTE_ADDR', '')
            if remote_addr:
                if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and cls.is_valid_ip(remote_addr):
                    ip_address = remote_addr.strip()
        if not ip_address:
            ip_address = '127.0.0.1'
        return ip_address

    def isAllowedUserIP(self, request):
        if hasattr(request, 'user'):
            if hasattr(request.user, 'userprofile'):
                userprofile = request.user.userprofile
                # user_ip = self.get_client_ip(request)
                user_ip = self.get_ip_address_from_request(request)

                for ip_address in userprofile.whitelist_ips.all():
                    print(ip_address.ip_address, user_ip)
                    if ip_address.ip_address == user_ip:
                        return True
        return False



@deconstructible
class FileValidator(object):
    DEFAULT_CONTENT_TYPE = 'application/x-empty'

    error_messages = {
     'content_type': _(u"Content type %(content_type)s unsupported."),
    }
    
    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.content_types = content_types
    
    def __call__(self, data):
        params = {}
        error_list = []
        if hasattr(data, 'size'):
            data_size = data.size
        elif hasattr(data, '__len__'):
            try:
                data_size = len(data)
            except Exception as e:
                print(e)
                data_size = 0
                pass
        else:
            data_size = 0
        if self.content_types:
            try:
                content_type = self.content_type_from_data(data)
                if content_type not in self.content_types:
                    params = { 'content_type': content_type }
                    error_list.append(
                        ValidationError(self.error_messages['content_type'], 'content_type', params)
                    )
            except:
                pass
        if error_list != []:
            raise ValidationError(error_list)
        