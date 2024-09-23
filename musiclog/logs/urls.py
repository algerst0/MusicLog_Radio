from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.upload_csv),
    path('djs/songs/', views.dj_songs, name='dj-songs'),
    path('songs/', views.song_list, name='song-list'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('songs/', views.SongListView.as_view(), name='song-list'),
    path('songs/<int:id>/', views.SongDetailView.as_view(), name='song-detail'),
    path('programs/<str:program_name>/songs/', views.ProgramSongsView.as_view(), name='program-songs'),
    path('djs/<str:dj_name>/songs/', views.DJSongsView.as_view(), name='dj-songs'),
    path('artists/<str:artist_name>/songs/', views.ArtistSongsView.as_view(), name='artist-songs'),
]
