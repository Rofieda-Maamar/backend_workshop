from rest_framework import serializers 
from .models import Mood

from django.contrib.auth.models import User 


class MoodsSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = Mood 
        fields = "__all__"




class UserRegesterSerializer(serializers.ModelSerializer) : 
    password = serializers.CharField(write_only = True)
    class Meta : 
        model = User 
        fields = ['id' , 'username' , 'email' , 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'] ,
            email = validated_data['email'] ,
            password=validated_data['password']

        )
        return user

