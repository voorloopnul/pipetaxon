#!/usr/bin/env bash

# clean old build
rm -r dist pipetaxon.pyz

# include the dependencies from `pip freeze`
pip install -r <(pip freeze) --target dist/

# or, if you're using pipenv
# pip install -r  <(pipenv lock -r) --target dist/

# specify which files to be included in the build
# You probably want to specify what goes here
cp -r pipetaxon dist
cp -r taxonomy dist
cp manage.py dist
cp db.sqlite3 dist

# finally, build!
shiv --site-packages dist --compressed -p '/usr/bin/env python3' -o pipetaxon.pyz -e pipetaxon.main