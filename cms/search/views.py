from cms.atlascasestudies.models import AtlasCaseStudy
from cms.publications.models import Publication
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.core.models import Page
from wagtail.search.models import Query

from cms.posts.models import Post
from cms.blogs.models import Blog
from cms.pages.models import BasePage


def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)
    search_ordering = 'first_published_at'

    search_params = ''
    search_type = ''
    search_results_count = None

    # Search
    if search_query:
        if request.GET.get('type') == 'news':
            search_results = Post.objects.live().order_by(search_ordering).search(search_query)
            search_params = '&type=news'
            search_type = 'News'

        elif request.GET.get('type') == 'blogs':
            search_results = Blog.objects.live().order_by(search_ordering).search(search_query)
            search_params = '&type=blogs'
            search_type = 'Blogs'

        elif request.GET.get('type') == 'pages':
            search_results = BasePage.objects.live().order_by(search_ordering).search(search_query)
            search_params = '&type=pages'
            search_type = 'Pages'

        elif request.GET.get('type') == 'publications':
            search_results = Publication.objects.live().order_by(search_ordering).search(search_query)
            search_params = '&type=publications'
            search_type = 'Publications'

        elif request.GET.get('type') == 'atlas_case_studies':
            search_results = AtlasCaseStudy.objects.live().order_by(search_ordering).search(search_query)
            search_params = '&type=atlas_case_studies'
            search_type = 'Atlas Case Studies'

        else:
            search_results = Page.objects.live().order_by(search_ordering).search(search_query)

        search_results_count = search_results.count()

        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
        'search_params': search_params,
        'search_type': search_type,
        'results_count': search_results_count
    })
