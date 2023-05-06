from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import UserView, detail_user_view, create_user_view

urlpatterns = [
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('all/', UserView.as_view()),
    path('user/<str:username>', detail_user_view),
    path('user/create/', create_user_view)
]
