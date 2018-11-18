import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authtoken.models import Token

User = get_user_model()


def features(request):
    return render(request, 'www/features.html', {})


def request_token(request):
    User.objects.all().delete()
    email = request.POST.get('email', None)
    email_confirm = request.POST.get('email-confirm', None)

    if email == email_confirm and email:
        user, created = User.objects.get_or_create(username=email, password=uuid.uuid4().hex)
        if user:
            token = Token.objcts.get_or_create(user=user)
            token.key = None  # renew token for every request
            token.save()
    else:
        pass

    return render(request, 'www/register.html', {})
