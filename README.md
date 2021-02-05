# NHSEI Website

This is the repo for the NHS England & Improvement website https://england.nhs.uk

Currently available at https://nhsei-staging.uksouth.cloudapp.azure.com

# Developer Install Guide

Notes: 

* In production the site runs in a docker container but in development it can be more convenient to run the site in your local environment.

* Our ultimate aim is to have a development environment thats closer to the production environment and we should work on that ASAP

* You local environment requirements should meet the following:
Python >= 3.6, but we test and run it on Python 3.8 (the app is currently not compatible with v3.9)

* `sqlite3` we found to run tests sqlite3 --version should not be < 3.26 so you may need to upgrade it. On a mac run brew install sqlite

* Your development environment will be simpler to manage if you install it in a virtual environment or as a docker container. There are instructions below for setting up either a [docker container](#docker-container) or [virtual environment](#virtual-environment).

* The frontend styling, layout and components use the NHS.UK frontend design system: https://github.com/nhsuk/nhsuk-frontend. There's a [separate installation step](#front-end) required to install these using the node package manager (npm)

## How to install
---

Clone this repo to your local development machine

```
git clone https://github.com/rkhleics/nhs-ei.website [your_folder_name:optional]
```

then use either 1 or 2 below.

---

## <a name="docker-install"></a>1. Install using a docker container!

You will need 'docker' installed on your development machine. Get Docker: https://docs.docker.com/get-docker/

### Change into the root of the project e.g.

```
cd nhs-ei.website
```
or use the folder name you set when cloning the project.

### copy .env.example to .env
```
cp .env.example .env
```

### after you have installed docker...
```
docker-compose up
```

This will take a while to complete and will set up the environment and run the website and database service which you can then use develop on.

It mirrors all the services and packages needed to run in production.

---

## 2. Install using a virtual environment [recommended for development work]

You will need a package on your machine to be able to setup a virtual environment such as python -m venv, virtualenv or Pipenv. This example will use Pipenv

Create your virtual environment.
the python version should be 3.8
```
pipenv install -r requirements.dev
```
depending on your local python setup you may need to specify the version of python to use for the virtual environment...
```
pipenv install -r requirements.dev --python 3.8
```
### Your virtual environment should now be activated and ready to startup Wagtail

You should see the virtual environment name before your user account name e.g. (virtual-env-name) user@computer ...

If not run 
```
pipenv shell
```

When using the virtual environment setup Wagtail runs with a local database using sqlite3 and serves static files using the django static files app.

---

You should now be able to run the Wagtail app. If you are using 2. [virtual environment](#virtual-environment) then you will need to install the node packages to compile the frontend assets. If you are going to work only on the python/html files then this isn't required but it does come with the benefit of auto-reload on save when you change files, it's recommended!.

## 3. <a name="front-end"></a>Install NHS.UK Frontend design system

To compile the fontend assets and use autoreload you need to have node and npm available on your local machine.

* Install nodejs https://nodejs.org/en/
* NPM should be installed along with nodejs but if you need to install it https://www.npmjs.com/get-npm

In the root folder run

```
npm install
```
To install the node packages (they show up in a folder called node_modules in the root folder) and are not committed to the repo as they are development only requirements. npm start compiles all assets to the static assets folder at cms/static ...

---

## 4. <a name="#runapp"></a> Run the application

Do this only if you are using the [virtual environment](#virtual-environment). If you used the [docker container](#docker-container) install method these commands will be run automatically.

### Migrate the database. 

Run ...
```
python manage.py migrate
```

### Create a superuser login for the cms admin. 

Run ...
```
python manage.py createsuperuser
```
*** admin access is at http://localhost:3000/admin ***

You need to run 2 applications. One for the Wagtail app and the other for the frontend assets.

From one terminal and with the virtual environment activated from [virtual environment](#virtual-environment) and form the root folder run ...

```
python manage.py runserver 0:8000
```

Then from a second terminal run ...
```
npm start
```

This will start up the node process. You will see the progress in the terminal. The process needs to be left running. 

### Go to http://localhost:3000 to see the site. 

Using this url will make use of the auto reload feature and generally is better to use to avoid frontend assets been cached and showing old styling.

There's also http://localhost:8000 which can be used. It's the port used by the Django development server.

# Troubleshooting

If you are struggling to build the app (setup method 2) try starting your virtual environment from scratch. 
Run `pipenv --rm` to remove the virtual environment. Then delete `Pipfile` and `Pipfile.lock`.
  
Running `pipenv install -r requirements.dev` will then build a fresh virtual environment.

If you encounter problems with database migrations, remove your virtual environment as above, plus delete `db.sqlite3`. 
Then rebuild and re-run migrations as before.

TODO: How to upgrade sqlite3 version with python 3.8

# Importer App

The import app is located at /importer

It's a range of django management scripts that need to be run to import all the wordpress website data from Scrapy https://nhsei-scrapy.rkh.co.uk

## View the  <a href="https://github.com/rkhleics/nhs-ei.website/tree/main/docs/importer_app.md">Importer Guide</a>

The scripts in the importer guide need to be run for both install methods. 

Before the data is imported the development site you see will contain no pages other than the home page which will be blank at this stage.

# Application Guide

At it core this is a Wagtail app. Wagtail is a package built on the Django framework.

- [Wagtail Developer Documentation](https://docs.wagtail.io/en/v2.10.2/) for the version currently in production
- [Django Developer Docs](https://docs.djangoproject.com/en/3.1/) for the version currently in production and specified by Wagtail 2.10.2

View the [Application Guide](docs/application.md)

---

# Developer Testing
There are tests in place for each app in the cms (/cms/[appname]). The tests are inside the tests.py files.

Testing is functional tests at the moment. E.g. using the known test data imported check that each test page renders and the content from blocks is rendered as expected.

The following page types (models) are tested
- HomePage (cms/home/models.py)
- PublicationIndexPage and Publication (cms/publications/models.py)
- AtlasCaseStudyIndexPage and AtlasCaseStudy (cms/atlascasestudies/models.py)
- BlogIndexPage and Blog (cms/blog/models.py)
- PostIndexPage and Post (cms/posts/models.py)
- BasePage and ComponentsPage (cms/pages/models.py)

To run the tests you should prepare both the database and media files.

Move to the `fixtures` folder and run
```
./copy_media.sh
```

Then from the `project root` run
```
python manage.py loaddata fixtures/testdata.json
```

After loading testdata.json you will see sample pages available in the frontend and admin area.

A superuser login is created. Username: `admin` with password: `password123` which you can use at `http://localhost:8000/admin`

---

Making new testdata if you change the pages that are been tested and your test are been changed

### 1. Open a python shell thats aware of django
Wagtail pre renders all images and we need to remove them, we don't want them to be included in the test data. The original images will stay in place. When the page is next viewed new renders will be created from the originals. Testing doesn't test for the actual image used, just the presence of the image tag in the correct place in the HTML
```
python manage.py shell
```
Then run the flowing commands
```
from wagtail.images.models import Rendition
```
and 
```
Rendition.objects.all().delete()
```
You can close the shell now with quit()

### 2. Copy the project root media folder (/media)

Copy the media folder from your project root and replace the one in /fixtures

Now the media folder is a fixture that will represent the data when `./dumpdata.sh` is run next

### 3. Create a new testdata.json file

From the `fixtures` folder run
```
./dumpdata.sh > testdata.json
```
Now the data for all the pages in your development project has been written to `testdata.json` which you can later load again.