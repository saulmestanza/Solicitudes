# -*- coding: utf-8 -*-
from captcha.fields import CaptchaField
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm, SetPasswordForm
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from functools import partial
from models import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label=u'Contraseña', widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserForm(UserChangeForm):
    READ_ONLY_FIELDS = ['date_joined',
    'last_login',]
    HIDDEN_FIELDS = ['password',]
    NO_FORM_CONTROL_FIELDS = ['is_active',
    'is_staff',
    'is_superuser']

    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        ]

    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if not field in UserForm.NO_FORM_CONTROL_FIELDS:
                self.fields[field].widget.attrs['class'] = 'form-control'
            if field in UserForm.READ_ONLY_FIELDS:
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                #
                clean_method_name = "clean_%s" % field
                print clean_method_name
                assert clean_method_name not in dir(self)
                setattr(self, clean_method_name, partial(self._clean_for_readonly_field, fname=field))

            if field in UserForm.HIDDEN_FIELDS:
                self.fields[field].widget = forms.HiddenInput()

            if field == 'password':
                self.fields[field].help_text = _(u"Las contraseñas no se almacenan en texto plano, por lo que no hay forma de ver la de este usuario,\
                    pero puede cambiar la contraseña usando <a href=\"/administrador/user-edit-password/%s/\">este formulario</a>."%self.instance.username)

            if self.fields[field].help_text:
                self.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                self.fields[field].widget.attrs['data-placement'] = 'top'
                self.fields[field].widget.attrs['title'] = self.fields[field].help_text

    
    def _clean_for_readonly_field(self, fname):
        print self.initial[fname]
        return self.initial[fname]


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            #
            if self.fields[field].help_text:
                self.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                self.fields[field].widget.attrs['data-placement'] = 'top'
                self.fields[field].widget.attrs['data-html'] = 'true'
                self.fields[field].widget.attrs['title'] = mark_safe( self.fields[field].help_text )


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )
        exclude =('password', )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            #
            if self.fields[field].help_text:
                self.fields[field].widget.attrs['data-toggle'] = 'tooltip'
                self.fields[field].widget.attrs['data-placement'] = 'top'
                self.fields[field].widget.attrs['title'] = self.fields[field].help_text

            if field == 'is_staff':
                self.fields[field].initial = True


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


UserProfileFormSet = inlineformset_factory(User,
    UserProfile,
    form=UserProfileForm,
    extra=1,
    can_delete=False,
    max_num=1,)


class FacultadForm(forms.ModelForm):

    class Meta:
        model = Facultad
        fields = (
            'name',
            'carrer',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(FacultadForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CarreraForm(forms.ModelForm):

    class Meta:
        model = Carrera
        fields = (
            'name',
            'cicles',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(CarreraForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CicloForm(forms.ModelForm):

    class Meta:
        model = Ciclo
        fields = (
            'name',
            'subjects',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(CicloForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class MateriaForm(forms.ModelForm):

    class Meta:
        model = Materia
        fields = (
            'name',
            'description',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(MateriaForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AxesCaptchaForm(forms.Form):
    captcha = CaptchaField()


class ProcesoForm(forms.ModelForm):

    class Meta:
        model = Proceso
        fields = (
            'name',
            'proceso_items',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(ProcesoForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ProcesoItemsForm(forms.ModelForm):

    class Meta:
        model = ProcesoItems
        fields = (
            'name',
            'description',
            'image',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(ProcesoItemsForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PeriodoForm(forms.ModelForm):

    class Meta:
        model = Periodo
        fields = ( '__all__')
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(PeriodoForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
