from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('taxonomy.urls')),
    path('', include('www.urls')),

]
