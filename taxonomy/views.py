from django.shortcuts import render
from django.views.generic import ListView
from pipetaxon.settings import VALID_RANKS
from taxonomy.models import Taxonomy, Division, ALL_RANKS


class Index(ListView):
    template_name = 'taxonomy/index.html'
    model = Taxonomy
    paginate_by = 19

    def get_queryset(self):
        division = self.request.GET.get('division', None)
        rank = self.request.GET.get('rank', None)
        search_string = self.request.GET.get('search_string', None)
        filters = {}

        if division:
            filters['division'] = division

        if rank:
            filters['rank'] = rank

        if search_string:
            filters['name__contains'] = search_string

        queryset = Taxonomy.objects.filter(**filters)
        return queryset

    @property
    def filters(self):
        return {'rank': self.request.GET.get('rank', None), 'division': self.request.GET.get('division', None)}

    @property
    def division_list(self):
        return Division.objects.all().order_by('id')

    @property
    def rank_list(self):
        return VALID_RANKS if VALID_RANKS else ALL_RANKS


def api(request):
    return render(request, 'taxonomy/api.html', {})
