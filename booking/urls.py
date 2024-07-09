from django.urls import path
from . import views

urlpatterns = [
    path ('', views.main, name='main'),
    path ("<movie>/shows", views.shows, name = 'shows'),
    path ("shows/<int:shownum>/seats", views.seats, name = 'seats'),
    path ("cancel", views.cancel, name = 'cancel')
    ]