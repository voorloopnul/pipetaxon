import os
import sys

import django

# setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pipetaxon.settings")
django.setup()

try:
    production = sys.argv[1] == "production"
except IndexError:
    production = False

if production:
    import gunicorn.app.wsgiapp as wsgi

    # This is just a simple way to supply args to gunicorn
    sys.argv = [".", "pipetaxon.wsgi", "--bind=0.0.0.0:9999"]

    wsgi.run()
else:
    from django.core.management import call_command

    call_command("runserver")
