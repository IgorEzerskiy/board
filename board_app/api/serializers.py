from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import User
from board_app.models import Card, Category

# User serializer


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

# Category serializer


class CategoryReadSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)

# Card serializer


class CardSerializer(ModelSerializer):
    assignee = UserReadSerializer()
    reporter = UserReadSerializer()
    category = CategoryReadSerializer()

    class Meta:
        model = Card
        fields = ('id', 'assignee', 'reporter', 'title',
                  'text', 'category', 'created_at', 'updated_at',)


class CardCreateSerializer(ModelSerializer):

    class Meta:
        model = Card
        fields = ('assignee', 'title',
                  'text',)

    def create(self, validated_data):
        user = self.context['user']
        validated_data['reporter'] = user
        validated_data['category'] = Category.objects.first()
        card = Card.objects.create(**validated_data)
        return card

    def validate_assignee(self, value):
        if self.context['user'].is_superuser or self.context['user'].is_staff:
            return value
        elif self.context['user'] != value:
            raise serializers.ValidationError(
                {"assignee": "User can not assign other users."}
            )
        return value


class CardUpdateSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('assignee', 'title',
                  'text', 'category',)

    def validate_assignee(self, value):
        if self.context['user'].is_superuser or self.context['user'].is_staff:
            return value
        elif self.context['user'] != value:
            raise serializers.ValidationError(
                {"assignee": "User can not assign other users."}
            )
        return value

    def validate_category(self, value):
        if self.context['user'] == self.instance.assignee or self.context['user'].is_staff:
            if (self.context['user'].is_staff or self.context['user'].is_superuser) \
                    and value.name in ('New', 'In progress', 'In QA') \
                    and self.context['user'] != self.instance.assignee:
                raise serializers.ValidationError(
                    {"category": "Staff can not move card to status: New, In progress, In QA."}
                )

            if (not self.context['user'].is_staff or not self.context['user'].is_superuser) \
                    and value.name == 'Done':
                raise serializers.ValidationError(
                    {"category": "User can not move card to status: Done."}
                )

            if self.instance.category.name == 'New' and value.name not in ('New', 'In progress') \
                    and (not self.context['user'].is_superuser or not self.context['user'].is_staff):
                raise serializers.ValidationError(
                    {"category": f'You can not move card to status: {value.name}.'}
                )

            if self.instance.category.name == 'In progress' and \
                    value.name not in ('New', 'In progress', 'In QA') \
                    and (not self.context['user'].is_superuser or not self.context['user'].user.is_staff):
                raise serializers.ValidationError(
                    {"category": f'You can not move card to status: {value.name}.'}
                )

            if self.instance.category.name == 'In QA' \
                    and value.name not in ('In progress', 'In QA', 'Ready') \
                    and (not self.context['user'].user.is_superuser or not self.context['user'].is_staff):
                raise serializers.ValidationError(
                    {"category": f'You can not move card to status: {value.name}.'}
                )

            if self.instance.category.name == 'Ready' \
                    and value.name not in ('In QA', 'Ready') \
                    and (not self.context['user'].is_superuser or not self.context['user'].is_staff):
                raise serializers.ValidationError(
                    {"category": f'You can not move card to status: {value.name}.'}
                )
        else:
            raise serializers.ValidationError(
                {"category": f'You can not move this card.'}
            )
        return value
