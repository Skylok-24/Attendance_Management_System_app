from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

class Teacher(User) :
    department = models.CharField(max_length=100)

class Student(User) :
    academic_year = models.CharField(max_length=100)
    
class Module(models.Model) :
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher)

class ClassSession(models.Model) :
    room = models.CharField(max_length=30)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    module = models.ForeignKey(Module,on_delete=models.SET_NULL,null=True)

class Attendance(models.Model) :
    STATES = (
    ('present','Present'),
    ('absent','Absent')
    )
    status = models.CharField(
        max_length=10,
        choices=STATES,
        null=True
    )
    submit_date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student,null=True,on_delete=models.SET_NULL)
    session = models.ForeignKey(ClassSession,null=True,on_delete=models.SET_NULL)

class AbsenceJus(models.Model) :
    STATES = (
    ('accept','Accept'),
    ('refuse','Refuse')
    )
    reason = models.TextField()
    file = models.FileField(upload_to='justifications')
    submit_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATES,
        null=True
    )
    attendance = models.OneToOneField(Attendance,on_delete=models.CASCADE)

