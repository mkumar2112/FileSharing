from rest_framework import serializers
from .models import *
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import os

User = get_user_model()
class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_clientUser', 'is_operationUser']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        # client = validated_data['is_clientUser']
        # if client == True:
        #     user.is_clientUser = True
        return user
    

class ClientUserSerializer(serializers.ModelSerializer):
    user = userSerializer()  # Include user data in the ClientUser serializer

    class Meta:
        model = ClientUser
        fields = ['user']  

class OperationUserSerializer(serializers.ModelSerializer):
    user = userSerializer()  # Include user data in the ClientUser serializer

    class Meta:
        model = OperationUser
        fields = ['user']  

class FileSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField()
    class Meta:
        model=Files
        fields = ['File']
    
    
    


