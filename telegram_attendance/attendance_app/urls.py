from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.attendance_table, name='attendance_table'),
]
