from django.conf.urls import url
from django.urls import path
from anmeldung import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^anmeldung$', views.anmeldung, name='anmeldung'),
    url(r'^turnierliste$', views.turnierliste, name='turnierliste'),
    path('toutnament/<int:id>/', views.tournament, name='tournament'),
    path('clubs', views.clubs, name='clubs'),
]
