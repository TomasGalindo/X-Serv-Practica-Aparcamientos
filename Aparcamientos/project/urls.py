"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from final7 import views
from django.contrib.auth.views import logout
from django.views.static import serve
from project import settings

urlpatterns = [
    url(r'static/(?P<path>.*)$', serve,
        {'document_root': settings.URL_PRINCIPAL}),
    url(r'css/(.*)$', views.css, name="cargar css"),
    url(r'^aparcamientos/(\d+)$', views.pagAparca,
        name="Pagina del aparcamiento"),
    url(r'^aparcamientos/$', views.todosAparca,
        name="listado con todos los aparcamientos"),
    url(r'^about/$', views.about, name="Info sobre Funcionamiento"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register', views.register, name="crear usuario"),
    url(r'^logout', logout, {'next_page': '/'}),
    url(r'^login', views.milogin),
    url(r'^$', views.pagPrincipal, name="prueba pagina principal"),
    url(r'^(.*)/XML$', views.xml, name="XML de la pagina de usuario"),
    url(r'^(.*)$', views.pag_usu, name="pagina de usuario"),

]
