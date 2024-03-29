"""project URL Configuration

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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from ClassViews.views import (
    ContactView,
    NewContactView,
    EditContactView,
    ContactDelete,
    Upload,
    Export
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^Contact/$', ContactView.as_view(), name='list_contact'),
    url(r'^contact/new/$', NewContactView.as_view(), name='new_contact'),
    url(r'^contact/(?P<pk>\d+)/edit/$', EditContactView.as_view(),
        name='edit_contact'),
    url(r'^contact/(?P<pk>\d+)/delete/$', ContactDelete.as_view(),
        name='delete_contact'),
    url(r'^contacts/upload/$', Upload.as_view(), name='contact_upload'),
    url(r'^contacts/export/$', Export.as_view(), name='contact_download'),
    url(r'^', include('ClassViews.urls')),
    url(r'^accounts/login/$', auth_views.login,
        {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/Contact'}, name='logout'),
]
