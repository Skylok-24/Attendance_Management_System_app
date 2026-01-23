from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

def home(request):
    return HttpResponse("Hello from myapp 👋")

@api_view(['GET'])
def get_users(request) :
    users = User.objects.only('first_name','last_name','email','role')
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)