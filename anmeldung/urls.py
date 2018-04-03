from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from anmeldung import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('tournament_signup', views.tournament_signup, name='tournament_signup'),
    path('tournament_signup/<int:id>/', views.tournament_signup, name='tournament_signup'),
    path('new_player', views.new_player, name='new_player'),
    url(r'^turnierliste$', views.turnierliste, name='turnierliste'),
    path('tournament/<int:id>/', views.tournament, name='tournament'),
    path('clubs', views.clubs, name='clubs'),
    path('ranking', views.ranking, name='ranking'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)