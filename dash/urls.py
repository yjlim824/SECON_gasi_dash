from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dash.html', views.index),
]
