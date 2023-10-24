from django.http import Http404
from django.shortcuts import render
from .models import Content
from courses.models import Course
from .serializers import ContentSerializer
from accounts.permissions import IsAdminUser, IsAdminOrOwner
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .permissions import CanRetrieveContentPermission


class ContentView(generics.CreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = "course_id"
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs["course_id"])
        serializer.save(course=course)


class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = "content_id"
    permission_classes = [
        permissions.IsAuthenticated,
        CanRetrieveContentPermission,
    ]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        content_id = self.kwargs[self.lookup_url_kwarg]
        course_id = self.kwargs["course_id"]

        try:
            obj = get_object_or_404(queryset, id=content_id, course_id=course_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Http404:
            try:
                get_object_or_404(Course, id=course_id)
            except Http404:
                raise Http404("course not found.")
            raise Http404("content not found.")

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404 as e:
            error_message = str(e)
            return Response({"detail": error_message}, status=status.HTTP_404_NOT_FOUND)
