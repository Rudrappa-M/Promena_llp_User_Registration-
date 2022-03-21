"""Promena URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="PROMENA LLP",
      default_version='v1',
      description="PROMENA LLP",
      terms_of_service="http://promena.in/",
      contact=openapi.Contact(email="Pradeep@promena.in"),
      #license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('Accounts/', include('Accounts.urls')),
    path('Users/',include('Users.urls')),
    # path('home/',include('home.urls'))

]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)