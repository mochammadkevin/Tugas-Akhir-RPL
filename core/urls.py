from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import RedirectView
from django.conf import settings

urlpatterns = [
    path('', include('myFirstApp.urls')),
    path('admin/', admin.site.urls),
]
