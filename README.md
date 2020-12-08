# NHSE/I: Wagtail Test

This is used to test our IMPORTER app inside a wagtail instance and is were we are collecting the data from SCRAPY and importing it into a Wagtail instance.

We expect this app to show us the result of imporing pages, categories, posts and blog  and give us a chance to test out theories etc. It's an ongoing project that will likely chnage many times before production use as we discover data that needs conversion to a more suitable format to Wagtail import.

## Running the scripts

# Importing

The data is collected from https://nhsei-scrapy.rkh.co.uk/api/ 

```
Collect All Data    | python manage.py runimport all
Build The Site      | python manage.py runimport build
Fix some stuff      | python manage.py runimport fixes
Make some stuff     | python manage.py runimport makes
Make docuemnts      | python manage.py runimport documents
```

Skipping importing media in its own script, it's too buggy just now. So any media needed for pages or publicaitons gets pulled in as required for now.

Should you wnat to run the scripts individually then look at the scripts run in importer > management > commands > runimport.py

Last minute code snippets.

Analytics, for core settings when in place

```
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FBFNP91TN9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
 
  gtag('config', 'G-FBFNP91TN9');
</script>
```

# Deleting

```
1. Delete All  | python manage.py delete_all
```

Delete All runs through each of the delete commands in order which you can run separatly if need be.

At present delete_all as well as the import actions cause Wagtail to generate history for the site. It's a new feature in Wagtail in the latest version. This table gets very large and we don't need that data going forward. Maybe the imports and deletes can be set to not save history? For now in dev im just starting over with a fresh database every now and then.

But only if you are developing the app. It's nice to have a snapshot at this point so you can move back to it if things go wrong testing scripts etc. We're working with 7500+ pages plus the other tables at this point and I found the dumpdata command to be cumbersome. As I'm using sqlite3 for the DB I make a copy to a fixtures folder which can be quicky restored if needed. Infact i do this before runing the scripts below and again after :)

In fixtures i'll have copies of db.sqlite3 as I move through the stages when running indiviual imports so I can restore to an import/processing point.
