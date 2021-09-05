from django.urls import path
from .views import welcome, upload_file, temp_country_creator

app_name = 'airpollution'

urlpatterns = [
    path('', welcome, name='welcome'),
    path('uplad_file', upload_file, name='upload_file'),
    path('temp_country_creator', temp_country_creator, name='temp_country_creator')
]
