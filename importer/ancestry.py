from cms.pages.models import BasePage
from cms.home.models import Page


class Ancestry:
    """work out the final ancestor of a page from meta data in a model"""

    def __init__(self, page):
        self.page = page
        # print(self.page, self.page.id, self.page.wp_id)
        self.parent_type = self.get_parent_type()

    def get_parent_type(self):
        # was seeing errors but not sure why???
        """TypeError: '>' not supported between instances of 'NoneType' and 'int'"""
        # self.page.parent it the wp_id so that explains why sometimes is None
        if self.page.parent is not None:
            if self.page.parent > 0:
                return "valid"
            elif self.page.parent == 0 and self.page.real_parent > 0:
                return "faux"
            elif self.page.parent == 0 and self.page.real_parent == -1:
                return "fixtop"
            else:
                return "top"

    def get_parent(self):
        # there's a real_parent property available from SCRAPY
        possible_parents = self.count_possible_parents()
        if possible_parents == 1 and self.parent_type == "valid":  # OK
            return BasePage.objects.get(wp_id=self.page.parent).id
        elif possible_parents == 1 and self.parent_type == "faux":  # filter for source
            return BasePage.objects.get(wp_id=self.page.real_parent).id
        elif possible_parents > 1 and self.parent_type == "faux":  # filter for source
            return BasePage.objects.get(
                source=self.page.source, wp_id=self.page.real_parent
            ).id
        elif possible_parents > 1 and self.parent_type == "valid":  # filter for source
            return BasePage.objects.get(
                source=self.page.source, wp_id=self.page.parent
            ).id

    def count_possible_parents(self):
        if self.parent_type == "valid":
            return BasePage.objects.filter(wp_id=self.page.parent).count()
        if self.parent_type == "faux":
            return BasePage.objects.filter(wp_id=self.page.real_parent).count()
        if self.parent_type == "fixtop":
            return -1
        if self.parent_type == "top":
            return 0
