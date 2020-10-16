# NHS-EI Website

NHS-EI Website: Wagtail CMS contains the code to get a basic site up and runing with asset compilation using gulp.

## How to install

### 1. Clone this repository

https://github.com/rkhleics/nhs-ei.website

# DEVELOPMENT

### Set up and activate a virtual environment

Use any method you like best

### Install python dependancies

```
pip install -r requirements/dev.txt

python manange.py migrate

python manage.py createsuperuser

python manage.py runserver
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

# NOTES

Has prototype added in https://github.com/rkhleics/nhs-ei.website to achieve running as a development package

### Can Be Removed In The Future

---

cms/urls.py

provides the urls to be able to view the current static prototype pages

```
# views to test static pages
    urlpatterns += [
        path('nav-prototype', TemplateView.as_view(
            template_name='prototype_pages/nav_prototype.html'),
            name='nav-prototype'),
        path('search-results-prototype', TemplateView.as_view(
            template_name='prototype_pages/search_results_prototype.html'),
            name='search-prototype'),
        path('content-page-prototype', TemplateView.as_view(
            template_name='prototype_pages/content_page_prototype.html'),
            name='content-prototype'),
    ]
```

---

static prototype templates

    templates/prototype_pages/*
    templates/prototype_pages/content_page_prototype.html
    templates/prototype_pages/nav_prototype.html
    templates/prototype_pages/search_results_prototype.html

reworked to enable django template parsing
