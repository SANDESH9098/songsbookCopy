from django.contrib import admin
from .models import Song

# Register your models here.

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug',  'status']
    prepopulated_fields = {'slug': ('title',)}
