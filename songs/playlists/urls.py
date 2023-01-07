from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views
urlpatterns = [
    path('songs',views.songs),
    path('songs/<int:id>', views.song_details),
    path('playlists/<int:id>', views.playlist_details),
    path('playlists', views.playlists),
    path('add-to-playlist', views.add_to_playlist),
    path('remove-from-playlist', views.remove_from_playlist),
    path('users/token', auth_views.obtain_auth_token),
    path('users/register', views.create_user)
]
