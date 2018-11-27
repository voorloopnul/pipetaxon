from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from pipetaxon.settings import VALID_RANKS
from taxonomy.models import Taxonomy, Division, ALL_RANKS


class Index(ListView):
    template_name = 'taxonomy/index.html'
    model = Taxonomy
    paginate_by = 19

    def get_queryset(self):
        division = self.request.session.get('division', None)
        rank = self.request.session.get('rank', None)
        filters = {}
        if division:
            filters['division'] = division
        if rank:
            filters['rank'] = rank

        queryset = Taxonomy.objects.filter(**filters)
        return queryset

    @property
    def filters(self):
        return {'rank': self.request.session.get('rank', None), 'division': self.request.session.get('division', None)}

    @property
    def division_list(self):
        return Division.objects.all().order_by('id')

    @property
    def rank_list(self):
        return VALID_RANKS if VALID_RANKS else ALL_RANKS


def api(request):
    return render(request, 'taxonomy/api.html', {})


def apply_filter(request):
    if 'division' in request.POST:
        request.session['division'] = request.POST.get('division', None)
    elif 'rank' in request.POST:
        request.session['rank'] = request.POST.get('rank', None)
    else:
        print("reset filters")
    return HttpResponseRedirect("/")
