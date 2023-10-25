from .models import Course
from students_courses.models import StudentCourse
from accounts.models import Account
from students_courses.serializers import StudentCourseSerializer
from .serializers import AddStudentCourse, CourseSerializer, CreateCourse
from accounts.permissions import IsAdminOrReadOnly, IsAdminOrOwner, IsAdminUser
from rest_framework import generics
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class CourseView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CreateCourse
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Course.objects.filter(students=self.request.user)
        return self.queryset.all()


class CourseDetailVIew(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = "course_id"
    permission_classes = [IsAdminOrOwner]


class StudentCourseView(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = AddStudentCourse
    lookup_url_kwarg = "course_id"
    permission_classes = [IsAdminUser]
