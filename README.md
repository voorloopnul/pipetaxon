# Project Title

PipeTaxon exposes the ncbi taxonomy database as a REST API. It's intended to be consumed by bioinformatic pipelines or dataviz applications.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This README is based on Ubuntu 18.04, other systems may have small difference in those steps.


### Installing

**download the latest taxdump from ncbi**
 
 ```
 wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
 ```

**decompress it**
 
 ```tar -zxvf taxdump.tar.gz ~/data```

**clone this repository**
 
 ``` git clone https://github.com/voorloopnul/pipetaxon.git ```

**enter project folder**
 
 ``` cd pipetaxon ```

**create a virtualenv** 
 
 ```python3 -m venv ~/venv/pipetaxon```

**enter the virtualenv**
 
 ```source ~/venv/pipetaxon```

**install the requirements**
 
 ```pip install -r requirements```

**build taxonomy database**
 
 ```./manage.py build_from_ncbi_full --taxonomy ~/data/```
 
**build lineage**
 
 ```./manage.py build_from_ncbi_full --lineage data/``` 

 > The --lineage command took 25 minutes and the --taxonomy 3 minutes in my I5 laptop

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Django](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [django-rest-framework](https://maven.apache.org/) - Dependency Management
* [gunicorn](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


