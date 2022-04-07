from django.urls import path
from .views import map_views, dash_views, map2_views, secon_views
from . import views

urlpatterns = [
    path('', dash_views.index),
    path('index.html', dash_views.index),
    path('map.html', map_views.map, name='map'),
    path('map2.html', map2_views.map, name='map2'),
    path('secon', secon_views.secon, name='secon'),
]
