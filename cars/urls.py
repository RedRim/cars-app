from django.urls import path

from .views import *

urlpatterns = [
    path('', CarsHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('contact/', contact, name='contact'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('brand/<slug:brand_slug>/', CarsBrand.as_view(), name='brand'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/<slug:profile_slug>/', Profile.as_view(), name='profile'),
    path('edit/', EditProfile.as_view(), name='editprofile'),
    path('edit/password/', EditPassword.as_view(), name='editpassword'),
    path('modering/', Modering.as_view(), name='modering'),
    path('post/toggle_published/<slug:post_slug>/', toggle_is_published, name='toggle_is_published'),
    path('post/createcomment/<slug:post_slug>/', create_comment, name='create_comment'),
    path('post/like', ShowPost.image_like, name='add_like')
]

handler404 = pageNotFound