from django.urls import path, include

urlpatterns = [
    path('api/', include('board_app.api.urls'))
]
