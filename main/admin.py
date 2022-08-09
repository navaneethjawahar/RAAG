from django.contrib import admin

from .models import playlist_user, playlist_song ,recommended_song
# Register your models here.
admin.site.register(playlist_user)
admin.site.register(playlist_song)
admin.site.register(recommended_song)