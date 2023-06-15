from django.urls import path, include
from rest_framework import routers

from board_app.api.resources import CategoryListAPIView, CardModelViewSet

router = routers.SimpleRouter()
router.register(r'board', CardModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListAPIView.as_view()),
]
