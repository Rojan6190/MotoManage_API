# core/permissions.py  (or users/permissions.py — your choice, just import consistently)

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Allows access only to users whose role == 'admin'.
    Used by the React admin dashboard.
    """
    message = "You do not have admin privileges."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission.
    - Admin can do anything.
    - Regular user can only access their own object.

    The view must call  get_object()  for this to fire.
    For list views use a queryset filter instead.
    """
    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.role == "admin":
            return True

        # Works for User objects and for Vehicle objects (via obj.owner)
        owner = getattr(obj, "owner", obj)   # Vehicle → owner field; User → obj itself
        return owner == request.user


class IsSelfOrAdmin(BasePermission):
    """
    For profile endpoints:  GET/PATCH /api/mobile/profile/
    Users can only read/update themselves; admins can do anything.
    This is a view-level check (not object-level) because the view
    always scopes to request.user anyway.
    """
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated