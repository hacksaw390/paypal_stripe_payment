from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.filters import UserFilter
from base.helpers.decorators import exception_handler
from base.permissions import IsStaff, IsSuperUser
from accounts.serializers import AdminUserSerializer, AdminProfileSerializer, AdminCustomerSerializer
from base.helpers.utils import entries_to_remove
from base.user_role_permissions import permission_data
User = get_user_model()
from django.contrib.auth.models import  Permission
from base.permissions import HasRequiredPermissionForMethod
from rest_framework.response import Response

class AdminProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdminProfileSerializer
    queryset = User.objects.prefetch_related('groups', 'user_permissions').filter()
    http_method_names = ['get', 'patch']
    removable_keys = ('role','email', 'username','is_active','is_staff','is_superuser')

    def get_object(self):
        return self.request.user
        
    def get(self, request):
        profile = self.get_object()
        serializer = self.serializer_class(profile)
        response = serializer.data
        user_permissions_list = list(Permission.objects.filter(user__username=self.request.user.username).values_list('codename', flat=True))
        response["permissions"] = user_permissions_list        
        return Response(response)

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        self.request.data.update(entries_to_remove(self.request.data, self.removable_keys))
        return super().patch(request, *args, **kwargs)

    
class AdminUserListCreateApiView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['accounts.view_user']
    post_permission_required = ['accounts.add_user']
    serializer_class = AdminUserSerializer
    queryset = User.objects.filter(is_staff=True)
    search_fields = ['email','username']
    filterset_class = UserFilter

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        user_role = request.data.get('role')
        request.data['is_active'] = True
        request.data['is_staff'] = True
        request.data['username'] = request.data['email']
        request.data['password'] = make_password(request.data['password'])
        response = super(AdminUserListCreateApiView, self).create(request, *args, **kwargs)
        user_id = response.data.get("id")
        user = User.objects.get(id=user_id)
        permission = Permission.objects.filter(codename__in = permission_data.get(user_role))
        user.user_permissions.add(*permission)
        return response
    
class AdminUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['accounts.view_user']
    patch_permission_required = ['accounts.change_user']
    serializer_class = AdminUserSerializer
    queryset = User.objects.filter(is_staff=True)
    http_method_names = ['patch', 'get']
    removable_keys = ('password','email','username','is_staff')

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        self.request.data.update(entries_to_remove(self.request.data, self.removable_keys))
        user_role = request.data.get('role')
        user = self.get_object()
        user.user_permissions.clear()
        permission = Permission.objects.filter(codename__in = permission_data.get(user_role))
        user.user_permissions.add(*permission)
        return super(AdminUserRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)


class AdminCustomerLisApiView(ListAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['accounts.view_user']
    serializer_class = AdminCustomerSerializer
    queryset = User.objects.filter(is_staff=False)
    search_fields = ['email','username']
    filterset_class = UserFilter


class AdminCustomerRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['accounts.view_user']
    serializer_class = AdminCustomerSerializer
    queryset = User.objects.filter(is_staff=False)
