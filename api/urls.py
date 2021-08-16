"""
    Version: 1.0.0
    Author: MSI Shafik
"""

from django.urls import path, include

# Put here all apps url 
urlpatterns = [
    path('users/', include('apps.user.urls')),
]
