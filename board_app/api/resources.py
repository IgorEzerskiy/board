from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from board_app.api.serializers import CategoryReadSerializer, CardSerializer
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


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer


class CardModelViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDeleteAPIView(DestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

