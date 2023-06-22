from django.urls import path
from .views import WishView, user_wishlists, create_edit_user_wishlist, delete_wishlist, user_wishes, fetch_rozetka, set_wish_bought, delete_wish, remove_user_from_list, add_user_to_list, get_shared_wishlists

urlpatterns = [
    path('wishes/', WishView.as_view()),
    path('wishlists/<str:username>', user_wishlists),
    path('wishlists/get_shared_wishlists/<str:username>', get_shared_wishlists),
    path('wishlists/createUpdate/<str:username>', create_edit_user_wishlist),
    path('wishlists/delete/<str:slug>', delete_wishlist),
    path('wishes/<str:wishlist_slug>', user_wishes),
    path('wish/update', set_wish_bought),
    path('wish/delete/<str:id>', delete_wish),
    path('wishlists/remove/<str:profile_id>/<str:list_id>', remove_user_from_list),
    path('wishlists/add/<str:profile_id>/<str:list_id>', add_user_to_list),
    path('fetch/', fetch_rozetka)
]
