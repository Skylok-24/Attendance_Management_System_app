from rest_framework import serializers
from .models import Module ,User

class ModuleSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Module
        fields = ['name']

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields = ['first_name','last_name','email','role']