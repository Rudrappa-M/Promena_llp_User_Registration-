from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
from Accounts.views import *
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="PROMENA LLP",
      default_version='v1',
      description="PROMENA LLP",
      terms_of_service="http://promena.in/",
      contact=openapi.Contact(email="Pradeep@promena.in"),
      #license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
     path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     path('Register/', RegisterView.as_view({'post':'create'})),
     path('Login/', LoginAPI.as_view({'post':'create'})),

]
