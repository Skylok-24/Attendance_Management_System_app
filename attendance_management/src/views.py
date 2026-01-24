from django.shortcuts import render

# Create your views here.
from datetime import  date
from django.http import HttpResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User , Attendance , ClassSession
from .serializer import UserSerializer ,ClassSessionSerializer, RegisterSerializer,MyTokenObtainPairSerializer, AttendanceSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

def home(request):
    return HttpResponse("Hello from myapp 👋")

@api_view(['GET'])
def get_users(request) :
    users = User.objects.only('first_name','last_name','email','role')
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def get_students() :

@api_view(['POST'])
def register_user(request) :
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid() :
        serializer.save()
        return Response({
            'message' : 'User Created Seccessfully'
        },status=201)
    return Response(serializer.errors,status=400)

@api_view(['POST'])
def get_absents(request) :
    if not request.user.is_authenticated :
        return Response({
            'detail' : 'you must login'
        })


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_attendance(request):
    user = request.user

    if user.role != 'student':
        return Response({
            "error": "YOU ARE NOT ALLOWED"
        }, status=403)  # 403 Forbidden
    try:
        attendances = Attendance.objects.filter(student__id=user.id)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_sessions(request):
    sessions = ClassSession.objects.all().order_by('date', 'start_time')
    serializer = ClassSessionSerializer(sessions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_today_sessions(request):
    today = date.today()
    sessions = ClassSession.objects.filter(date=today).order_by('start_time')

    if not sessions.exists():
        return Response({"message": "there no sessions today"}, status=200)

    serializer = ClassSessionSerializer(sessions, many=True)
    return Response(serializer.data)