from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, decorators, status
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSeriazlier, UserSerializer


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@decorators.api_view(['GET'])
def detail_user_view(request: Request, username: str):
    try:
        user = User.objects.get(username=username)
        serialized_user = UserSerializer(user)
        profile = Profile.objects.get(owner=user.id)
        serialized_profile = ProfileSeriazlier(profile)
        return Response(serialized_user.data | serialized_profile.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@decorators.api_view(['POST'])
def create_user_view(request):
    try:
        user = User.objects.filter(username=request.data['username']).exists()
        if (user):
            return Response({"message": "This user already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        user_profile = Profile()
        user_profile.owner = user
        user_profile.save()

        return Response(status=status.HTTP_201_CREATED)

    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
