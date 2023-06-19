from django.urls import path, include
from rest_framework import routers

from board_app.api.resources import CategoryListAPIView, CardModelViewSet, CardDeleteAPIView, AuthToken

router = routers.SimpleRouter()
router.register(r'board', CardModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListAPIView.as_view()),
    path('card-delete/<int:pk>', CardDeleteAPIView.as_view()),
    path('login/', AuthToken.as_view())
]
