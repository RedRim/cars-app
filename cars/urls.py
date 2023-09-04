from .views import *

from django.urls import path

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('contact/', contact, name='contact'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('brand/<slug:brand_slug>/', CarsBrand.as_view(), name='brand'),
    path('modering/', Modering.as_view(), name='modering'),
    path('post/toggle_published/<slug:post_slug>/', toggle_is_published, name='toggle_is_published'),
    path('post/createcomment/<slug:post_slug>/', create_comment, name='create_comment'),
    path('post/like', ShowPost.image_like, name='add_like')
]

handler404 = pageNotFound