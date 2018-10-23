"""familia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url( r'^login/$',auth_views.LoginView.as_view(template_name="home.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="useraccounts/logout.html"), name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^signup/$', core_views.signup, name='signup'),
    path('admin/', admin.site.urls),
    path('core/',include('core.urls')),
]
