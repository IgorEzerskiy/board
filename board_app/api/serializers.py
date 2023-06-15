from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from board_app.models import Card, Category


class CategoryReadSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class CardSerializer(ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'assignee', 'reporter', 'title',
                  'text', 'category', 'created_at', 'updated_at',)

