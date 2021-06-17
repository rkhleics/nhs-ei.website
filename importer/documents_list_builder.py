from os import unlink
import re
from bs4 import BeautifulSoup
from cms.pages.models import BasePage, ComponentsPage
from cms.posts.models import Post
from cms.blogs.models import Blog
from cms.publications.models import Publication
from cms.atlascasestudies.models import AtlasCaseStudy

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
# not in scope
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

MEDIA_FILE_EXTENSIONS = {
    "images": ["jpg", "gif", "png"],
    "documents": ["doc", "pdf", "xlsx", "docx"],
}


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

    def __init__(self, all_pages=None, html_content=""):
        # theres are log files to record url problems, clean it out first
        with open("log/parse_stream_fields_url_errors.txt", "w") as log:
            log.write("parse_stream_field missing urls\n")
        with open("log/parse_stream_fields_media_errors.txt", "a") as the_file:
            the_file.write("parse_stream_field missing media\n")
        self.html_content = TEST_CONTENT
        if not all_pages:
            self.urls = self.all_pages()
        else:
            self.urls = all_pages
        self.change_links = []

    def all_pages(self):
        models = [BasePage, ComponentsPage, Blog, Post, AtlasCaseStudy, Publication]
        url_ids = {}  # cached

        for model in models:
            pages = model.objects.all()
            for page in pages:
                url_ids[page.url] = page.id

        return url_ids

    def extract_links(self, content=None):
        # BS4 to get a handle on all the anchor links
        if not content:
            html_content = self.html_content
        else:
            html_content = content
        soup = BeautifulSoup(html_content, features="html5lib")

        links = soup.find_all("a", href=re.compile(r"^https://www.england.nhs.uk/"))

        for link in links:
            page_path = "/" + "/".join(link["href"].split("/")[3:])
            self.prepare_links(link, page_path)

    def prepare_links(self, link, page_path):
        path_list = page_path.split("/")
        if len(path_list[-1]):
            pass
            # with open('log/parse_stream_fields_media_errors.txt', 'a') as the_file:
            #     the_file.write('{}\n'.format(page_path))
            #     print('++++++missing media: {}'.format(page_path))
        else:  ############ GOT TO HERE just run ./manage.py parse_stream_fields
            if page_path in self.urls and page_path not in SKIP_ANCHOR_URLS:
                page_link = self.make_page_link(link.text, self.urls[page_path])
                self.change_links.append([link, page_link])
            else:
                with open("log/parse_stream_fields_url_errors.txt", "a") as the_file:
                    the_file.write("{}\n".format(page_path))
                print("++++++missing url: {}".format(page_path))
        # if self.urls[path]:
        #     self.change_links.append(self.urls[path]) ####### got to here

    def make_page_link(self, text, page_id):
        return '<a id="{}" linktype="page">{}</a>'.format(page_id, text)

    def make_document_link(self, text, document_id):
        return '<a id="{}" linktype="document">{}</a>'.format(document_id, text)

    def make_image_embed(self, text, image_id, image_alt, image_format):
        return '<embed embedtype="image" id="{}" alt="{}" format="{}" />'.format(
            image_id, image_alt, image_format
        )
