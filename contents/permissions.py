from rest_framework import permissions


class CanRetrieveContentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        course = obj.course

        if (
            request.method in permissions.SAFE_METHODS
            and user in course.students.all()
            or user.is_superuser
        ):
            return True
        return False
