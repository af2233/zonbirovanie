from django.urls import path

from . import views


urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('process/<int:id>/', views.process, name='process'),
    path('receive/<int:id>/', views.receive, name='receive'),
    path('download/<int:id>/', views.download, name='download'),
]
