"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'progile.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.AppList(
            _('Publications'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('system.core.models.*',),
            exclude=(
                'system.core.models.SocialNetwork',
                'system.core.models.Contact',
                'system.core.models.Address',
                'system.core.models.About',
                'system.core.models.Role',
                'system.core.models.Member',
                'system.core.models.Author',
                'system.core.models.Photographer',
                'system.core.models.Editorial',
                'system.core.models.Discipline',
            ),

        ))

        self.children.append(modules.Group(
            _('Administration'),
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    _('General configurations'),
                    collapsible=False,
                    column=1,
                    models=(
                        'system.core.models.SocialNetwork',
                        'system.core.models.Contact',
                        'system.core.models.Address',
                        'system.core.models.About',
                        'system.core.models.Role',
                        'system.core.models.Member',
                        'system.core.models.Author',
                        'system.core.models.Photographer',
                    ),
                ),
                modules.AppList(
                    _('Publication configurations'),
                    collapsible=False,
                    column=1,
                    models=(
                        'system.core.models.Editorial',
                        'system.core.models.Discipline',
                    ),
                ),
                modules.AppList(
                    _('Users'),
                    column=1,
                    collapsible=False,
                    models=('django.contrib.*',),
                ),
            ]
        ))

        self.children.append(modules.LinkList(
            _('Pages'),
            column=2,
            children=[
                {
                    'title': _('progile GUI'),
                    'url': '/home/',
                    'external': False,
                },
                # {
                #     'title': _('Grappelli Documentation'),
                #     'url': 'http://packages.python.org/django-grappelli/',
                #     'external': True,
                # },
                # {
                #     'title': _('Grappelli Google-Code'),
                #     'url': 'http://code.google.com/p/django-grappelli/',
                #     'external': True,
                # },
            ]
        ))

        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            column=2,
            collapsible=False,
            limit=5,
        ))



