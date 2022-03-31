from django.urls import path
from .views import map_views, dash_views
from . import views

urlpatterns = [
    path('', dash_views.index),
    path('index.html', dash_views.index),
    path('map.html', map_views.map, name='map'),
]
