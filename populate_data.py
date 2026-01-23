import os
import django
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

# --- جزء الإعداد المهم جداً ---
# هذا الجزء يربط السكربت بإعدادات جانغو
# تأكد أن 'attendance_management.settings' هو المسار الصحيح لملف settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_management.settings')
django.setup()

# --- الاستدعاءات تأتي بعد الإعداد ---
from attendance_management.src.models import User, Teacher, Student, Module, ClassSession, Attendance, AbsenceJus


def create_english_data():
    print("Starting data generation...")

    # 1. Create Admin User
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@school.com',
            password='password123',
            first_name='Super',
            last_name='Admin',
            role='admin'
        )
        print(f"Admin created: {admin}")

    # 2. Create Teachers
    teacher1 = Teacher(
        username='t_smith',
        email='smith@school.com',
        first_name='John',
        last_name='Smith',
        role='teacher',
        department='Computer Science'
    )
    teacher1.set_password('password123')
    teacher1.save()

    teacher2 = Teacher(
        username='t_emily',
        email='emily@school.com',
        first_name='Emily',
        last_name='Johnson',
        role='teacher',
        department='Mathematics'
    )
    teacher2.set_password('password123')
    teacher2.save()
    print("Teachers created.")

    # 3. Create Students
    student1 = Student(
        username='s_david',
        email='david@school.com',
        first_name='David',
        last_name='Brown',
        role='student',
        academic_year='Senior Year'
    )
    student1.set_password('password123')
    student1.save()

    student2 = Student(
        username='s_sarah',
        email='sarah@school.com',
        first_name='Sarah',
        last_name='Connor',
        role='student',
        academic_year='Junior Year'
    )
    student2.set_password('password123')
    student2.save()
    print("Students created.")

    # 4. Create Modules
    mod_db = Module.objects.create(name='Database Systems')
    mod_db.teachers.add(teacher1)

    mod_math = Module.objects.create(name='Linear Algebra')
    mod_math.teachers.add(teacher2)
    print("Modules created.")

    # 5. Create Sessions
    session1 = ClassSession.objects.create(
        room='Lab A',
        date=datetime.date.today(),
        start_time=datetime.time(9, 0),
        end_time=datetime.time(11, 0),
        module=mod_db
    )

    session2 = ClassSession.objects.create(
        room='Hall 101',
        date=datetime.date.today(),
        start_time=datetime.time(13, 0),
        end_time=datetime.time(15, 0),
        module=mod_math
    )
    print("Sessions created.")

    # 6. Create Attendance
    att_present = Attendance.objects.create(
        status='present',
        student=student1,
        session=session1
    )

    att_absent = Attendance.objects.create(
        status='absent',
        student=student2,
        session=session1
    )
    print("Attendance recorded.")

    # 7. Create Absence Justification
    dummy_file = SimpleUploadedFile("medical_report.txt", b"Student was ill.")

    jus1 = AbsenceJus.objects.create(
        reason='Sudden Sickness',
        file=dummy_file,
        status='accept',
        attendance=att_absent
    )
    print("Justification created.")
    print("--- Data Generation Completed Successfully! ---")


if __name__ == '__main__':
    create_english_data()