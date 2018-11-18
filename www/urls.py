from django.urls import path
from www.views import features, request_token

urlpatterns = [
    path('features/', features, name='site-features'),
    path('register/', request_token, name='site-register'),
]
