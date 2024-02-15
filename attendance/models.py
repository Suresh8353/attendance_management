from django.db import models

# Create your models here.


class Students(models.Model):
    roll_number = models.IntegerField(primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=100, blank=False)
    father_name = models.CharField(max_length=100, blank=False)
    course = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    mobile = models.BigIntegerField(blank=False, null=False)
    dob = models.DateField(blank=False)
    gender = models.CharField(max_length=8, blank=False)
    address = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=50, blank=False)
    pin = models.IntegerField(blank=False, null=False)
    religion = models.CharField(max_length=50)
    image = models.ImageField(blank=True)


class PresentStudent(models.Model):
    student_name = models.CharField(max_length=100, null=False, blank=False)
    lecture = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)
    attendance = models.CharField(max_length=50, null=False, blank=False)
