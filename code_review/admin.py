from django.contrib import admin

from code_review.models import File


@admin.register(File)
class FileModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_display_links = ('id', 'name', 'status')
    search_fields = ('name', 'status')
    list_filter = ('name', 'status')
    ordering = ['id']