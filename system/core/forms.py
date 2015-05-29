#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from redactor.widgets import RedactorEditor
from django.db import models

from .models import *

# class AboutAdminForm(forms.ModelForm):
#     class Meta:
#         model = About
#         widgets = {
#             "body": RedactorEditor(),
#         }

# class MemberAdminForm(forms.ModelForm):
#     class Meta:
#         model = Member
#         widgets = {
#             "about": RedactorEditor(),
#         }

# class AuthorAdminForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         widgets = {
#             "about": RedactorEditor(),
#         }

# class PhotographerAdminForm(forms.ModelForm):
#     class Meta:
#         model = Photographer
#         widgets = {
#             "about": RedactorEditor(),
#         }

# class NoticeAdminForm(forms.ModelForm):
#     class Meta:
#         model = Notice
#         widgets = {
#             "body": RedactorEditor(),
#         }

# class PhotogalleryAdminForm(forms.ModelForm):
#     class Meta:
#         model = Photogallery
#         widgets = {
#             "body": RedactorEditor(),
#         }

# class VideoLibraryAdminForm(forms.ModelForm):
#     class Meta:
#         model = VideoLibrary
#         widgets = {
#             "body": RedactorEditor(),
#         }

# class PodcastAdminForm(forms.ModelForm):
#     class Meta:
#         model = Podcast
#         widgets = {
#             "body": RedactorEditor(),
#         }

# class EventAdminForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         formfield_overrides = {
#             models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
#         }
#         widgets = {
#             "body": RedactorEditor(),
#         }
