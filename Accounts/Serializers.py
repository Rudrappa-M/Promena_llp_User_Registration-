from dataclasses import fields
from rest_framework import serializers
from Models.models import *

# Create your Serializers here.
class OtpSerializer(serializers.ModelSerializer):

    class Meta():
        model = AuthUser
        fields = ('otp',)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('username', 'mobile_number', 'password', 'email', 'full_name')


class ResponseModel(serializers.Serializer):
    message = serializers.CharField(max_length=200)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        exclude = ('password',)


class LoginSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ('mobile_number','password')


class LoginResponse(serializers.Serializer):
    mobile_number = serializers.IntegerField()
    token = serializers.CharField(max_length=300)


class OtpResendSerializer(serializers.Serializer):
    mobile_number = serializers.IntegerField()


class OtpValidateSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField()
    class Meta():
        model = User
        fields = ('mobile_number','otp')


class ForgotPasswordSerilaizer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number',)

class PasswordResetSerializer(serializers.Serializer):
    # mobile_number = serializers.IntegerField()
    # token = serializers.CharField(max_length=500)
    # password=serializers.CharField(max_length=500)
    class Meta():
        model=User
        fields=('id','mobile_number')