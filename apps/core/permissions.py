from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    """
    Allows access only to users with the ADMIN role or superusers.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_superuser or 
                getattr(request.user, 'role', '') == 'ADMIN'
            )
        )

class IsTeacherRole(permissions.BasePermission):
    """
    Allows access only to users with the TEACHER role.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                getattr(request.user, 'role', '') == 'TEACHER'
            )
        )

class IsStudentRole(permissions.BasePermission):
    """
    Allows access only to users with the STUDENT role.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                getattr(request.user, 'role', '') == 'STUDENT'
            )
        )

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Allows access to TEACHER or ADMIN roles.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_superuser or 
                getattr(request.user, 'role', '') in ('ADMIN', 'TEACHER')
            )
        )
