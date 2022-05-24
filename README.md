# KBTU-Djangщ-final-project

# Final project intrustions

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Limkaa/KBTU-Django-final-project.git
$ cd KBTU-Django-final-project
```

```sh
$ cd project
$ python manage.py makemigrations
$ python manage.py migrate
```

In order to be able to log into admin panel create superuser

```sh
$ python manage.py createsuperuser
email: admin@example.com
password: admin
```

### Let's make easier testing API

For that purpose project root directory has `project.postman_collection.json`.
It is a file with all necessary API methods and other settings, which can be imported to your Postman. Just you for that 'import' option in Postman menu. After you successfully did this, we can go to next and final step!

### Let's run project

Type this in terminal:

```sh
(env)$ cd project
(env)$ python manage.py runserver
```

Then go to Postman and try to make your first API request for this project using Postman
Have fun :)
