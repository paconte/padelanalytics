from django.contrib import admin
from .models import Club, Tournament, Player, Registration

admin.site.register(Club)
admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Registration)
