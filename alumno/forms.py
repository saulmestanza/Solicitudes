# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm, SetPasswordForm
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from functools import partial
from models import *
from administrador.models import *
from profesor.models import *
from choices import STATUS_CHOICE

class AlumnoForm(forms.ModelForm):
    READ_ONLY_FIELDS = []

    required_css_class = 'required'
    is_new = False

    first_name = forms.CharField(label=u'Nombre', max_length=30)
    last_name = forms.CharField(label=u'Apellido', max_length=30)
    email = forms.EmailField(label=u'Email', max_length=254, required=True)
    password = forms.CharField(label=_(u'Contraseña'), widget=forms.HiddenInput, required=False)
    # is_active = forms.BooleanField(label=u'Activo', required=False)
    
    def __init__(self, *args, **kw):
        super(AlumnoForm, self).__init__(*args, **kw)
        if not hasattr(self.instance, 'user'):
            alumno_count = User.objects.filter(email__icontains='anonymous@cu.ucsg.edu.ec').count()
            alumno_username = 'Alumno_%d'%(alumno_count + 1)
            alumno_user = User(username=alumno_username)
            alumno_user.set_password('blife2017cn')
            self.instance.user = alumno_user 
            self.is_new = True
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

        self.fields['first_name'].widget.attrs['style'] = 'text-transform: capitalize;'
        self.fields['last_name'].widget.attrs['style'] = 'text-transform: capitalize;'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field in AlumnoForm.READ_ONLY_FIELDS:
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                clean_method_name = "clean_%s" % field
                assert clean_method_name not in dir(self)
                setattr(self, clean_method_name, partial(self._clean_for_readonly_field, fname=field))
            if field == 'password':
                self.fields[field].help_text = _(u"Las contraseñas no se almacenan en texto plano, por lo que no hay forma de ver la de este usuario,\
                    pero puede cambiar la contraseña usando <a href=\"/alumno/alumno-edit-password/%s/\">este formulario</a>."%self.instance.id)

    
    def save(self, *args, **kw):
        # is_active = self.cleaned_data.get('is_active')
        self.instance.user.first_name = self.cleaned_data.get('first_name').title()
        self.instance.user.last_name = self.cleaned_data.get('last_name').title()
        email = self.cleaned_data.get('email')
        self.instance.user.email = email
        self.instance.user.is_staff = False
        self.instance.user.username = email
        self.instance.user.set_password(email)
        self.instance.user.is_active = True
        user = self.instance.user
        user.save()
        if Group.objects.filter(name='Estudiantes').exists():
            user.groups.add( Group.objects.get(name='Estudiantes') )

        self.instance.user = user
        super(AlumnoForm, self).save(*args, **kw)
        return AlumnoForm

    
    def as_plain(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = '<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row = '%s',
            row_ender = '</p>',
            help_text_html = ' <span class="helptext">%s</span>',
            errors_on_separate_row = True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@cu.ucsg.edu.ec' in email:
            return email
        else:
            raise forms.ValidationError("Ingrese un correo válido")

    def _clean_for_readonly_field(self, fname):
        return self.cleaned_data[fname]

    
    class Meta:
        model = Alumno
        fields = [
            'user',
            'first_name',
            'last_name',
            'email',
            'carrer',
            # 'is_active',
            ]
        exclude = ( 'user', )


class AlumnoNewForm(forms.ModelForm):
    READ_ONLY_FIELDS = []

    required_css_class = 'required'
    is_new = False

    first_name = forms.CharField(label=u'Nombre', max_length=30)
    last_name = forms.CharField(label=u'Apellido', max_length=30)
    email = forms.EmailField(label=u'Email', max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label=_(u'Contraseña'), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label=_(u'Confirmar contraseña'), required=True)
    
    def __init__(self, *args, **kw):
        super(AlumnoNewForm, self).__init__(*args, **kw)
        if not hasattr(self.instance, 'user'):
            alumno_count = User.objects.filter(email__icontains='anonymous@cu.ucsg.edu.ec').count()
            alumno_username = 'Alumno_%d'%(alumno_count + 1)
            alumno_user = User(username=alumno_username)
            alumno_user.set_password('blife2017cn')
            self.instance.user = alumno_user 
            self.is_new = True
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

        self.fields['first_name'].widget.attrs['style'] = 'text-transform: capitalize;'
        self.fields['last_name'].widget.attrs['style'] = 'text-transform: capitalize;'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field in AlumnoNewForm.READ_ONLY_FIELDS:
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                clean_method_name = "clean_%s" % field
                assert clean_method_name not in dir(self)
                setattr(self, clean_method_name, partial(self._clean_for_readonly_field, fname=field))

    
    def save(self, *args, **kw):
        self.instance.user.first_name = self.cleaned_data.get('first_name').title()
        self.instance.user.last_name = self.cleaned_data.get('last_name').title()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        self.instance.user.email = email
        self.instance.user.is_staff = False
        self.instance.user.username = email
        self.instance.user.set_password(password)
        self.instance.user.is_active = True
        user = self.instance.user
        user.save()
        if Group.objects.filter(name='Estudiantes').exists():
            user.groups.add( Group.objects.get(name='Estudiantes') )

        self.instance.user = user
        super(AlumnoNewForm, self).save(*args, **kw)
        return AlumnoNewForm

    
    def as_plain(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row = '<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row = '%s',
            row_ender = '</p>',
            help_text_html = ' <span class="helptext">%s</span>',
            errors_on_separate_row = True)

    def clean(self):
        min_length = 7

        cleaned_data = super(AlumnoNewForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("password", "Contraseña y Confirmar Contraseña no son iguales")
        elif len(password) < min_length:
            self.add_error("password", ("Contraseña debe de tener {0} o más caracteres").format(min_length))
        elif not any(char.isdigit() for char in password):
            self.add_error("password", 'La contraseña debe contener al menos 1 dígito.')
        elif not any(char.isalpha() for char in password):
            self.add_error("password", 'La contraseña debe contener al menos 1 letra.')
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@cu.ucsg.edu.ec' in email:
            return email
        else:
            raise forms.ValidationError("Ingrese un correo válido")

    def _clean_for_readonly_field(self, fname):
        return self.cleaned_data[fname]

    
    class Meta:
        model = Alumno
        fields = [
            'user',
            'first_name',
            'last_name',
            'email',
            'carrer',
            'password',
            ]
        exclude = ( 'user', )


class AlumnoSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(AlumnoSetPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ProcesoAlumnoForm(forms.ModelForm):

    process_id = forms.IntegerField(required=False)
    alumn_id = forms.IntegerField(required=False)
    subject_id = forms.IntegerField(required=False)
    periodo_id = forms.IntegerField(required=False)

    class Meta:
        model = ProcesoAlumno
        fields = (
            'process_id',
            'alumn_id',
            'subject_id',
            'parcial',
            'periodo',
            'periodo_id',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(ProcesoAlumnoForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, *args, **kw):
        print self.cleaned_data.get('document')

        process_id = self.cleaned_data.get('process_id')
        process = Proceso.objects.get(pk=process_id)
        self.instance.process = process

        if 'Gracia' in process.name:
            self.instance.parcial = ""

        alumn_id = self.cleaned_data.get('alumn_id')
        alumn = Alumno.objects.get(pk=alumn_id)
        self.instance.alumn = alumn

        subject_id = self.cleaned_data.get('subject_id')
        subject = Materia.objects.filter(pk=subject_id).first()
        self.instance.subject = subject

        periodo_id = self.cleaned_data.get('periodo_id')
        periodo = Periodo.objects.filter(pk=periodo_id).first()
        self.instance.periodo = periodo.name

        super(ProcesoAlumnoForm, self).save(*args, **kw)
        return ProcesoAlumnoForm


class ProcesoAlumnoItemsForm(forms.ModelForm):

    process_id_2 = forms.IntegerField(required=False)

    class Meta:
        model = ProcesoAlumnoItems
        fields = (
            'process_id_2',
            'name',
            'description',
            'document',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(ProcesoAlumnoItemsForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, *args, **kw):
        process_id = self.cleaned_data.get('process_id_2')
        process = ProcesoAlumno.objects.get(pk=process_id)
        self.instance.process_alumno = process
        super(ProcesoAlumnoItemsForm, self).save(*args, **kw)
        return ProcesoAlumnoItemsForm


class ProcesoAlumnoCompleteForm(forms.ModelForm):
    
    description = forms.CharField(widget=forms.Textarea, label='Descripción')
    documento = forms.FileField(label='Documento', required=False)
    extras = forms.ModelMultipleChoiceField(required=False, queryset=Profesor.objects.all())
    input_nota_0 = forms.CharField(required=False, label='Nota')

    class Meta:
        model = ProcesoAlumno
        fields = (
            'status',
            'process',
            'alumn',
            'subject',
            'extras',
            'creation_date',
            'description',
            'documento',
            'input_nota_0',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(ProcesoAlumnoCompleteForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields['process'].widget.attrs['readonly'] = 'readonly'
            self.fields['alumn'].widget.attrs['readonly'] = 'readonly'
            self.fields['subject'].widget.attrs['readonly'] = 'readonly'
            self.fields['creation_date'].widget.attrs['readonly'] = 'readonly'

            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, *args, **kw):
        super(ProcesoAlumnoCompleteForm, self).save(*args, **kw)
        return ProcesoAlumnoCompleteForm


class HistorialForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea, label=u'Descripción')
    is_ok = forms.BooleanField(required=False)

    class Meta:
        model = Historial
        fields = (
            'description',
            'document',
            'process_alumno',
            'is_ok',
            'status',
            'created_by',
        )
        exclude =('deleted', )

    def __init__(self, *args, **kwargs):
        super(HistorialForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, *args, **kw):
        super(HistorialForm, self).save(*args, **kw)
        return HistorialForm


