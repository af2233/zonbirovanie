from django.urls import path, include

from .views import LogoutView


app_name = 'users'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('logout/', LogoutView.as_view(), name='logout'),
]
