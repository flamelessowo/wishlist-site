from rest_framework import serializers
from .models import Wish, WishList


class WishListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='owner.username')
    class Meta:
        model = WishList
        fields = '__all__'


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = '__all__'
