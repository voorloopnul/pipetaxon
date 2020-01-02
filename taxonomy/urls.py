from django.urls import path
from rest_framework import routers
from taxonomy.api import TaxonomyViewSet, LCAView
from taxonomy.views import Index, api

router = routers.SimpleRouter()
router.register(r'api/taxonomy/lca', LCAView, basename='taxonomy-lca')
router.register(r'api/taxonomy', TaxonomyViewSet, basename='taxonomy')

urlpatterns = [
    path('', Index.as_view(), name='site-list'),
    path('api/', api, name='site-api'),
]

urlpatterns += router.urls
