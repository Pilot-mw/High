from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/portal/', views.student_portal, name='student_portal'),
    path('student/logout/', views.student_logout, name='student_logout'),
    path('teacher/login/', views.student_login, name='teacher_login'),
    path('teacher/portal/', views.dashboard, name='teacher_portal'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/', views.settings, name='admin_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/', views.students, name='students'),
    path('teachers/', views.teachers, name='teachers'),
    path('classes/', views.classes, name='classes'),
    path('subjects/', views.subjects, name='subjects'),
    path('attendance/', views.attendance, name='attendance'),
    path('exams/', views.exams, name='exams'),
    path('fees/', views.fees, name='fees'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.dashboard, name='login'),
    path('register/', views.dashboard, name='register'),
    path('api/create-user/', views.create_user, name='create_user'),
    path('api/save-settings/', views.save_settings, name='save_settings'),
]
