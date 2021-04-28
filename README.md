# Digitized Voting for Academic Institutions

[![Python Version](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.1-brightgreen.svg)](https://djangoproject.com)

This is a project to complement by research and in fulfillment of my computer science degree. The project offers an effective solution to the expensive, time-consuming elections across most Academic Institutions. COVID-19 brought everything to a standstill in 2020 and this partly inspired research into this. 

### Stack ###
Django Framework
Bootstrap CSS Framework
JQuery
SQLite

NB: Please use POSTGRES when in production since SQLite just wasn't built for that.

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/crukundo/digitized-voting.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.


## License

The source code is released under the [MIT License](https://github.com/crukundo/digitized-voting/blob/master/LICENSE).
