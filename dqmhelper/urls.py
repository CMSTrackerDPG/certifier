"""dqmhelper URL Configuration

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

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("home.urls")),
    path("trackermaps/", include('trackermaps.urls')),
    path("openruns/", include('openruns.urls')),
    path("summary/", include('summary.urls')),
    path("delete/", include('delete.urls')),
    path("restore/", include('restore.urls')),
    path("shiftleader/", include('shiftleader.urls')),
    path("list/", include("listruns.urls")),
    path("certify/", include("certifier.urls")),
    path("plot/", include("plot.urls")),
    path("accounts/", include('allauth.urls')),
    path("users/", include('users.urls')),
    path("reference/", include('addrefrun.urls')),
    path("admin/", admin.site.urls),
    path("mldatasets/", include('mldatasets.urls')),
    path("mlplayground/", include('mlplayground.urls', namespace = 'mlplayground')),
    path("cablingmap/", include('cablingmap.urls')),
]
