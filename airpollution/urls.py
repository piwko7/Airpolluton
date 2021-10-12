from django.urls import path
from . import views


app_name = 'airpollution'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('table/', views.table, name='table'),
    path('charts/', views.charts, name='charts'),
    path('airpollution_table_data', views.airpollution_table_data, name='airpollution_table_data'),
    path('airpollution_visual_data_1', views.airpollution_visual_data_1, name='airpollution_visual_data_1'),
    path('airpollution_visual_data_2', views.airpollution_visual_data_2, name='airpollution_visual_data_2'),
    path('temp_country_creator', views.temp_country_creator, name='temp_country_creator'), #temp view to create models
    path('temp_add_colors_to_pollutants', views.temp_add_colors_to_pollutants, name='temp_add_colors_to_pollutants') #temp view to create models
]
