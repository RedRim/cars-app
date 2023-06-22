from django.urls import path

from .views import *

urlpatterns = [
    path('', CarsHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<int:post_int>/', ShowPost.as_view(), name='post'),
    path('brand/<slug:brand_slug>/', CarsBrand.as_view(), name='brand'),
]

handler404 = pageNotFound