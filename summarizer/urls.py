from django.urls import path, include
from . import views

urlpatterns = [
    path('upload/', views.upload_and_summarize, name='upload_and_summarize'),
]