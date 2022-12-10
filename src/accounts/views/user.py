from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from accounts.serializers import ChangePasswordSerializer, UserProfileSerializer, UserAddressSerializer
from base.helpers.decorators import exception_handler
from django.utils.decorators import method_decorator
from base.helpers.utils import entries_to_remove
User = get_user_model()
from accounts.models import UserAddress
from accounts.filters import UserAddressFilter

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_password_change(request: Request) -> Response:
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"message": "old password is not right."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }
        # delete_cache(f'{request.user.username}_token_data')
        return Response(response)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = User.objects.prefetch_related('groups', 'user_permissions').filter()
    http_method_names = ['get', 'patch']
    removable_keys = ('email')

    def get_object(self):
        return self.request.user

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        self.request.data.update(entries_to_remove(self.request.data, self.removable_keys))
        return super().patch(request, *args, **kwargs)


class UserAddressListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    filterset_class = UserAddressFilter

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super(UserAddressListCreateAPIView, self).create(request, *args, **kwargs)


class UserAddressRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    http_method_names = ['get', 'patch']
    removable_keys = ('user')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        self.request.data.update(entries_to_remove(self.request.data, self.removable_keys))
        return super().patch(request, *args, **kwargs)