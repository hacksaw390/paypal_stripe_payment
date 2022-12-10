from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CharField
from base.serializers import DynamicFieldsModelSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed
User = get_user_model()
from accounts.models import UserAddress

class UserRegisterSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email','phone_number','password', 'is_active', 'profile_pic_url')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class AdminUserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email','phone_number',"password", 'is_active','role','is_staff','profile_pic_url')
        extra_kwargs = {
            'password': {'write_only': True}
        }
class AdminCustomerSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email','phone_number','password', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email','phone_number', 'is_active','role')
        
class AdminProfileSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email','phone_number','role','is_active','is_staff','is_superuser','profile_pic_url')

class UserProfileSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email','phone_number','is_active','profile_pic_url')

class UserAddressSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)



# Reset password
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)
    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


# use for read write serializer
class UserLiteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email','phone_number')