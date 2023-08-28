from django.contrib import admin

from code_review.models import File, Log


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_display_links = ('id', 'name', 'status')
    search_fields = ('name', 'status')
    list_filter = ('name', 'status')
    ordering = ['id']


@admin.register(Log)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'linter', 'sent_status', 'datetime')
    list_display_links = ('id', 'linter')
    search_fields = ('linter', 'datetime')
    list_filter = ('linter', 'datetime')
    ordering = ('id',)
