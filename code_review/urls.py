from django.urls import path

from code_review.views import upload_file, modify_file, get_files, get_file_log, delete_file

app_name = 'code_review'

urlpatterns = [
    path('', get_files, name='get_files'),
    path('<int:file_id>/}', get_file_log, name='get_file_log'),
    path('upload/', upload_file, name='upload_file'),
    path('modify/<int:pk>/', modify_file, name='modify_file'),
    path('delete/<int:pk>/', delete_file, name='delete_file')
]
