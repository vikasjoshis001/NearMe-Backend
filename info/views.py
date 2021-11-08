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

            # if (shop_image == ""):
            #     shop_image = "images/logo.png"
            # if (shop_image == None):
            #     shop_image = "images/logo.png"

            shop_data = {
                "shop_name": shop_name,
                "shop_contact": shop_contact,
                "shop_email": shop_email,
                "shop_address": shop_address,
                "shop_type": shop_type,
                "shop_image":shop_image,
                "shop_description": shop_description,
                "owner_name": owner_name,
                "owner_contact": owner_contact,
                "owner_email": owner_email,
                "owner_address": owner_address,
            }

            ShopSerializer = ShopInfoSerializer(data = shop_data)
            if ShopSerializer.is_valid(raise_exception=True):
                ShopSerializer.save()

                # shopObj = ShopSerializer.save()
                # shopId = ShopInfo.objects.all().last()
                # sid = str(shopId.shop_id)
                # shopObj = ShopInfo.objects.filter(shop_id=sid)
                # if 'shop_image' in request.data:
                #     image_data = request.data.get('shop_image')
                #     format, imgstr = image_data.split(';base64,')
                #     ext = format.split('/')[-1]
                #     data = ContentFile(base64.b64decode(imgstr))
                #     file_name = shop_type + "_" + str(random.randint(1, 100))+ext
                #     shopObj[0].shop_image.save(file_name, data, save=True)
                # ShopSerializer = ShopInfoSerializer(shopObj[0])
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
        print(list(shop_lists))
        dic = {
            "Type": "Success",
            "Message": "Shop listed successfully",
            "data": list(shop_lists),
        }
        return Response(data=dic, status=status.HTTP_201_CREATED)
