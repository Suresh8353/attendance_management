from django.urls import path
from attendance import views


urlpatterns = [
    path('', views.college_home),
    path("attendance", views.take_attendance, name='attendance'),
    path('admission', views.student_admission, name='admission'),
]
