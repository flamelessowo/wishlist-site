from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from users.models import Profile


class WishList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=False)
    description = models.CharField(max_length=300, null=True)
    created_date = models.DateTimeField(default=now, editable=False)
    slug = models.SlugField(verbose_name='Slug', default='dummy-wish-list')
    shared_with = models.ManyToManyField(Profile, blank=True)

    def __str__(self):
        return f'{self.owner.username}\'s {self.name} wishlist'

    class Meta:
        verbose_name = 'Wish List'
        verbose_name_plural = 'Wish Lists'


class Wish(models.Model):
    wish_list = models.ForeignKey(to=WishList, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=250, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    image_link = models.CharField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=False, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    bought = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.wish_list.owner.username}\'s {self.name} wish item'

    class Meta:
        verbose_name = 'Wish'
        verbose_name_plural = 'Wishes'
