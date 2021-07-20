import requests
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from config import settings


class UserActivationView(APIView):
    """
    Представление активации профиля
    """
    permission_classes = (AllowAny,)

    def get(self, request, uid, token):
        """
        Активация профиля и перенаправление на вход в профиль
        """
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/SOLO/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        requests.post(post_url, data=post_data)
        return redirect('http://' + settings.FRONT_HOST)


class PasswordResetConfirmView(APIView):
    """
    Представление смены пароля
    """
    permission_classes = (AllowAny,)

    def get(self, request, uid, token):
        """
        Получение токена и UID и перенаправление на смену пароля
        """
        return redirect('http://' + settings.FRONT_HOST + '?uid=' + uid + 'token=' + token)
