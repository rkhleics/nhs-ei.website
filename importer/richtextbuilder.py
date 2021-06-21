from os import PRIO_USER, unlink
import requests
import re
import sys
import logging
from io import BytesIO
from django.core.files import File
from bs4 import BeautifulSoup
from cms.pages.models import BasePage, ComponentsPage
from cms.posts.models import Post
from cms.blogs.models import Blog
from cms.publications.models import Publication
from cms.atlascasestudies.models import AtlasCaseStudy
from wagtail.core.models import Page
from wagtail.documents.models import Document
from wagtail.images.models import Image
from wagtail.core.models import Collection
from .httpcache import session

logger = logging.getLogger("importer")
TEST_CONTENT = """
<h2>Tips and examples</h2>
<p>
Our <a href="https://www.england.nhs.uk/fft/friends-and-family-test-development-project-2018-19/case-studies/">
case studies</a> provide examples of the work of some providers to make the FFT inclusive.</p>
<ul>
<li id="stacking-context-main">&nbsp;&nbsp;
<a href="https://www.england.nhs.uk/wp-content/uploads/2016/01/fft-dashboard-dec15.xlsx">FFT Dashboard</a>
</li>
</ul>
<ul>
<li><a href="https://www.england.nhs.uk/wp-content/uploads/2014/10/fft-audio-prom.mp3">Audio promotion</a> – This is a 30-second audio file with voice over and background music to promote the use of the FFT. You can download it for use as you wish, on websites, hospital radio and so on.</li>
<li><a href="https://www.england.nhs.uk/wp-content/uploads/2016/03/fft-ppt-1slide.ppt">Single slide promo for FFT</a> – This Powerpoint slide is a prompt to patients to take part in the FFT and to find out more about it.&nbsp; It is suitable for most healthcare settings.</li>
</ul>
<p>In addition to the support outlined in the support package, the&nbsp;
<a class="pdf-link" href="https://www.england.nhs.uk/wp-content/uploads/2016/04/vanguard-funding.pdf">
50 vanguards were allocated total funding of almost £133 million in 2015/16</a>,&nbsp;
<a class="pdf-link" href="https://www.england.nhs.uk/wp-content/uploads/2016/05/vanguard-allocs.pdf">
£112 million in 2016/17</a>&nbsp;and&nbsp;<a href="https://www.england.nhs.uk/a-focus-on-staff-health-and-wellbeing/">
£101 million for 2017/18</a>.</p>
"""

# some urls dont need to be rewritten as they are
# not in scope in this project and will remain
# absolute when live although they are same site just now
SKIP_ANCHOR_URLS = [
    "/east-of-england/",
    "/london/",
    "/midlands/",
    "/north-east-yorkshire/",
    "/north-west/",
    "/south-east/",
    "/south/",
    "/statistics/statistical-work-areas/rtt-waiting-times/rtt-guidance/",
]

# these pages are 404 in live site
SKIP_ANCHOR_URLS += ["/fft/fft-guidance/revised-fft-guidance/"]

# not sure how to manage these yet
SKIP_ANCHOR_URLS += ["/patientsafety/wp-content"]

MEDIA_FILE_EXTENSIONS = {
    "images": ["jpg", "gif", "png"],
    "documents": ["doc", "pdf", "xlsx", "docx"],
}

IGNORE_CONTENT_WITH = ["form"]


