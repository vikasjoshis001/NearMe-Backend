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

            settings.user_dict = {
                'name': name,
                'contact': contact,
                'email': email,
                'password': password,
                'confirm_password': password,
            }

            serializer = RegistrationSerializer(data=settings.user_dict)
            if serializer.is_valid():
                serializer.save()
                dict = {
                    "msg": "User Registered Successfully"
                }
                # settings.otp = random.randint(100000, 999999)
                # print(settings.otp)
                # msg = "Your One Time Password for GateMaster Registeration\n\nverification code : " + \
                #     str(settings.otp)
                # try:
                #     send_mail(
                #         'GateMaster Registeration',
                #         msg,
                #         'crunchbase.io@gmail.com',
                #         [email],
                #         fail_silently=False,
                #     )
                # except:
                #     print("Sorry! Mail not sent...")

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
            print(data)
            settings.username = data.name
            salt = data.password[:64]
            data.password = data.password[64:]
            pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode(
                'utf-8'), salt.encode('ascii'), 100000)
            pwdhash = binascii.hexlify(pwdhash).decode('ascii')

            if(pwdhash == data.password):
                dic = {
                    "msg": "Login Successfull",
                    "name": settings.username
                }
        except:
            dic = {
                "msg": "Login Unsuccessfull"
            }
        return Response(dic)
