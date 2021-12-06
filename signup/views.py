from django import db
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
import hashlib
import binascii
import os
import random
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from info.models import *
from nearme_backend import settings
# Create your views here.


class RegistrationView(generics.CreateAPIView):
    """ Register new user """

    def post(self, request, **kwargs):
        # jwt token validation
        name = request.data.get('name')
        contact = request.data.get('contact')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        try:
            user = Registration.objects.get(email=email)
            user_serializer = RegistrationSerializer(user, many=False)
            data = user_serializer.data
            if data['email'] is not None:
                dict = {
                    "msg": "Email Already Exist"
                }
                return Response(dict)
        except:
            if (password != confirm_password):
                dict = {
                    "msg": "Wrong Password"
                }
                return Response(dict)

            salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
            pwdhash = hashlib.pbkdf2_hmac(
                'sha512', password.encode('utf-8'), salt, 100000)
            pwdhash = binascii.hexlify(pwdhash)
            password = (salt + pwdhash).decode('ascii')

            user_dict = {
                'name': name,
                'contact': contact,
                'email': email,
                'password': password,
                'confirm_password': password,
            }

            serializer = RegistrationSerializer(data=user_dict)
            if serializer.is_valid():
                serializer.save()
                dict = {
                    "msg": "User Registered Successfully"
                }
            else:
                print(serializer.errors)
                dict = {
                    "msg": "Error"
                }
            return Response(dict)


class LoginView(generics.CreateAPIView):

    def post(self, request, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        dic = {
            "msg": "Wrong Password"
        }
        try:
            data = Registration.objects.get(email=email)
            newmail = email.split('@')
            print(newmail[0])
            settings.username = newmail[0]
            print(settings.username)
            salt = data.password[:64]
            data.password = data.password[64:]
            pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode(
                'utf-8'), salt.encode('ascii'), 100000)
            pwdhash = binascii.hexlify(pwdhash).decode('ascii')

            if(pwdhash == data.password):
                # owner_datas = list(
                #     OwnerInfo.objects.filter(owner_email=email).values_list(
                #         'owner_shop', flat=True
                #     )
                # )
                # shop_datas = list(
                #     ShopInfo.objects.filter(shop_id=owner_datas[0]).values_list(
                #         'shop_name', 'shop_contact', 'shop_type'
                #     )
                # )
                # profile_datas = list(
                #     Registration.objects.filter(email=email).values_list(
                #         'name', 'contact', 'email'
                #     )
                # )
                logObj = LogIn.objects.filter(login_name="New Login")
                logObj.update(isLoggedIn=True)
                dic = {
                    "msg": "Login Successfull",
                    "name": settings.username,
                    # "owner": owner_datas,
                    # "shop": shop_datas,
                    # "profile": profile_datas
                }
        except:
            dic = {
                "msg": "Login Unsuccessfull"
            }
        return Response(dic)


class IsLoggedInView(generics.CreateAPIView):

    def get(self, request, **kwargs):
        logObj = LogIn.objects.get(login_name="New Login")
        dic = {
            "msg": logObj.isLoggedIn,
            "name": settings.username
        }
        return Response(dic)


class LogOutView(generics.CreateAPIView):

    def get(self, request, **kwargs):
        logObj = LogIn.objects.filter(login_name="New Login")
        logObj.update(isLoggedIn=False)
        logObjs = LogIn.objects.get(login_name="New Login")
        dic = {
            "msg": logObjs.isLoggedIn
        }
        return Response(dic)
