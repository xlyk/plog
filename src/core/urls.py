from django.contrib import admin
from django.urls import path

from plog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/<str:slug>/', views.PostView.as_view(), name='post'),
    path('', views.IndexView.as_view(), name='index')
]
