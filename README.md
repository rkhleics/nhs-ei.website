# NHSE/I: Wagtail Test

This is used to test our IMPORTER app inside a wagtail instance and is were we are collecting the data from SCRAPY and importing it into a Wagtail instance.

We expect this app to show us the result of imporing pages, categories, posts and blog  and give us a chance to test out theories etc. It's an ongoing project that will likely chnage many times before production use as we discover data that needs conversion to a more suitable format to Wagtail import.

## Running the scripts

# Importing

The data is collected from https://nhsei-scrapy.rkh.co.uk/api/ 

```
Collect All Data    | python manage.py runimport all
Build The Site      | python manage.py runimport build
```
Should you wnat to run the scripts individually then look at the scripts run in importer > management > commands > runimport.py

```
# the whole lot in specific order

# BEFORE ALL OTHERS as related keys exists
import_categories(get_api_url('categories'))
import_publication_types(get_api_url('publication_types'))
import_settings(get_api_url('settings'))
import_regions(get_api_url('regions'))
# END BEFORE ALL OTHERS

# pages needs to run here because later commands
# create pages that prevent this script from running becuse of slug duplication

import_pages(get_api_url('pages'))
import_posts(get_api_url('posts'))
import_blogs(get_api_url('blogs'))
import_publications(get_api_url('publications'))
import_atlas_case_studies(get_api_url('atlas_case_studies'))
```

```
call_command('page_mover')
call_command('fix_slugs')
call_command('swap_page_types')
call_command('fix_component_page_slugs')
call_command('fix_landing_page_slugs')
call_command('swap_blogs_page')
call_command('parse_stream_fields')
call_command('parse_stream_fields_component_pages') # here we have url issue
# TODO python manage.py parse_stream_fields_landing_pages  we need the blog autors may be do other stuff here first???
call_command('make_top_pages')
call_command('make_alert_banner')
call_command('make_home_page')
call_command('make_footer_links')
```
# Deleting

```
1. Delete All  | python manage.py delete_all
```

Delete All runs through each of the delete commands in order which you can run separatly if need be.

At present delete_all as well as the import actions cause Wagtail to generate history for the site. It's a new feature in Wagtail in the latest version. This table gets very large and we don't need that data going forward. Maybe the imports and deletes can be set to not save history? For now in dev im just starting over with a fresh database every now and then.

But only if you are developing the app. It's nice to have a snapshot at this point so you can move back to it if things go wrong testing scripts etc. We're working with 7500+ pages plus the other tables at this point and I found the dumpdata command to be cumbersome. As I'm using sqlite3 for the DB I make a copy to a fixtures folder which can be quicky restored if needed. Infact i do this before runing the scripts below and again after :)

In fixtures i'll have copies of db.sqlite3 as I move through the stages when running indiviual imports so I can restore to an import/processing point.