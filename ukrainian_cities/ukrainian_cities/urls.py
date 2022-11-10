"""
URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from cities.views import CreateUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cities.urls')),
    
    path('auth/', include([
        path('login/', include('django.contrib.auth.urls')),
        path('signup/', CreateUserView.as_view(), name='create-user')
    ])),
]
