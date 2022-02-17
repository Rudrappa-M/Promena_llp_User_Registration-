from django.core.paginator import Paginator
from rest_framework.response import Response
from Accounts.Serializers import *
from rest_framework import viewsets, views,generics,status
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from Models.models import *
from django.contrib import auth
from .Serializers import *
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class GetAllUsersView(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = get_user_model().objects.all()
    serializer_class = GetAllUserSerializer
    token_param_config1 = openapi.Parameter(
        'page', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config2 = openapi.Parameter(
        'index', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config3 = openapi.Parameter(
        'search', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config1,token_param_config2,token_param_config3],responses={200: GetAllUserSerializer, 400: ResponseModel, 401: ResponseModel })
    def list(self,request):
        if request.user.is_authenticated:
            page = request.GET.get('page')
            index = request.GET.get('index')
            search = request.GET.get('search')
            if search is None:
                query = get_user_model().objects.all().distinct()
                paginator = Paginator(query, index)
                page_obj = paginator.get_page(page)
                serializer = GetAllUserSerializer(page_obj, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                query = get_user_model().objects.filter(Q(full_name__contains=search) | Q(email__contains=search) | Q(
                mobile_number__contains=search)).distinct()
                index = request.GET.get('index')
                paginator = Paginator(query, index)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                serializer = GetAllUserSerializer(page_obj, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            json = {"message": "UNAUTHORIZED"}
            serializer = ResponseModel(json)
            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['get']

    @swagger_auto_schema(responses={200: RegisterSerializer, 400: ResponseModel , 401: ResponseModel})
    def list(self, request):
        if request.user.is_authenticated:
            try:
                user = request.user
                userinfo = get_user_model().objects.filter(id=user.id)
                serializer = RegisterSerializer(userinfo,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                json = {"message": e}
                serializer = ResponseModel(json)
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        else:
            json = {"message": "UNAUTHORIZED"}
            serializer = ResponseModel(json)
            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)

