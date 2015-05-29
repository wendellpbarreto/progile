#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from .views import View

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/home/')),

    url(r'^(?P<slug>\w+)/$', View.as_view(), name='view',),
)
