from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index),
    path('callback', callback),
    path('me/', me),
    path('countuser/', countuser),
    path('get_x_users/<int:x>/', get_x_users),
]
