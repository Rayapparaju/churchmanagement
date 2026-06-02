from django.contrib import admin
from .models import Sermon


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'bible_verse', 'date', 'series', 'is_published')
    list_filter = ('is_published', 'series', 'date')
    search_fields = ('title', 'speaker', 'bible_verse')
