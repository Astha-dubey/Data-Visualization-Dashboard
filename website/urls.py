from django.contrib import admin
from django.urls import path
from website import views
urlpatterns = [
    path('corruption/', views.graph_view,name='corruption data'),
    path('crimerate/', views.crime_rate_chart,name='crime rate chart'),
    path('development_index/', views.development_index,name='development index chart'),
    path('gdp/', views.gdp_chart,name='GDP chart'),
    path('internet_users/', views.internet_users,name='internet users chart'),
    path('literacy/', views.literacy,name='literacy users chart'),
    path('pollution/', views.pollution,name='pollution chart'),
    path('population/', views.population,name='population chart'),
    path('poverty/', views.poverty,name='poverty chart'),
    path('unemployment/', views.unemployment,name='unemployment chart'),
    path('render/', views.renderform,name='common form chart selection'),
    path('', views.renderform,name='common form chart selection')
]
