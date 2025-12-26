from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return bool(request.user and request.user.is_staff)

class DjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map = {
            'GET': ['%(app_label)s.view_%(model_name)s'],
        }

class ViewCustomerHistoryPermission(permissions.BasePermission): 
    def has_permission(self, request, view): 
        if view.action == 'history': # check if the action is 'history'
            return request.user.has_perm('store.view_history') # check if the user has the 'view_history' permission
        return True