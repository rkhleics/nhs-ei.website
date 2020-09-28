# NHS-EI Website

NHS-EI Website:  Wagtail CMS contains the code to get a basic site up and runing with asset compilation using gulp.

## How to install

### 1. Clone this repository

https://github.com/rkhleics/nhs-ei.website

# DEVELOPMENT

### Set up and activate a virtual environment

Use any method you like best

### Install python dependancies

```
pip install -r requirements/dev.txt

./manange.py migrate

./manange.py createsuperuser

./manage.py runserver
```
Keep the above running in it's own terminal

### Install NPM dependancies

```
npm install
```

### Run NPM

development with reload
```
npm start
```

compile for production
```
npm run build
```