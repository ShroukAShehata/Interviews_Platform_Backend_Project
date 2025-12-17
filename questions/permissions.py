# core/permissions.py
from rest_framework.permissions import BasePermission


class IsExpertUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "expert")
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "admin")
    

class IsOwner(BasePermission):
    """
    Allow editing only if user is owner of question/answer
    """

    def has_object_permission(self, request, view, obj):
        # obj could be Question or Answer instance
        return obj.created_by == request.user or obj.author == request.user

