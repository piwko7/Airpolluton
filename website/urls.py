from django.urls import path
from .views import index, samples

app_name = 'website'

urlpatterns = [
    path('', index, name='index'),
    path('samples/', samples, name='samples'),
]
