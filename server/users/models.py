from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    friends = models.ManyToManyField(User, related_name='friends_of', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="images/user-images", null=True)
    owner = models.ForeignKey(to=User, blank=False, on_delete=models.CASCADE, null=True)
