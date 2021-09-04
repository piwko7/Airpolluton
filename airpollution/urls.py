from django.urls import path
from .views import welcome

app_name = 'airpollution'

urlpatterns = [
    path('', welcome, name='welcome'),
]
