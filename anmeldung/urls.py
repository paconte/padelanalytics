from django.conf.urls import url
from django.urls import path
from anmeldung import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('tournament_signup', views.tournament_signup, name='tournament_signup'),
    path('tournament_signup/<int:id>/', views.tournament_signup, name='tournament_signup'),
    url(r'^turnierliste$', views.turnierliste, name='turnierliste'),
    path('toutnament/<int:id>/', views.tournament, name='tournament'),
    path('clubs', views.clubs, name='clubs'),
]
