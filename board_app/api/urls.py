from django.urls import path, include
from rest_framework import routers

from board_app.api.resources import CategoryListAPIView, CardModelViewSet, CardDeleteAPIView, AuthToken, \
    CardCreateAPIView, UserCreateAPIView, UserReadAPIVIew, CardUpdateAPIView
router = routers.SimpleRouter()
router.register(r'board', CardModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListAPIView.as_view()),
    path('card-delete/<int:pk>', CardDeleteAPIView.as_view()),
    path('card-create/', CardCreateAPIView.as_view()),
    path('card-update/<int:pk>', CardUpdateAPIView.as_view()),
    path('login/', AuthToken.as_view()),
    path('registration/', UserCreateAPIView.as_view()),
    path('users/', UserReadAPIVIew.as_view())
]
