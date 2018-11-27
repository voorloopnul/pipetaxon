from django.contrib.auth import get_user_model
from django.shortcuts import render
from .forms import GetTokenForm

User = get_user_model()


def features(request):
    return render(request, 'www/features.html', {})


def request_token(request):
    msg = None
    form = GetTokenForm()
    if request.POST:
        form = GetTokenForm(request.POST)
        if form.is_valid():
            form.create_token()
            msg = "Token sent to {0}".format(form.cleaned_data['email'])
    return render(request, 'www/register.html', {'form': form, 'msg': msg})
