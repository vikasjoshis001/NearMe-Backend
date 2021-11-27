from .models import *
from rest_framework import serializers, status


class ShopInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopInfo
        fields = '__all__'
        
class OwnerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OwnerInfo
        fields = '__all__'


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = '__all__'
