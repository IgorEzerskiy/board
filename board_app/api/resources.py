from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from board_app.api.permissions import IsAuthenticatedOrPermissionDeny
from board_app.api.serializers import CategoryReadSerializer, CardSerializer, CardCreateSerializer, \
    UserCreateSerializer, UserReadSerializer, CardUpdateSerializer
from board_app.models import Card, Category


class AuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'token': token.key,
        })

# User views


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserReadAPIVIew(ListAPIView):
    serializer_class = UserReadSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrPermissionDeny, IsAdminUser]

# Category Views


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    permission_classes = [IsAuthenticatedOrPermissionDeny]

# Card Views


class CardCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CardCreateSerializer
    permission_classes = [IsAuthenticatedOrPermissionDeny]

    def get_serializer_context(self):
        context = super(CardCreateAPIView, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context


class CardModelViewSet(ModelViewSet):
    """Use ?search=<category__name>"""
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedOrPermissionDeny]
    filter_backends = [SearchFilter]
    search_fields = ['category__name']
    http_method_names = ['get']


class CardDeleteAPIView(DestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticatedOrPermissionDeny, IsAdminUser]


class CardUpdateAPIView(UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardUpdateSerializer
    permission_classes = [IsAuthenticatedOrPermissionDeny]

    def get_serializer_context(self):
        context = super(CardUpdateAPIView, self).get_serializer_context()
        context.update(
            {"user": self.request.user}
        )
        return context
