from django.conf import settings
from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from wagtail.wagtailsnippets import urls
from wagtail.wagtailsnippets.permissions import user_can_edit_snippets
from wagtail.wagtailsnippets.models import get_snippet_content_types


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^snippets/', include(urls)),
    ]


class SnippetsMenuItem(MenuItem):
    def is_shown(self, request):
        return user_can_edit_snippets(request.user)

@hooks.register('register_admin_menu_item')
def register_snippets_menu_item():
    menu_items = []
    i = 0

    for content_type in get_snippet_content_types():
        verbose_name = content_type.model_class()._meta.verbose_name
        verbose_name = verbose_name[0:1].upper() + verbose_name[1:]
        menu_items.append(SnippetsMenuItem(verbose_name, urlresolvers.reverse('wagtailsnippets_list', args=[content_type.app_label, content_type.model]), classnames='icon icon-snippet', order=500 - i))
        i += 1

    return menu_items
    # return SnippetsMenuItem(_('Snippets'), urlresolvers.reverse('wagtailsnippets_index'), classnames='icon icon-snippet', order=500)


@hooks.register('insert_editor_js')
def editor_js():
    return format_html("""
            <script src="{0}{1}"></script>
            <script>window.chooserUrls.snippetChooser = '{2}';</script>
        """,
        settings.STATIC_URL,
        'wagtailsnippets/js/snippet-chooser.js',
        urlresolvers.reverse('wagtailsnippets_choose_generic')
    )


@hooks.register('register_permissions')
def register_permissions():
    snippet_content_types = get_snippet_content_types()
    snippet_permissions = Permission.objects.filter(content_type__in=snippet_content_types)
    return snippet_permissions
