# Pipetaxon

PipeTaxon exposes the ncbi taxonomy database as a REST API. It's intended to be consumed by bioinformatic pipelines or dataviz applications.

![alt text](https://i.imgur.com/A7Vxzq9.png)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The following instructions are based on Ubuntu 18.04 other systems may have small differences in prerequisites and installation steps.

```
sudo apt-get install python3-venv
```


### Installing

The following steps should be enough to get an instance of pipetaxon running on ubuntu systems, by default it have all
ranks from NCBI and uses sqlite for database. Further instructions on how to setup pipetaxon with different databases 
and/or custom rank settings are available later in this document.
 

*download the latest taxdump from ncbi* 
 ```
 wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
 ```

*decompress it*
 ```
 tar -zxvf taxdump.tar.gz ~/data
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
 source ~/venv/pipetaxon
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
 ./manage.py build_from_ncbi_full --taxonomy ~/data/
 ```
 
*build lineage*
 ```
 ./manage.py build_from_ncbi_full --lineage data/
 ``` 

 > The --lineage command took 25 minutes and the --taxonomy 3 minutes in my I5 laptop

## Deployment

Add additional notes about how to deploy this on a live system

## Custom configurations 

### Working with different database 

### Using custom lineage

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


