from Models.models import *
from rest_framework import serializers


class GetAllUserSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ('username', 'mobile_number', 'password', 'email', 'full_name')
