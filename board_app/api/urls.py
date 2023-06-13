from django.urls import path, include
from rest_framework import routers


router = routers.SimpleRouter()
# router.register(r'', )

urlpatterns = [
    path('', include(router.urls)),
]
