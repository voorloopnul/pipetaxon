from django import forms


class GetTokenForm(forms.Form):
    email = forms.EmailField(label="Email address")
    email2 = forms.EmailField(label="(Confirm) Email address")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")

        if email != email2:
            self.add_error('email2', "Email addresses doesn't match!")
