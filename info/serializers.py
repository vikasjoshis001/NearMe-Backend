from .models import *
from rest_framework import serializers, status

class ShopInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopInfo
        fields = '__all__'