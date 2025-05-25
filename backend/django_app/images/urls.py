from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.upload_archive, name='upload_archive'),
    path('process/<int:archive_id>/', views.process_images, name='process_images'),
    path('download/<int:archive_id>/', views.download_processed_archive, name='download_processed_archive'),
    path('receive/<int:archive_id>/', views.receive_processed_archive, name='receive_processed_archive'),
]
