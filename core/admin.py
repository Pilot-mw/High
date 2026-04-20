from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ('student_id', 'username', 'email', 'form_level', 'stream', 'is_teacher', 'is_admin', 'is_active')
    list_filter = ('form_level', 'stream', 'is_teacher', 'is_admin', 'is_active', 'is_staff')
    search_fields = ('student_id', 'username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Student Information', {'fields': ('student_id', 'form_level', 'stream', 'phone', 'address', 'date_of_birth', 'parent_name', 'parent_phone')}),
        ('Roles & Permissions', {'fields': ('is_teacher', 'is_admin')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Student Information', {'fields': ('student_id', 'form_level', 'stream')}),
    )