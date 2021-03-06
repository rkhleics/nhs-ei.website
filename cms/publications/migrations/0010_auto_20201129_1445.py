# Generated by Django 3.1.2 on 2020-11-29 14:45

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0009_publication_component_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='documents',
            field=wagtail.core.fields.StreamField([('document_group', wagtail.core.blocks.StreamBlock([('document', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.RichTextBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock()), ('summary', wagtail.core.blocks.RichTextBlock(required=False))])), ('document_link', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.RichTextBlock(required=False)), ('external_url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('summary', wagtail.core.blocks.RichTextBlock(required=False))])), ('document_embed', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.RichTextBlock(required=False)), ('html', wagtail.core.blocks.RawHTMLBlock())])), ('free_text', wagtail.core.blocks.RichTextBlock())], group='Custom')), ('jump_menu', wagtail.core.blocks.StructBlock([('menu', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('menu_id', wagtail.core.blocks.CharBlock())])))], group='Custom')), ('named_anchor', wagtail.core.blocks.StructBlock([('anchor_id', wagtail.core.blocks.CharBlock()), ('heading', wagtail.core.blocks.CharBlock(required=False))], group='Custom'))], blank=True),
        ),
    ]
