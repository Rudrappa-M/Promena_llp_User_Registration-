from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
from .views import *
from rest_framework import permissions

urlpatterns = [
    path('Profile/', ProfileView.as_view({'get':'list'})),
    path('AllUsers/', GetAllUsersView.as_view({'get':'list'})),

]