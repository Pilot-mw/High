from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True)
    form_level = models.CharField(max_length=20, blank=True, null=True)
    stream = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    parent_name = models.CharField(max_length=100, blank=True, null=True)
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.student_id} - {self.get_full_name()}"

    @property
    def role(self):
        if self.is_admin:
            return 'admin'
        elif self.is_teacher:
            return 'teacher'
        return 'student'

    def can_edit_students(self):
        return self.is_admin or self.is_teacher

    def can_edit_teachers(self):
        return self.is_admin