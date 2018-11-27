import uuid
from django import forms
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from rest_framework.authtoken.models import Token


class GetTokenForm(forms.Form):
    email = forms.EmailField(label="Email address")
    email2 = forms.EmailField(label="(Confirm) Email address")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")

        if email != email2:
            self.add_error('email2', "Email addresses doesn't match!")

    def create_token(self):
        try:
            user = User.objects.get(username=self.cleaned_data['email'])
        except User.DoesNotExist:
            user = User.objects.create(username=self.cleaned_data['email'], password=uuid.uuid4().hex)

        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.delete()
            token = Token.objects.create(user=user)
        self._send_email_with_token(self.cleaned_data['email'], token)

    @staticmethod
    def _send_email_with_token(to, token):
        subject, from_email, to = 'New token to access PipeTaxon API', 'noreply@mg.voorloop.com', to
        text_content = 'Hey,\nHere is your new access token for PipeTaxon: {0}\n\nRegards,\nRicardo Pascal'.format(token.key)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], reply_to=('pipetaxon@voorloop.com',))
        msg.send()
