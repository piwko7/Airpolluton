from django.urls import path
from .views import airpollution, temp_country_creator, temp_add_colors_to_pollutants,\
    airpollution_table_data, airpollution_visual_data_1, airpollution_visual_data_2
app_name = 'airpollution'

urlpatterns = [
    path('', airpollution, name='airpollution'),
    path('airpollution_table_data', airpollution_table_data, name='airpollution_table_data'),
    path('airpollution_visual_data_1', airpollution_visual_data_1, name='airpollution_visual_data_1'),
    path('airpollution_visual_data_2', airpollution_visual_data_2, name='airpollution_visual_data_2'),
    path('temp_country_creator', temp_country_creator, name='temp_country_creator'), #temp view to create models
    path('temp_add_colors_to_pollutants', temp_add_colors_to_pollutants, name='temp_add_colors_to_pollutants') #temp view to create models
]
