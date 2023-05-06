from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, decorators, status
from django.core.exceptions import ObjectDoesNotExist

from wishes.serializers import WishListSerializer, WishSerializer

from .models import Wish, WishList


class WishListView(generics.ListAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class WishView(generics.ListAPIView):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
