# Secured back-end architecture with Django ORM
*by Jean-Corentin Loirat*
on 27/10/2022

Git hub link : https://github.com/BeanEden/Project12

## Description :
"Epic Event" is a CRM developed for an event-organizing company

## Technologies :
* Django
* Python
* PostgreSQL

## Set up :

### 1 - Download the zip file :
Install the elements in the repository of your choice

### 2 - Create a virtual environment in your repo and activate it :
* Terminal command : `cd path/to/selected/project/directory`
* Terminal command : `python -m venv env`
* Terminal command : `env/Scripts/activate.bat` (Windows)

### 3 - Import packages :
Import in your virtual environment the necessary packages
* Terminal command : `pip install -r requirements.txt`

### 4 - Set up POSTGRESQL :
* Install postgres
* Install psycopg2  `pip install psycopg2`
* Create a ".env" file with your database information (an example is provided ".env.example") 
* The database set-up should be complete and properly red by "settings.py"

Additional information :
- PostgreSql with django : https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django
- example with a .env file : https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8

### 5 - Check for migrations :
Check if the migrations are up to date
* Terminal command : `python manage.py makemigrations`
* Terminal command : `python manage.py migrate`

### 6 - Load data or create superuser:
You can choose to read the provided .json database with : `python manage.py loaddata example.json`.
You can also create your own superuser to startyour new DB : `python manage.py createsuperuser`

It is recommended to check for migrations after loading the example db


### 5 - Start the server :
Start the server in order to use the API
* Terminal command : `python manage.py runserver`


## Using the CRM
After starting the server, the user can connect at :
http://127.0.0.1:8000/


### Connection :
You need a provided account or a superuser account to access the CRM.
You can't register on your own.

All others endpoints/views require to be authenticated


## API architecture :
4 models exists : 
* User
* Customer
* Contract
* Event

These Models are managed through serializers.

Controllers manage CRUD operations and Views.


### Security :

The CRM/API is secured against :
- authentication (access and refresh token, limited time session, only use while authenticated)
- injection (fields are slugs / alphanumeric / predetermined choices, including the search field)
- unauthorized actions (a support_user can't create a new user for example)

The app is designed to never crash and always redirect in case of misuse. 

### Access : 

Only one admin is selected : the superuser
Everyone else is a regular user with its specific permissions.

Every user type has its own view (read_only / update).

## Logging :
User login and log out are followed.
An error log is also set up.

## Learn more :
Classes and functions are documented with docstrings about their use, arguments and responses.