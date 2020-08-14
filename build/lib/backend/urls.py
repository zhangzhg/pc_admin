from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search),
    path('getChapterList', views.getChapterList),
    path('getContent', views.getContent),
    path('getAllContent', views.getAllContent)
]
