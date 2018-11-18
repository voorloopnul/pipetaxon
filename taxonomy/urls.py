from django.urls import path
from rest_framework import routers
from taxonomy.api import TaxonomyViewSet, LCAView
from taxonomy.views import Index, apply_filter, api

router = routers.SimpleRouter()
router.register(r'api/taxonomy/lca', LCAView, base_name='taxonomy-lca')
router.register(r'api/taxonomy', TaxonomyViewSet, base_name='taxonomy')

urlpatterns = [
    path('', Index.as_view(), name='site-list'),
    path('filter/', apply_filter, name='site-filter'),
    path('api/', api, name='site-api'),
]

urlpatterns += router.urls
