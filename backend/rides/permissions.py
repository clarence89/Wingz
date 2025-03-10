from rest_framework.permissions import BasePermission


# Can be done using Manager to all Models. which will return None or empty list. when role is not admin. But i Just place it here for now
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user and request.user.role and request.user.role.name == "admin"
        return False
