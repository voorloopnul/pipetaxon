# Pipetaxon

PipeTaxon exposes the ncbi taxonomy database as a REST API. It's intended to be consumed by bioinformatic pipelines or dataviz applications.

![alt text](https://i.imgur.com/A7Vxzq9.png)

## Getting Started (the super easy way)

Just open a terminal and copy&paste the following command:
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

We have packaged pipetaxon as a docker container, you should be able to get it up effortless by simply running the following commands:

```
docker pull voorloop/pipetaxon
```

```
docker run -p **80**:8000 voorloop/pipetaxon
```

if the default HTTP port is already in use or you don't have permission you can simply change it for any other port:
 
```
docker run -p **81**:8000 voorloop/pipetaxon
```

Then go ahead to your browser and type:

 > `http://localhost` (when you choose port 80) or `http://localhost:81` (or any other port you have chosen)


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

The accession data is quite large, if you need to get all the data SQLite probably will not handle it very well.
We have tested `nucl_gb.accession2taxid.gz` with SQLite, the database got 11GB and took one hour to add all the 266 millions of accession IDs in this file.


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

SQLITE should suffice for most use cases of standalone execution of pipetaxon, but if you need an full featured RDBMS like
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

> NOTE: You need the create (or provide) valid credential to access the database. 

### Using custom lineage

By default all ranks present in NCBI will be part of your newly created taxonomy database, if you want to use a custom lineage
*(removing ranks that don't aggregate in your project)*, you can easily do that replacing the line `VALID_RANKS = []` to something like:
 
 ```
 VALID_RANKS = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
 ``` 
 
Keep in mind that you can't change these values after building your database, if you already have one running you first
need to clear it's data

```
./manage.py build_database --clear ~/data/
```

Them run again the build process:

 ```
 ./manage.py build_database --taxonomy ~/data/ 
 ```
 
 ```
 ./manage.py build_database --lineage ~/data/
 ``` 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
