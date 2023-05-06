from django.contrib import admin

from wishes.models import Wish, WishList

admin.site.site_title = 'alisa\'s administration'
admin.site.site_header = 'alisa\'s Administration'

admin.site.register(Wish)
admin.site.register(WishList)
