from .views import *

from django.urls import path

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/<slug:profile_slug>/', Profile.as_view(), name='profile'),
    path('edit/', EditProfile.as_view(), name='editprofile'),
    path('edit/password/', EditPassword.as_view(), name='editpassword'),
    path('follow/', follow_user, name='follow')
]

handler404 = pageNotFound