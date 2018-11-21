from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from pipetaxon.settings import VALID_RANKS
from taxonomy.models import Taxonomy, Division


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

    def pagination_slice(self):
        current_page_number = self.get_context_data()['page_obj'].number
        lower = current_page_number - 9
        higher = current_page_number + 9

        if lower < 0:
            lower = 0
            higher = 18

        return "{0}:{1}".format(lower, higher)

    @property
    def filters(self):
        return {'rank': self.request.session.get('rank', None), 'division': self.request.session.get('division', None)}

    @property
    def division_list(self):
        return Division.objects.all().order_by('id')

    @property
    def rank_list(self):
        return VALID_RANKS


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
