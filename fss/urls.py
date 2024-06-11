from django.urls import path
from . import views

app_name = 'fss'
urlpatterns = [
    path('', views.index, name='index'),
]