from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from uuid import uuid4


class Account(AbstractUser):
    groups = models.ManyToManyField(
            Group, 
            related_name="account_groups"
    )

    user_permissions = models.ManyToManyField(
                    Permission,
                    related_name="account_permissions"  
    )

    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    email = models.CharField(
        max_length=100,
        unique=True
    )

    my_courses = models.ManyToManyField(
        "courses.Course",
        through="students_courses.StudentCourse",
        related_name="students"
    )