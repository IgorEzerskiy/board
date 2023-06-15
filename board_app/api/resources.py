from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from board_app.api.serializers import CategoryReadSerializer, CardSerializer
from board_app.models import Card, Category


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer


class CardModelViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
