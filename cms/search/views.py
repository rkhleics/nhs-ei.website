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
    query = request.GET.get("query", None)
    """
    sample query
    ?
    query=nursing&
    order=pub_date_asc&
    content_type=pages&
    date_from=2020-11-01&
    date_to=2020-11-29
    """

    page = request.GET.get("page", 1)

    """
    possible ordering
    'first_published_at'
    '-first_published_at'
    'latest_revision_created_at'
    '-latest_revision_created_at'
    """
    search_ordering = "-first_published_at"

    if request.GET.get("order"):
        search_ordering = request.GET.get("order")

    search_type = ""
    search_results_count = None
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    # Search
    if query:
        if request.GET.get("content_type") == "news":
            """searching news only"""
            if request.GET.get("date_from") and request.GET.get("date_to"):
                objs = (
                    Post.objects.live()
                    .order_by(search_ordering)
                    .filter(
                        first_published_at__range=[
                            request.GET.get("date_from"),
                            request.GET.get("date_to"),
                        ]
                    )
                )
                search_results = objs.search(query)
                date_from = request.GET.get("date_from")
                date_to = request.GET.get("date_to")
            else:
                search_results = (
                    Post.objects.live().order_by(search_ordering).search(query)
                )

            search_type = "news"

        elif request.GET.get("content_type") == "blogs":
            """searching blogs only"""
            if request.GET.get("date_from") and request.GET.get("date_to"):
                objs = (
                    Blog.objects.live()
                    .order_by(search_ordering)
                    .filter(
                        first_published_at__range=[
                            request.GET.get("date_from"),
                            request.GET.get("date_to"),
                        ]
                    )
                )
                search_results = objs.search(query)
                date_from = request.GET.get("date_from")
                date_to = request.GET.get("date_to")
            else:
                search_results = (
                    Blog.objects.live().order_by(search_ordering).search(query)
                )

            search_type = "blogs"

        elif request.GET.get("content_type") == "pages":
            """searching pages only"""
            if request.GET.get("date_from") and request.GET.get("date_to"):
                objs = (
                    BasePage.objects.live()
                    .order_by(search_ordering)
                    .filter(
                        first_published_at__range=[
                            request.GET.get("date_from"),
                            request.GET.get("date_to"),
                        ]
                    )
                )
                search_results = objs.search(query)
                date_from = request.GET.get("date_from")
                date_to = request.GET.get("date_to")
            else:
                search_results = (
                    BasePage.objects.live().order_by(search_ordering).search(query)
                )

            search_type = "pages"

        elif request.GET.get("content_type") == "publications":
            """searching publications only"""
            if request.GET.get("date_from") and request.GET.get("date_to"):
                objs = (
                    Publication.objects.live()
                    .order_by(search_ordering)
                    .filter(
                        first_published_at__range=[
                            request.GET.get("date_from"),
                            request.GET.get("date_to"),
                        ]
                    )
                )
                search_results = objs.search(query)
                date_from = request.GET.get("date_from")
                date_to = request.GET.get("date_to")
            else:
                search_results = (
                    Publication.objects.live().order_by(search_ordering).search(query)
                )

            search_type = "publications"

        else:
            if request.GET.get("date_from") and request.GET.get("date_to"):
                objs = (
                    Page.objects.live()
                    .order_by(search_ordering)
                    .filter(
                        first_published_at__range=[
                            request.GET.get("date_from"),
                            request.GET.get("date_to"),
                        ]
                    )
                )
                search_results = objs.search(query)
                date_from = request.GET.get("date_from")
                date_to = request.GET.get("date_to")
            else:
                search_results = (
                    Page.objects.live().order_by(search_ordering).search(query)
                )

        # if request.GET.get('date_from') and request.GET.get('date_to'):
        #     search_results.filter(first_published_at__range=[request.GET.get('date_from'), request.GET.get('date_to')])

        search_results_count = search_results.count()

        query = Query.get(query)
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

    search_params = "&query={}&order={}&content_type={}&date_from={}&date_to={}".format(
        query, search_ordering, search_type, date_from, date_to
    )

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "query": query,
            "search_results": search_results,
            "results_count": search_results_count,
            "page": page,
            "search_params": search_params,
            "content_type": search_type,
            "order": search_ordering,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
