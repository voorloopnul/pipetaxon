from django.core.mail import EmailMultiAlternatives


def send_email_with_token(to, token):
    subject, from_email, to = 'New token to access PipeTaxon API', 'noreply@mg.voorloop.com', to
    text_content = 'Hey,\nHere is your new access token for PipeTaxon: {0}\n\nRegards,\nRicardo Pascal'.format(token.key)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], reply_to=('pipetaxon@voorloop.com',))
    msg.send()
