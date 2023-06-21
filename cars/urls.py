from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('addpage/', add_page, name='addpage'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<int:post_id>/', show_post, name='post'),
    path('brand/<int:brand_id>/', show_brand, name='brand'),
]

handler404 = pageNotFound