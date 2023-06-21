from django.urls import path
from .views import WishView, user_wishlists, create_edit_user_wishlist, delete_wishlist, user_wishes, fetch_rozetka, set_wish_bought, delete_wish

urlpatterns = [
    path('wishes/', WishView.as_view()),
    path('wishlists/<str:username>', user_wishlists),
    path('wishlists/createUpdate/<str:username>', create_edit_user_wishlist),
    path('wishlists/delete/<str:slug>', delete_wishlist),
    path('wishes/<str:wishlist_slug>', user_wishes),
    path('wish/update', set_wish_bought),
    path('wish/delete/<str:id>', delete_wish),
    path('fetch/', fetch_rozetka)
]
