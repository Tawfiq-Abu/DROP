from django.urls import path
from .views import UploadLeaderboardView,LeaderboardView
from .views import export_contestants_to_excel


urlpatterns = [
    path('upload/', UploadLeaderboardView.as_view(), name='upload-leaderboard'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('export-contestants/', export_contestants_to_excel, name='export_contestants'),
]
