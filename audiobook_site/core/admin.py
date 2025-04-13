from django.contrib import admin

from core.models import AudioBook


@admin.register(AudioBook)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'audio_file')
