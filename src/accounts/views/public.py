import json
import logging
import jwt
import requests
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from accounts.utils.token import create_tokens
from rest_framework.permissions import IsAuthenticated
from base.helpers.email import send_email
from django.conf import settings
from rest_framework.generics import CreateAPIView, GenericAPIView
from base.helpers.decorators import exception_handler
from accounts.models import User
from accounts.serializers import UserRegisterSerializer, UserSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
# from accounts.tasks.users import send_sms
from base.cache.redis_cache import delete_cache, get_cache, set_cache
from base.helpers.decorators import exception_handler
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password

# paswsword reset
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from base.helpers.email import send_email

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request) -> Response:
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        raise ValidationError(
            detail='email and password if required', code=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email__exact=email)
        if not user.check_password(raw_password=password):
            raise ValidationError(detail='invalid password',
                                  code=status.HTTP_400_BAD_REQUEST)
        access_token, refresh_token = create_tokens(user=user)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        set_cache(key=f'{email}_token_data', value=json.dumps(
            UserSerializer(user).data), ttl=5*60*60)
        print(get_cache(f'{email}_token_data'))
        return Response(data=data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        raise ValidationError(detail='user not found',
                              code=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def refreshed_token(request: Request) -> Response:
    refreshed_token = request.data.get('refresh_token')
    try:
        payload = jwt.decode(
            jwt=refreshed_token, key=settings.SECRET_KEY, algorithms='HS256', verify=True)
        if payload['token_type'] != 'refresh':
            return JsonResponse(data={
                'message': 'no refresh token provided',
                'success': False
            }, status=400)
        user_name = payload.get('username')
        user_obj = get_object_or_404(User, username=user_name)
        if get_cache(f'{user_obj.username}_token_data'):
            raise ValidationError(
                detail='Already have a valid token', code=status.HTTP_401_UNAUTHORIZED)
        if not user_obj.is_active:
            raise ValidationError(
                detail='user is not active', code=status.HTTP_401_UNAUTHORIZED)
        access_token, refresh_token = create_tokens(user=user_obj)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
    except Exception as err:
        return JsonResponse(data={
            'message': f'{str(err)}',
            'success': False,
        }, status=401)

class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['is_active'] = True
        request.data['username'] = request.data['email']
        request.data['password'] = make_password(request.data['password'])
        return super(UserRegisterView, self).create(request, *args, **kwargs)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def logout(request: Request) -> Response:
    if not request.user:
        raise ValidationError(detail='user not found',
                              code=status.HTTP_404_NOT_FOUND)
    delete_cache(f'{request.user.email}_token_data')
    return Response(data={'message': 'user has been logged out'}, status=status.HTTP_200_OK)



# password reset
class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'accounts:public:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            send_email( '5boysbd@gmail.com' ,'Reset your passsword', absurl)
            return Response({'message': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response({'message': 'this email have not any user'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, 'message': "token is valid"}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)




""" *** Social Auth (Google)*** """
@api_view(['POST'])
@permission_classes([AllowAny])
@exception_handler
def get_user_data_from_google(request):

    GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

    access_token = request.data.get("access_token")
    r = requests.post(
        GOOGLE_ID_TOKEN_INFO_URL,
        data={ "access_token": access_token,}

    )
    if not r.ok:
        raise ValidationError('id_token is invalid.')
    google_response = r.json()
    email = google_response.get('email')
    first_name = google_response.get('given_name')
    last_name = google_response.get('family_name')
    try:
        user = User.objects.filter(email = email)[0]
    except:
        try:
            user = User.objects.get(username = email)
        except:
            user = User.objects.create (username = email, email = email, first_name = first_name ,last_name = last_name )

    access_token, refresh_token = create_tokens(user=user)
    data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
    set_cache(key=f'{user.email}_token_data', value=json.dumps(UserSerializer(user).data), ttl=5*60*60)
    return Response(data=data, status=status.HTTP_201_CREATED)


""" *** Social Auth (Facebook)*** """
@api_view(['POST'])
@permission_classes([AllowAny])
@exception_handler
def get_user_data_from_facebook(request):

    FACEBOOK_ID_TOKEN_INFO_URL = 'https://graph.facebook.com/me'

    access_token = request.data.get("access_token")
    r = requests.post(
        FACEBOOK_ID_TOKEN_INFO_URL,
        data={ "access_token": access_token,
        'fields': 'email,first_name,last_name'}

    )
    if not r.ok:
        raise ValidationError('id_token is invalid.')
    fb_response = r.json()
    id = fb_response.get('id')
    username = 'fb'+id
    email = fb_response.get('email')
    first_name = fb_response.get('first_name')
    last_name = fb_response.get('last_name')
    try:
        user = User.objects.get(username = username)
    except:
        if email:
            user = User.objects.create (username=username, email=email, first_name=first_name ,last_name=last_name )
        else:
            user = User.objects.create (username=username, first_name=first_name ,last_name=last_name )

    access_token, refresh_token = create_tokens(user=user)
    data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
    set_cache(key=f'{user.username}_token_data', value=json.dumps(UserSerializer(user).data), ttl=5*60*60)
    return Response(data=data, status=status.HTTP_201_CREATED)