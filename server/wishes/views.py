import requests
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, decorators, status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from wishes.serializers import WishListSerializer, WishSerializer

from .models import Wish, WishList


class WishListView(generics.ListAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class WishView(generics.ListAPIView):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer


@decorators.api_view(['GET'])
def user_wishlists(request: Request, username: str) -> Response:
    user = User.objects.get(username=username)
    wish_lists = WishList.objects.filter(owner=user.id)
    serialized_wish_lists = WishListSerializer(wish_lists, many=True)
    return Response(serialized_wish_lists.data, status=status.HTTP_200_OK)


@decorators.api_view(['GET'])
def user_wishes(request: Request, wishlist_slug: str) -> Response:
    wishlist = WishList.objects.get(slug=wishlist_slug)
    wishes = Wish.objects.filter(wish_list=wishlist)
    serialized_wish_list = WishListSerializer(wishlist)
    serialized_wishes = WishSerializer(wishes, many=True)
    return Response({ "wishlist": serialized_wish_list.data, "wishes": serialized_wishes.data }, status=status.HTTP_200_OK)


@decorators.api_view(['POST', 'PUT'])
def create_edit_user_wishlist(request: Request, username: str) -> Response:
    if (request.method == 'POST'):
        user = User.objects.get(username=username)
        request.data['owner'] = user.id
        request.data['slug'] = slugify(request.data['name'])
        wishlist_serializer = WishListSerializer(data=request.data)
        wishlist_serializer.is_valid(raise_exception=True)
        wishlist_serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        user = User.objects.get(username=username)
        wishlist = WishList.objects.get(slug=request.data['slug'])
        wishlist.name = request.data['name']
        wishlist.description = request.data['description']
        wishlist.slug = slugify(wishlist.name)
        wishlist.save()
        return Response(status=status.HTTP_200_OK)


@decorators.api_view(['DELETE'])
def delete_wishlist(request: Request, slug):
    wishlist = WishList.objects.get(slug=slug)
    wishlist.delete()
    return Response(status=status.HTTP_200_OK)


@decorators.api_view(['PUT'])
def set_wish_bought(request: Request):
    wish = Wish.objects.get(pk=request.data["id"])
    wish.bought = request.data["bought"]
    wish.save()
    return Response(status=status.HTTP_200_OK)


@decorators.api_view(['DELETE'])
def delete_wish(request: Request, id: str):
    Wish.objects.get(pk=id).delete()
    return Response(status=status.HTTP_200_OK)


@csrf_exempt
@decorators.api_view(['POST'])
def fetch_rozetka(request: Request):
    wishlist_id = request.data['wishlist_id']
    response = requests.get(request.data['uri'])
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    image = soup.select_one('.picture-container__picture').get_attribute_list("src")[0]
    title = soup.select_one('.product__title').getText().strip()
    price = soup.select_one('.product-price__big').getText()
    description = soup.select_one('.product-about__description-content').getText()
    link = request.data['uri']

    wish_serializer = WishSerializer(data={"link": link, "image_link": image, "name": title, "price": price[:-1], "description": description, "wish_list": wishlist_id})
    wish_serializer.is_valid(raise_exception=True)
    wish_serializer.save()
    return Response(status=status.HTTP_200_OK)
