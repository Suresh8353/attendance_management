from django.contrib import admin
from .models import Students
# Register your models here.


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'father_name', 'email', 'course', 'mobile', 'dob', 'gender',
                    'address', 'city', 'state', 'pin', 'religion']
