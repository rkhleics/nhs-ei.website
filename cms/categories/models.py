import sys
from django.core.checks import messages
from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError

"""CATEGORIES work with blogs and posts and across sub sites"""


class CategorySubSite(models.Model):
    title = models.CharField(max_length=100)
    """ coming across form wordpress need to keep for now"""
    source = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Category(models.Model):
    sub_site = models.ForeignKey(
        CategorySubSite,
        on_delete=models.PROTECT,
        null=True
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    """ coming across from wordpress need to keep for now"""
    wp_id = models.PositiveSmallIntegerField(null=True)
    source = models.CharField(null=True, max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    # prevent deleting a category if its in use
    # def delete(self, *args, **kwargs):
    #     Post = apps.get_model('posts.Post')
    #     posts_count = Post.objects.filter(
    #         post_category_relationship__category=self)

    #     Blog = apps.get_model('blogs.Blog')
    #     blogs_count = Blog.objects.filter(
    #         blog_category_relationship__category=self)

    #     if posts_count or blogs_count:
    #         raise ValidationError('1244')
    #     else:
    #         super().delete(*args, **kwargs)


"""PUBLICATION TYPES work with publications (document) and across sub sites"""


class PublicationTypeSubSite(models.Model):
    title = models.CharField(max_length=100)
    """ coming across form wordpress need to keep for now"""
    source = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class PublicationType(models.Model):
    sub_site = models.ForeignKey(
        PublicationTypeSubSite,
        on_delete=models.PROTECT,
        null=True
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    """ coming across from wordpress need to keep for now"""
    wp_id = models.PositiveSmallIntegerField(null=True)
    source = models.CharField(null=True, max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Publication Type'
        verbose_name_plural = 'Publication Types'

    def __str__(self):
        return self.name

    # prevent deleting a category if its in use
    # def delete(self, *args, **kwargs):
    #     Post = apps.get_model('posts.Post')
    #     posts_count = Post.objects.filter(post_category_relationship__category=self)

    #     Blog = apps.get_model('blogs.Blog')
    #     blogs_count = Blog.objects.filter(blog_category_relationship__category=self)

    #     if posts_count or blogs_count:
    #         raise ValidationError('1244')
    #     else:
    #         super().delete(*args, **kwargs)


class Setting(models.Model):
    # sub_site = models.ForeignKey(
    #     CategorySubSite,
    #     on_delete=models.PROTECT,
    #     null=True
    # )
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    """ coming across from wordpress need to keep for now"""
    wp_id = models.PositiveSmallIntegerField(null=True)
    # source = models.CharField(null=True, max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.name


class Region(models.Model):
    # sub_site = models.ForeignKey(
    #     CategorySubSite,
    #     on_delete=models.PROTECT,
    #     null=True
    # )
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    """ coming across from wordpress need to keep for now"""
    wp_id = models.PositiveSmallIntegerField(null=True)
    # source = models.CharField(null=True, max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name