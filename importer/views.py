import csv
from nhsei_wagtail.publications.models import Publication
from nhsei_wagtail.atlascasestudies.models import AtlasCaseStudy
from urllib.parse import urlparse

from django.shortcuts import render
from django.http import HttpResponse

from wagtail.core.models import Page
from wagtail.images.models import Image
from wagtail.documents.models import Document
from nhsei_wagtail.pages.models import BasePage
from nhsei_wagtail.home.models import HomePage
from nhsei_wagtail.posts.models import Post
from nhsei_wagtail.blogs.models import Blog
from nhsei_wagtail.categories.models import Category, PublicationType, Region, Setting
# from nhsei_wagtail.tags.models import Tag

KNOWN_SLUG_PROBLEMS = {
    # 'sponsors': 'parent page 404',
    # 'webinars': 'parent page 404',
    # 'main-stages': 'parent page 404',
    # 'gallery': 'parent page 404',
    # 'speaker-highlights': 'parent page 404',
    # 'sub-groups': 'parent page 404',
    # 'videos': 'parent page 404',
    # 'why': 'is redirected',
    # 'get-involved-3': 'parent page is redirected',
    # 'framework': 'is redirected',
    # 'burden-reduction': 'parent page 404',
    # 'home-2': 'commissioning slug problem',
}

REDIRECT_SLUGS_FOUND = {
    # '/greener-nhs/': 'greenernhs',
    # '/sample-page/': 'aac',
    # '/nhs-rightcare/': 'nhsrightcare',
    # '/tbc/': 'non-executive-opportunities',
    # '/improvement-knowledge-hub/': 'improvement-hub',
    # '/nhs-england-and-nhs-improvement-corona-virus/': 'coronavirus',
}


def dashboard(request):
    # def get_context(self, request, *args, **kwargs):
    # context = super().get_context(request, *args, **kwargs)
    home_page = HomePage.objects.all()[0]  # quick and dirty

    # find homepage children with children
    top_pages = BasePage.objects.child_of(home_page)

    """to report on top pages that have no children"""

    top_pages_with_children = []
    for p in top_pages:
        children = p.get_children()
        if p.slug in KNOWN_SLUG_PROBLEMS.keys():
            p.known_slug_problem = KNOWN_SLUG_PROBLEMS[p.slug]
        if len(children) > 1:
            top_pages_with_children.append(p)

    context = {}
    context['top_pages_with_children'] = top_pages_with_children
    context['top_pages_with_children_count'] = len(top_pages_with_children)

    """ to report on top pages that have children """

    top_pages_without_children = []
    for p in top_pages:
        children = p.get_children()
        if p.slug in KNOWN_SLUG_PROBLEMS.keys():
            p.known_slug_problem = KNOWN_SLUG_PROBLEMS[p.slug]
        if not len(children):
            top_pages_without_children.append(p)

    """ top report on any page that has a different path wordpress vs Wagtail, this should be empty """

    all_base_pages = BasePage.objects.all()
    base_pages_path_errors = []
    first_segment_tracker = []
    for page in all_base_pages:
        # first_segment = urlparse(page.url).path.split('/')[1]
        # if not first_segment in first_segment_tracker:
        # first_segment_tracker.append(first_segment)
        self_url = page.url
        live_url = urlparse(page.wp_link).path
        message = ''
        path = '/' + self_url.split('/')[1]
        already_found = False
        if not self_url == live_url:
            # print(self_url)
            # print(live_url)
            if self_url in REDIRECT_SLUGS_FOUND.keys():
                message = REDIRECT_SLUGS_FOUND[self_url]
                # print('found')
            # page.slug
            # if live_url in REDIRECT_SLUGS_FOUND.keys():
            #     page.redirect_slug_problem = REDIRECT_SLUGS_FOUND[live_url]
            # if page.url.split('/')[1] in first_segment_tracker:
            #     already_found = True
            base_pages_path_errors.append({
                'title': page.title,
                'page_url': page.url,
                'message': message,
                'source': page.source,
                'found': already_found,
                'path': path,
                'live_url': live_url
            })
    # print(first_segment_tracker)

    context['url_errors'] = base_pages_path_errors
    context['url_errors_count'] = len(base_pages_path_errors)

    context['top_pages_without_children'] = top_pages_without_children
    context['top_pages_without_children_count'] = len(
        top_pages_without_children)

    context['post_pages_count'] = Post.objects.count()
    context['blog_pages_count'] = Blog.objects.count()
    context['total_pages_count'] = Page.objects.exclude(title='Root').count()
    context['atlas_case_studies_pages_count'] = AtlasCaseStudy.objects.count()
    context['publications_pages_count'] = Publication.objects.count()

    context['base_pages_count'] = BasePage.objects.count()
    context['top_pages'] = home_page.get_children()
    context['home_children_count'] = home_page.get_children().count()
    
    context['categories_count'] = Category.objects.count()
    context['settings_count'] = Setting.objects.count()
    context['regions_count'] = Region.objects.count()
    context['publication_types_count'] = PublicationType.objects.count()
    # context['images_count'] = Image.objects.count()
    # context['documents_count'] = Document.objects.count()

    return render(request, 'importer/dashboard.html', context)


def top_pages_with_children(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="top-pages-with-children.csv"'

    writer = csv.writer(response)
    writer.writerow(['Page', 'Path', 'Slug', 'ID'])

    home_page = HomePage.objects.all()[0]  # quick and dirty
    top_pages = BasePage.objects.child_of(home_page)

    for p in top_pages:
        children = p.get_children()

        if len(children) > 1:
            writer.writerow(
                [p.title, 'https://nhsei-wagtail.rkh.co.uk' + p.url, p.slug, p.id])

    return response


def top_pages_without_children(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="top-pages-without-children.csv"'

    writer = csv.writer(response)
    writer.writerow(['Page', 'Path', 'Slug', 'ID'])

    home_page = HomePage.objects.all()[0]  # quick and dirty
    top_pages = BasePage.objects.child_of(home_page)

    for p in top_pages:
        children = p.get_children()

        if not len(children):
            writer.writerow(
                [p.title, 'https://www.england.nhs.uk' + p.url, p.slug, p.id])

    return response


def url_errors(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="url-errors.csv"'

    writer = csv.writer(response)
    writer.writerow(['Page', 'Path', 'Slug', 'ID'])

    all_base_pages = BasePage.objects.all()
    base_pages_path_errors = []
    first_segment_tracker = []
    for page in all_base_pages:
        self_url = page.url
        live_url = urlparse(page.wp_link).path
        message = ''
        path = '/' + self_url.split('/')[1]
        already_found = False
        if not self_url == live_url:
            # print(self_url)
            # print(live_url)
            # if self_url in REDIRECT_SLUGS_FOUND.keys():
            #     message = REDIRECT_SLUGS_FOUND[self_url]
            # print('found')
            # page.slug
            # if live_url in REDIRECT_SLUGS_FOUND.keys():
            #     page.redirect_slug_problem = REDIRECT_SLUGS_FOUND[live_url]
            # if page.url.split('/')[1] in first_segment_tracker:
            #     already_found = True
            # base_pages_path_errors.append({
            #     'title': page.title,
            #     'page_url': page.url,
            #     'message': message,
            #     'source': page.source,
            #     'found': already_found,
            #     'path': path,
            #     'live_url': live_url
            # })

            writer.writerow(
                [page.title, 'https://www.england.nhs.uk' + page.url, page.slug, page.id, ])

    return response
