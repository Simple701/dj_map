"""dj_map URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from mymap import views as map_views

urlpatterns = [
    url(r'^$|^index', map_views.index), 
    url(r'^mk_add', map_views.mk_add), 
    url(r'^mk_list', map_views.mk_list),
    url(r'^mk_del', map_views.mk_del),
    url(r'^mk_update', map_views.mk_update),
    url(r'^pt_add', map_views.pt_add), 
    url(r'^do_editor', map_views.mk_pt_get),
    url(r'^get_token', map_views.get_token),
    url(r'^get_min_url', map_views.get_min_url),
    url(r'^editor_upload', map_views.ediror_upload),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('users.urls')),
]
