# Pipetaxon

PipeTaxon exposes the ncbi taxonomy database as a REST API. It's intended to be consumed by bioinformatic pipelines or dataviz applications.

### Main featuress

 - Expose the entire taxonomy database as an API
 - Provide a web interface for human interaction
 - Optionally can query taxonomy from accession id
 - Retrieve entire lineage from a taxonomy id
 - LCA endpoint (retrieve the lowest common ancestor from a list of taxonomy id) 
 - Allow exclusion of ranks

### Live demo

http://pipetaxon.voorloopnul.com:8888


![alt text](https://i.imgur.com/A7Vxzq9.png)

## Getting Started (the super easy way)

In a terminal copy and paste the following command:
```
curl https://raw.githubusercontent.com/voorloopnul/pipetaxon/master/install/install.sh | sudo bash
```

```
pipetaxon install
```

```
pipetaxon start
```

> Go to your browser and type: http://localhost:8888
       
## Getting Started (the easy way)

Pipetaxon is also a docker container, you should be able to get it up effortless by simply running the following commands:

```
docker pull voorloop/pipetaxon
```

```
docker run -p **80**:8000 voorloop/pipetaxon
```

if the default HTTP port is already in use or you don't have permission you can simply change it to any other port:
 
```
docker run -p **8888**:8000 voorloop/pipetaxon
```

Go to your browser and type:

 > `http://localhost` (when you choose port 80) or `http://localhost:8888` (or any other port you have chosen)


## Getting Started

These instructions should be enough to get an instance of pipetaxon running in a ubuntu system. By default it have all
ranks from NCBI and uses sqlite for database. Further instructions on how to setup pipetaxon with different databases 
and/or custom rank settings are available later in this document.


### Prerequisites

The following instructions are based on Ubuntu 18.04 other systems may have small differences in prerequisites and installation steps.

```
sudo apt-get install python3-venv
```


### Installing
 

*download the latest taxdump from ncbi* 
 ```
 wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz
 ```

*decompress it*
 ```
 mkdir ~/data/ && tar -zxvf new_taxdump.tar.gz -C ~/data/
 ```

*clone this repository* 
 ```
 git clone https://github.com/voorloopnul/pipetaxon.git
 ```

*enter project folder*
 ```
 cd pipetaxon
 ```

*create a virtualenv* 
  ```
 python3 -m venv ~/venv/pipetaxon
 ```

*enter the virtualenv*
 ```
 source ~/venv/pipetaxon/bin/activate
 ```

*install the requirements* 
 ```
 pip install -r requirements.txt
 ```

*run migrations*
 ```
 ./manage.py migrate
 ```

*build taxonomy database*
 ```
 ./manage.py build_database --taxonomy ~/data/
 ```
 
*build lineage*
 ```
 ./manage.py build_database --lineage ~/data/
 ``` 

 > The --lineage command took 25 minutes and the --taxonomy 3 minutes in my I5 laptop

## Adding the accession data (optional)

The accession data is quite large. If you need all the ids, SQLite might not be able to handle it very well.
We have tested `nucl_gb.accession2taxid.gz` with SQLite, the database size went to around 11GB and took one hour 
to create all the 266 millions accession IDs from this file.


 ```
 https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz
 ```

 ```
 mkdir ~/data/ && tar -zxvf nucl_gb.accession2taxid.gz -C ~/data/
 ```

 ```
 ./manage.py build_database --accession ~/data/
 ```

## Custom configurations 

### Working with different database

SQLITE should suffice most use cases of standalone execution of pipetaxon, but if you need a full featured RDBMS like
postgres or mysql your can easily configure it by changing the database config in settings.py to something like this:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'pipetaxon',
        'USER': '<username>',
        'PASSWORD': '<password>',
    }
}

```

### Using custom lineage

By default all ranks present in NCBI will be part of your newly created taxonomy database, if you want to use a custom lineage
*(removing ranks that don't add value to your project)*, you can easily do that by replacing the line `VALID_RANKS = []` to something like:
 
 ```
 VALID_RANKS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
 ``` 
 
Keep in mind that you can't change this settings after building your database, if you already have one pipetaxon instance running, you first
need to clear it's data

```
./manage.py build_database --clear ~/data/
```

Then you can run again the build process:

 ```
 ./manage.py build_database --taxonomy ~/data/ 
 ```
 
 ```
 ./manage.py build_database --lineage ~/data/
 ``` 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
