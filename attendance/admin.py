from django.contrib import admin
from .models import Students, PresentStudent
# Register your models here.


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'father_name', 'email', 'course', 'mobile', 'dob', 'gender',
                    'address', 'city', 'state', 'pin', 'religion']


@admin.register(PresentStudent)
class PresentStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_name', 'lecture', 'date', 'attendance']
