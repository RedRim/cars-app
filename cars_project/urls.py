from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 

from cars_project import settings   
from cars.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars.urls'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, documentation_root=settings.MEDIA_ROOT)
