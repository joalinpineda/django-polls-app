# django-polls-app

A single Django App based on [Django Tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/)

## Getting started:

*Create a virtual enviroment*

For Windows users:

`py -m venv venv`

For unix based OS (Linux and macOS):

`python3 -m venv venv`

*Turn on the enviroment*

For Windows users:

`source\Scripts\activate`

For unix based OS (Linux and macOS):

`source venv/bin/activate`

*Install dependencies*

`pip install -r requirements.txt`

**Make migrations**

`python3 manage.py makemigrations`

**Migrate**

`python3 manage.py migrate`

**Create some data at Database**

You can make a superuse to access to Django Admin

**Create super user**
``python3 manage.py createsuperuser``

**Now you can enter some data**


*Run development server*

Win:
`py manage.py runserver`

Linux/macOS:
`python3 manage.py runserver`

And its done. 
Happy hacking!✌️