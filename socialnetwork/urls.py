"""socialnetwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_feed, name='home_feed'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('create/', views.create_post, name='create_post'),
    path('livesearch/<str:word>/<int:sid1>.<int:sid2>/',
         views.livesearch, name='livesearch'),
    path('follow/<str:user_id>/', views.follow, name='follow'),
    path('unfollow/<str:user_id>/', views.unfollow, name='unfollow'),
    path('comment/<int:post_id>/', views.comment, name='comment'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('unlike/<int:post_id>/', views.unlike, name='unlike'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('notifications/', views.notifications, name='notifications'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
