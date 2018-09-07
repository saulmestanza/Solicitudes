# -*- coding: utf-8 -*-
"""SeguimientoUCSG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include, handler404, handler500
from django.conf.urls.static import static
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext as _

class HomeView(TemplateView): 
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['tittle'] = _(u"Seguimiento UCSG")
        if self.request.user.is_authenticated():
            context['motto'] = _(u"Bienvenido al sistema de Seguimiento UCSG")
            context['alert_message'] = {'class': 'success',
            'mod': u'',
            'message': _(u'Inicio de sesión exitoso.')}
        else:            
            context['motto'] = _(u"Bienvenido al sistema de Seguimiento UCSG")
            context['alert_message'] = {'class': 'warning',
            'mod': _(u'Atención:'),
            'message': _(u'Este es un sitio de acceso restringido.')}
        return context

def error_404(request):
        data = {}
        return render(request,'404.html', data)

def error_500(request):
        data = {}
        return render(request,'500.html', data)

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name="base"),
    url(r'^administrador/', include('administrador.urls')),
    url(r'^profesor/', include('profesor.urls')),
    url(r'^alumno/', include('alumno.urls')),
    url(r'^reporteria/', include('reporteria.urls')),
    url(r'^api/', include('webservices.urls')),
    url(r'^captcha/', include('captcha.urls')),
]

handler404 = error_404
handler500 = error_500
