from django.contrib import admin
from .models import Song, Listener, Playlist, Payment

# Register your models here.
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'album', 'genre']
    
class ListenerAdmin(admin.ModelAdmin):
    list_display = ['username', 'gender', 'contact', 'member']
    
class PlaylistAdmin(admin.ModelAdmin):
     list_display = ['name','listener_name', 'songs']

    
admin.site.register(Song)
admin.site.register(Listener, ListenerAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Payment)

    