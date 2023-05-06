from django.urls import path
from .views import WishListView, WishView

urlpatterns = [
    path('wishes/', WishView.as_view()),
    path('wishlists/', WishListView.as_view()),
]
