from rest_framework import serializers
from .models import Module ,User, Student , Attendance , ClassSession
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ModuleSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Module
        fields = ['id','name']

class StudentSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Student
        fields = ['academic_year']

class UserSerializer(serializers.ModelSerializer) :
    student = StudentSerializer(read_only=True)
    class Meta :
        model = User
        fields = ['first_name','last_name','email','role','student']

class RegisterSerializer(serializers.ModelSerializer) :
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta :
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']

    def validate_email(self, value):
        if not value.endswith('@univ-geulma.dz'):
            raise serializers.ValidationError("only @univ-guelma.dz is valide")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password'] :
            raise serializers.ValidationError({"password","password dont match"})
        return data

    def create(self,validated_data):
        validated_data.pop('confirm_password')
        student = Student.objects.create_user(
            **validated_data,
            role='student',
            academic_year=2026
        )
        return student

class AttendanceSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Attendance
        fields = ['id','status','submit_date','session']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        data['email'] = self.user.email
        data['role'] = self.user.role
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name

        if self.user.role == 'student':
            try:
                from .models import Student
                student = Student.objects.get(id=self.user.id)
                data['academic_year'] = student.academic_year
            except:
                data['academic_year'] = None

        return data

class ClassSessionSerializer(serializers.ModelSerializer):
    module_details = ModuleSerializer(source='module', read_only=True)

    class Meta:
        model = ClassSession
        fields = ['id', 'room', 'date', 'start_time', 'end_time', 'module_details']


class TeacherModuleSerializer(serializers.ModelSerializer):
    sessions_count = serializers.IntegerField(source='classsession_set.count', read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'name', 'sessions_count']


class TeacherSessionSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source='module.name', read_only=True)

    class Meta:
        model = ClassSession
        fields = ['id', 'room', 'date', 'start_time', 'end_time', 'module_name']