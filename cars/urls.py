from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('models/<slug:model>/', models, name='models',)
]

handler404 = pageNotFound