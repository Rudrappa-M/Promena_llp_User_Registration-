from turtle import update
from rest_framework.response import Response
from rest_framework import viewsets, views,generics,status
from django.contrib.auth import get_user_model
from Models.models import *
from django.contrib import auth
from .Serializers import *
from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import datetime
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
import random
# Create your views here.


class RegisterView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['post']

    @swagger_auto_schema(responses={201: OtpSerializer, 400: ResponseModel, 409: ResponseModel})
    def create(self,request):
        data = request.data
        mobile_number = data['mobile_number']
        check = get_user_model().objects.filter(mobile_number=mobile_number).exists()
        if check is False:
            try:
                users = get_user_model().objects.create_user(mobile_number=data['mobile_number'],email=data['email'],password=data['password'],full_name=data['full_name'],username=data['username'])
                users.save()
                otp = random.randint(1000, 9999)
                user = get_user_model().objects.get(mobile_number=data['mobile_number'])
                userid = user.id
                authuser = AuthUser.objects.create(user=users, otp=otp , otp_expiry=datetime.datetime.now() + datetime.timedelta(minutes=10))
                json = {"otp": otp}
                serializer = OtpSerializer(json)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as v:
                json = {"message": v}
                serializer = ResponseModel(json)
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                json = {"message": e}
                serializer = ResponseModel(json)
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            json = {"message": "User already exists"}
            serializer = ResponseModel(json)
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)


class LoginAPIView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    http_method_names = ['post']
    queryset = get_user_model().objects.all()

    @swagger_auto_schema(responses={200: LoginResponse, 404: ResponseModel, 400: ResponseModel})
    def create(self,request):
        data = request.data
        mobile_number = data['mobile_number']
        password = data['password']
        check = get_user_model().objects.filter(mobile_number=mobile_number).exists()

        if check is True:
            try:
                user = auth.authenticate(mobile_number=mobile_number, password=password)

                if user:
                    data = {"token": user.tokens()['access'],"mobile_number": user.mobile_number}
                    serializer = LoginResponse(data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    json = {"message": "Incorrect password ,password does not match"}
                    serializer = ResponseModel(json)
                    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                json = {"message": e}
                serializer = ResponseModel(json)
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            json = {"message": "User does not  exists"}
            serializer = ResponseModel(json)
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


class ResendOtpView(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = get_user_model().objects.all()
    serializer_class = OtpResendSerializer

    @swagger_auto_schema(responses={200: OtpSerializer, 404: ResponseModel})
    def create(self,request):
        data = request.data
        mobile_number = data['mobile_number']
        check =get_user_model().objects.filter(mobile_number=mobile_number).exists()
        if check is True:
            otp = random.randint(1000,9999)
            user = get_user_model().objects.get(mobile_number=mobile_number)
            qs = AuthUser.objects.filter(user=user.id).update(otp=otp,otp_expiry=datetime.datetime.now() + datetime.timedelta(minutes=10))
            json = {'otp': otp}
            serializer = OtpSerializer(json)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            json = {"message": "User does not  exists"}
            serializer = ResponseModel(json)
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


class OtpValidateView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = OtpValidateSerializer
    http_method_names = ['post',]

    @swagger_auto_schema(responses={200: ResponseModel, 400: ResponseModel, 404: ResponseModel})
    def create(self,request):
        data = request.data
        mobile_number = data['mobile_number']
        rotp = data['otp']
        check = get_user_model().objects.filter(mobile_number=mobile_number).exists()
        if check is True:
            qss = get_user_model().objects.get(mobile_number=mobile_number)
            qs = list(AuthUser.objects.filter(user=qss).values())
            print(qs)
            exptime = ''
            for x in qs:
                sotp = x['otp']
                exptime = x['otp_expiry']

            now = datetime.datetime.now().time()
            expriytime = exptime.time()

            if now < expriytime:
                if sotp == rotp :
                    validated = AuthUser.objects.filter(user=qss).update(is_otpvalidated=True)
                    json = {'message': "Successfully Verified"}
                    serializer = ResponseModel(json)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    json = {'message': "wrong otp"}
                    serializer = ResponseModel(json)
                    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                json = {'message': "otp expired"}
                serializer = ResponseModel(json)
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            json = {'message': "User does not Exists"}
            serializer = ResponseModel(json)
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


class ForgotPasswordView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ForgotPasswordSerilaizer
    http_method_names = ['post',]

    @swagger_auto_schema(responses={200: ResponseModel, 404: ResponseModel})
    def create(self,request):
        data = request.data
        check =get_user_model().objects.filter(mobile_number=data['mobile_number']).exists()
        if check == True:
            qs = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
            email = ''
            for x in qs:
                email = x['email']
            user = get_user_model().objects.get(mobile_number=data['mobile_number'])
            token = PasswordResetTokenGenerator().make_token(user)
            update = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(email_token=token,otp_expiry=datetime.datetime.now() + datetime.timedelta(minutes = 10))
            absurl = 'http://dfo.hktech.in/password-reset.html?Mg=' + token
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            data = {'email_body': email_body, 'to_email': email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            json = {'message': "Successfully Sent "}
            serializer = ResponseModel(json)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            json = {'message': "User does not Exists"}
            serializer = ResponseModel(json)
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

# class PasswordReset(viewsets.ModelViewSet):
#     serializer_class = PasswordResetSerializer
#     queryset = get_user_model().objects.all()
#     http_method_names = ['post', ]

#     @swagger_auto_schema(responses={200: ResponseModel, 400: ResponseModel, 404: ResponseModel })
#     def create(self,request):
#         token = request.GET.get('token')
#         password = request.GET.get('password')
#         users = list(get_user_model().objects.filter(email_token=token).values())
#         uid = ''
#         exptime = ''
#         for u in users:
#             uid = u['id']
#         for u in users:
#             exptime = u['otp_expiry']

#         nw = datetime.datetime.now().time()
#         expirytime = exptime.time()
#         if nw < expirytime:
#             try:
#                 user = get_user_model().objects.get(id=uid)
#                 user.set_password(password)
#                 user.save()
#                 json = {'message': "Successfully Sent "}
#                 serializer = ResponseModel(json)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Exception as e:
#                 json = {"message": e}
#                 serializer = ResponseModel(json)
#                 return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             json = {'message': "Token Expired"}
#             serializer = ResponseModel(json)
#             return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

from rest_framework.exceptions import AuthenticationFailed
from drf_yasg import openapi
class Password_reset(views.APIView):
    serializer_class = PasswordResetSerializer
    token_param_config1 = openapi.Parameter(
        'password', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    token_param_config2 = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config1,token_param_config2])
    def post(self,request):
        token = request.GET.get('token')
        password = request.GET.get('password')
        users = list(get_user_model().objects.filter(email_token=token).values())
        uid = ''
        exptime = ''
        for u in users:
            uid = u['id']
        for u in users:
            exptime = u['otp_expiry']

        nw = datetime.datetime.now().time()
        expriytime = exptime.time()
        if nw < expriytime:
            try:
                user = get_user_model().objects.get(id=uid)
                user.set_password(password)
                user.save()
                datas = [password,token]
                mydata = {'data':'Password change success','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            except Exception as e:
                raise AuthenticationFailed({'data':'User Not Found','status':status.HTTP_404_NOT_FOUND,'detail': 'Failure , Login Falied'})
        else:
                mydata = {'data':'wrong token','code':status.HTTP_400_BAD_REQUEST,'detail':'wrong otp'}
                return Response(mydata)