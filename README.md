# Digitized Voting for Academic Institutions

[![Python Version](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.1-brightgreen.svg)](https://djangoproject.com)

This is a project to complement by research and in fulfillment of my computer science degree. The project offers an effective solution to the expensive, time-consuming elections across most Academic Institutions. COVID-19 brought everything to a standstill in 2020 and this partly inspired research into this. 

### Stack ###
1. Django Framework
2. Bootstrap CSS Framework

**Important:** Local database is SQLite3. But please use POSTGRES when in production since SQLite just wasn't built for that.

### Desired / TODO ###
1. Sign in process should use OTP. Student enters email/mobile number already on file at the university, receives OTP and enters this to verify identity and login. 
2. Once signed in, Student has 5 minutes to vote in any election or else timed out. Logging back in is only after 30mins
3. On the voting screen, radio buttons should consist of clear poster images of the candidates.


### Running the Project Locally

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

The project will be available at **127.0.0.1:8000**


### License

The source code is released under the [MIT License](https://github.com/crukundo/digitized-voting/blob/master/LICENSE).

### Demo Credentials

**EC Officer**: username: officer, password: ultimate012

You can create a new EC officer here: http://127.0.0.1:8000/accounts/signup/ec/ (testing purposes only.)
