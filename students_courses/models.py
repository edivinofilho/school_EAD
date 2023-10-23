from django.db import models
from accounts.models import Account
from courses.models import Course
from uuid import uuid4


class StudentCourseStatus(models.TextChoices):
    DEFAULT = "pending"
    ACCEPTED = "accepted"


class StudentCourse(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    status = models.CharField(
        max_length=30,
        choices=StudentCourseStatus.choices,
        default=StudentCourseStatus.DEFAULT,
    )

    course = models.ForeignKey(
        "accounts.Account", on_delete=models.CASCADE, related_name="student_course"
    )
    student = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="student_course"
    )
