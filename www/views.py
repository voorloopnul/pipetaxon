import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from .forms import GetTokenForm
from .models import send_email_with_token

User = get_user_model()


def features(request):
    return render(request, 'www/features.html', {})


def request_token(request):
    form = GetTokenForm()
    if request.POST:
        form = GetTokenForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User.objects.create(username=email, password=uuid.uuid4().hex)

            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
            send_email_with_token(email, token)

    return render(request, 'www/register.html', {'form': form})
