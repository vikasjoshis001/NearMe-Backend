from django.shortcuts import render
import random
from datetime import datetime, timedelta
import base64
import pandas as pd
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from .models import *
from .serializers import *


class ShopInfoView(generics.CreateAPIView):
    """ To add a shops """

    def post(self, request):
        try:
            shop_name = request.data.get('shop_name')
            shop_contact = request.data.get('shop_contact')
            shop_email = request.data.get('shop_email')
            shop_address = request.data.get('shop_address')
            shop_type = request.data.get('shop_type')
            shop_description = request.data.get('shop_description')
            shop_image = request.FILES.get("shop_image")
            owner_name = request.data.get('owner_name')
            owner_contact = request.data.get('owner_contact')
            owner_email = request.data.get('owner_email')
            owner_address = request.data.get('owner_address')

            shop_data = {
                "shop_name": shop_name,
                "shop_contact": shop_contact,
                "shop_email": shop_email,
                "shop_address": shop_address,
                "shop_type": shop_type,
                "shop_image": shop_image,
                "shop_description": shop_description
            }

            ShopSerializer = ShopInfoSerializer(data=shop_data)
            if ShopSerializer.is_valid(raise_exception=True):
                ShopSerializer.save()
                shop_id = ShopInfo.objects.latest('shop_id')
                print(shop_id)
                shop_data = {
                    "owner_shop": shop_id,
                    "owner_name": owner_name,
                    "owner_contact": owner_contact,
                    "owner_email": owner_email,
                    "owner_address": owner_address,
                }
                OwnerSerializer = OwnerInfoSerializer(data=shop_data)
                if OwnerSerializer.is_valid(raise_exception=True):
                    OwnerSerializer.save()
                dic = {
                    "Type": "Success",
                    "Message": "Shop added successfully",
                    "data": ShopSerializer.data
                }

            else:
                dic = {
                    "Type": "Error",
                    "Message": "Shop added unsuccessfully",
                    "data": ""
                }

            return Response(data=dic, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            print(e)
            dic = {
                "Type": "Error",
                "Message": "Shop added unsuccessfully",
                "data": e.detail
            }
            return Response(data=dic, status=status.HTTP_201_CREATED)


class GetList(generics.ListAPIView):
    def get(self, request, **kwargs):
        type = request.query_params['type']
        shop_lists = []
        shop_lists = ShopInfo.objects.filter(shop_type=type).values()
        dic = {
            "Type": "Success",
            "Message": "Shop listed successfully",
            "data": list(shop_lists),
        }
        return Response(data=dic, status=status.HTTP_201_CREATED)


class GetShop(generics.ListAPIView):
    def get(self, request, **kwargs):
        shop_id = request.query_params['shop_id']
        shop_lists = []
        shop_lists = ShopInfo.objects.filter(shop_id=shop_id).values()
        print(list(shop_lists))
        owner_lists = []
        owner_lists = OwnerInfo.objects.filter(owner_shop=shop_id).values()
        dic = {
            "Type": "Success",
            "Message": "Shop listed successfully",
            "shopData": list(shop_lists),
            "ownerData": list(owner_lists                                                                                                                                                                                                ),
        }
        return Response(data=dic, status=status.HTTP_201_CREATED)


class ContactUsView(generics.CreateAPIView):
    """ To contact """

    def post(self, request):
        try:
            fname = request.data.get('fname')
            lname = request.data.get('lname')
            email = request.data.get('email')
            comment = request.data.get('comment')

            contact_data = {
                "fname": fname,
                "lname": lname,
                "email": email,
                "comment": comment,
            }

            ContactSerializer = ContactUsSerializer(data=contact_data)
            if ContactSerializer.is_valid(raise_exception=True):
                ContactSerializer.save()

                dic = {
                    "Type": "Success",
                    "Message": "Message added successfully",
                    "data": ContactSerializer.data
                }
            else:
                dic = {
                    "Type": "Error",
                    "Message": "Message added unsuccessfully",
                    "data": ""
                }

            return Response(data=dic, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            print(e)
            dic = {
                "Type": "Error",
                "Message": "Message added unsuccessfully",
                "data": e.detail
            }
            return Response(data=dic, status=status.HTTP_201_CREATED)
