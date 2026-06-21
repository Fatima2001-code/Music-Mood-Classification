from django.urls import path
from django.urls import re_path as url
from Test import views 

urlpatterns = [
    path('', views.Login, name='Login'),
    url(r'^AudioUpload',views.audioUpload,name="audioUpload"),
    path('', views.audioUpload, name='AudioUpload'),
    url(r'^ModelSelection',views.toModelSelection,name="toModelSelection"),
    path('', views.getBack, name="toAudioUpload"),
    url(r'^Prediction', views.toPrediction, name="toPrediction"),
    path('returnModelSelection/', views.returnModelSelection, name="RMS"),
    path('', views.getBack, name="end"),
]