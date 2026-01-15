from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('api/send/', views.ChatAPIView.as_view(), name='send'),
    path('api/clear/', views.ClearHistoryView.as_view(), name='clear'),
]
