from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsearch import index

class QAIndexPage(Page):
    intro = RichTextField()
    
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(QAIndexPage, self).get_context(request)
        qa_pages = self.get_children().live()
        context['qa_pages'] = qa_pages
        return context

class QAPage(Page):
    date = models.DateField("Post date")
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
    ]
