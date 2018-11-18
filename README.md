# Step-by-Step: install and build database

`every step in here assumes your are in your home directory`

**download the latest taxdump from ncbi**
 > wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz

**decompress it**
 > tar -zxvf taxdump.tar.gz ~/data/

**clone this repository**
 > git clone https://github.com/voorloopnul/pipetaxon.git

**enter project folder**
 > cd pipetaxon

**create a virtualenv** 
 > python3 -m venv ~/venv/pipetaxon

**enter the virtualenv**
 > source ~/venv/pipetaxon

**install the requirements**
 > pip install -r requirements

**build taxonomy database**
 > ./manage.py build_from_ncbi_full --taxonomy ~/data/
 
**build lineage**
 > ./manage.py build_from_ncbi_full --lineage data/ 


`The --lineage command took 25 minutes and the --taxonomy took 3 minutes in my I3 laptop`