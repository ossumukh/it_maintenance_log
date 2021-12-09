from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('home/',views.home,name='coordinator_home')
]