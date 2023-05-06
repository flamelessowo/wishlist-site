from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, data):
        user = User.objects.create_user(username=data['username'])
        user.set_password(data['password'])
        user.save()

        return user


class ProfileSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
