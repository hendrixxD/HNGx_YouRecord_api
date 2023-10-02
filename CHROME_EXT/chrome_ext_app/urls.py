from django.urls import path
from . import views

app_name='chrome_ext_app'
urlpatterns = [
    
    path('create_video/', views.CreateRecordingView.as_view()),
    path('all_records/', views.AllRecordingsView.as_view()),
    path('save-data/<int:id>/', views.GetDataView.as_view()),
    path('singlevideo/<int:id>/', views.GetSingleVideoView.as_view()),
    
    # path('playback/<uuid:unique_identifier>/', SingleVideoView.as_view(), name='video_playback'),
]

