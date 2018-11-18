from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from taxonomy.models import Taxonomy
from taxonomy.serializers import TaxonomySerializer, NestedTaxonomySerializer


class TaxonomyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaxonomySerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ('rank', 'division',)
    search_fields = ('name',)

    def get_queryset(self):
        return Taxonomy.objects.all()

    @action(detail=True, methods=['get'])
    def lineage(self, request, pk=None):
        taxonomy = self.get_object()
        serializer = NestedTaxonomySerializer(instance=taxonomy)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LCAView(viewsets.ViewSet):

    def list(self, request, pk=None):
        taxid_list = request.GET.get("taxid_list", None)
        taxid_list = taxid_list.split(",")

        taxonomies = Taxonomy.objects.filter(taxid__in=taxid_list)
        for rank in ['genus', 'family', 'order', 'klass', 'phylum', 'kingdom', 'superkingdom']:
            values = []
            for taxonomy in taxonomies:
                values.append(taxonomy.__getattribute__(rank)())

            values = list(set(values))
            if len(values) == 1 and values != [False]:
                break

        if len(values) != 1:
            return Response("Not found")

        return Response(values[0].taxid)