class RichTextBuilder:

    """
    The purpose of this class is to sort out what
    blocks may be needed to represent the wysiwyg content
    from wordpress. There's wysiwyg content in both content fields
    and custom fields.
    Internal Page Links, Internal Media Links, Internal Image Sources
    """

    # <a id="3" linktype="page">Contact us</a> PAGE
    # <a id="1" linktype="document">link</a> DOCUMENT
    # <embed embedtype="image" id="10" alt="A pied wagtail" format="left" /> IMAGE

    def __init__(self, url_map, html_content=None):
        self.url_map_keys = url_map.keys()
        self.url_map = url_map
        self.change_links = []
        self.html_content = html_content

    def extract_img(self, content=None, page=None):
        soup = BeautifulSoup(content, features="html5lib")
        images = soup.find_all("img")
        print("images")
        print(images)
        sys.exit()

    def extract_links(self, content=None, page=None):
        # BS4 to get a handle on all the anchor links
        if not content:
            html_content = self.html_content
        else:
            html_content = content
        soup = BeautifulSoup(html_content, features="html5lib")

        links = soup.find_all(
            "a",
            href=re.compile(
                r"^(http://|https://)(www.england.nhs.uk/|www.england.nhs.uk)"
            ),
        )

        has_form = soup.find_all("form")

        if not has_form:

            for link in links:
                # get the href from anchor
                # these are the links in the wysiwyg content (absolute to old site)
                # /publication/daily-submission-of-flu-vaccination-data-for-healthcare-workers-letter/
                page_path = "/" + "/".join(link["href"].split("/")[3:])
                self.prepare_links(link, page_path, page)

    """
    how the whole site url paths are cached for the lookup
    [
        map[page.url] = {
            'id': page.id,
            'slug': page.slug,
            'title': page.title,
        },
        {...}
    ]
    '/publication/nhs-england-improvement/the-okay-to-stay-programme/': {
        'id': 9782, 
        'slug': 'the-okay-to-stay-programme', 
        'title': 'The ‘Okay to Stay’ programme'
    },
    
    on a quick interupted runimport mediafiles this is one of the documents
    documents/LeDeR-death-data-nov-27-2020-easy-read.pdf path
    d=Document.objects.get(file='documents/LeDeR-death-data-nov-27-2020-easy-read.pdf')

    and this is one of the images
    original_images/maysa-alsharif.jpg
    i=Image.objects.get(file='original_images/maysa-alsharif.jpg')
    """

    def prepare_links(self, link, page_path, page):

        path_list = page_path.split("/")  # a list of path segments
        # first is always '' so lets remove it
        del path_list[0]
        if not path_list[-1]:  # and remove the past one if none
            del path_list[-1]

        page_path = "/" + "/".join(path_list) + "/"  # a string of the path

        # some links are anchors
        # is_anchor_link = False
        # if '#' in path_list[-1]:
        #     is_anchor_link = True

        page_path_live = "https://www.england.nhs.uk" + page_path
        # print(page_path)

        home_page = Page.objects.filter(title="Home")[0]

        if not path_list:
            # home page
            page_link = self.make_page_link(link.text, home_page.id, home_page.title)
            self.change_links.append([link, page_link])

        elif (
            path_list
            and path_list[0] == "publication"
            or len(path_list) >= 2
            and path_list[1] == "publication"
        ):
            # find source url for publication ours are all in sub sites but links are not
            try:
                publication = Publication.objects.get(wp_link=page_path_live)
                page_link = self.make_page_link(
                    link.text, publication.id, publication.title
                )
                self.change_links.append([link, page_link])
            except:
                logger.warn(
                    "Stream field URL error (publication), %s | %s | %s",
                    link,
                    page_path,
                    page,
                )

        elif path_list and path_list[0] == "news":
            # find source url for news ours are all in sub sites
            try:
                post = Post.objects.get(wp_link=page_path_live)
                page_link = self.make_page_link(link.text, post.id, post.title)
                self.change_links.append([link, page_link])
            except:
                logger.warn(
                    "Stream field URL error (news), %s | %s | %s", link, page_path, page
                )

        elif path_list and path_list[0] == "blog":
            # find source url for blogs
            # print(page_path_live)
            try:
                blog = Blog.objects.get(wp_link=page_path_live)
                page_link = self.make_page_link(link.text, blog.id, blog.title)
                self.change_links.append([link, page_link])
            except:
                logger.warn(
                    "Stream field URL error (blog), %s | %s | %s", link, page_path, page
                )

        elif (
            path_list
            and path_list[0] == "wp-content"
            or len(path_list) >= 2
            and path_list[1] == "wp-content"
        ):  # becuse sometimes they are subsite links
            # a file link these arnt in the self.urls
            """problem here is we cant link to a page within a document using #page=2"""
            if "#" in path_list[-1]:
                page_path = page_path.split("#")[0]
            document_id = None
            file = "documents/" + path_list[-1]
            # print(file)

            try:
                document = Document.objects.get(file=file)
                document_id = document.id

            except Document.DoesNotExist:
                logger.warn("Media %s not found, linked from %s", page_path, page)
                collection_root = Collection.get_first_root_node()
                remote_file = session.get(page_path_live)
                media_file = File(BytesIO(remote_file.content), name=path_list[-1])
                file = Document(
                    title=path_list[-1], file=media_file, collection=collection_root
                )
                file.save()
                pass

            if document_id:
                document_link = self.make_document_link(
                    link.text, document_id, path_list[-1]
                )
                self.change_links.append([link, document_link])

        elif page_path in self.url_map_keys and page_path not in SKIP_ANCHOR_URLS:
            page_link = self.make_page_link(
                link.text,
                self.url_map[page_path]["id"],
                self.url_map[page_path]["title"],
            )
            self.change_links.append([link, page_link])

        else:
            # print('using live')
            response = session.get("https://www.england.nhs.uk" + page_path)
            url = ""
            is_post = False
            try:
                response.raise_for_status()
            except:
                logging.warn(
                    "HTTP Error %s when scraping %s", response.status_code, response.url
                )
            if response:
                url = response.url.split("/")
                del url[-1]
                del url[:3]
                # some urls have links to news items that start 2010/09 that needs to removed to find the url
                if (
                    len(url) >= 3
                    and url[0].isdigit()
                    and url[1].isdigit()
                    and not url[2].isdigit()
                ):  # is post
                    try:
                        page = Post.objects.get(wp_link=response.url)
                        id = page.id
                        title = page.title
                        page_link = self.make_page_link(link.text, id, title)
                        self.change_links.append([link, page_link])
                    except Post.DoesNotExist:
                        pass
                elif (
                    path_list[0].isdigit()
                    and path_list[1].isdigit()
                    and path_list[2].isdigit()
                ):
                    try:
                        blog = Blog.objects.get(wp_link=response.url)
                        id = blog.id
                        title = blog.title
                        page_link = self.make_page_link(link.text, id, title)
                        self.change_links.append([link, page_link])
                    except Blog.DoesNotExist:
                        pass
                else:  # is page
                    # print('could be a page')
                    actual_url = "/" + "/".join(url) + "/"  # a string of the path
                    if actual_url in self.url_map_keys:
                        id = self.url_map[actual_url]["id"]
                        title = self.url_map[actual_url]["title"]
                        page_link = self.make_page_link(link.text, id, title)
                        self.change_links.append([link, page_link])
                    else:
                        print("leaving the link alone")

            else:
                logger.warn("Stream fields URL error (???), %s, %s", page_path, page)

    def make_page_link(self, text, page_id, title):
        return (
            '<a id="{}" linktype="page" class="internal-link" title="{}">{}</a>'.format(
                page_id, title, text
            )
        )

    def make_document_link(self, text, document_id, title):
        return '<a id="{}" linktype="document" class="pdf-link" title="Download a copy of the {}">{}</a>'.format(
            document_id, title, text
        )

    def make_image_embed(self, image_id, image_alt, image_format):
        return '<embed embedtype="image" id="{}" alt="{}" format="{}" />'.format(
            image_id, image_alt, image_format
        )
