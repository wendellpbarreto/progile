#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import *
from .forms import *

# admin.site.unregister(Group)

# class SocialNetworkAdmin(admin.ModelAdmin):
#     model = SocialNetwork
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Informations"), {
#                 "fields" : (
#                     "type", "url",
#                 )
#             }
#         ),
#     )
#     list_display = ("type", "url")
#     list_filter = ("type",)
#     search_fields = ("type",)
#     ordering = ("type", "url",)

# admin.site.register(SocialNetwork, SocialNetworkAdmin)

# class ContactAdmin(admin.ModelAdmin):
#     model = Contact
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Informations"), {
#                 "fields" : (
#                     "type", "value",
#                 )
#             }
#         ),
#     )
#     list_display = ("type", "value")
#     list_filter = ("type",)
#     search_fields = ("type",)
#     ordering = ("type", "value",)

# admin.site.register(Contact, ContactAdmin)

# class AddressAdmin(admin.ModelAdmin):
#     model = Address
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("street", "number",),
#                     "complement",
#                     ("district", "zip_code",),
#                     ("city", "state",),
#                 )
#             }
#         ),
#     )
#     list_display = ("street",)

# admin.site.register(Address, AddressAdmin)

# class AboutAdmin(admin.ModelAdmin):
#     model = About
#     form = AboutAdminForm
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Informations"), {
#                 "fields" : (
#                     "body",
#                 )
#             }
#         ),
#     )
#     list_display = ("pk",)

# admin.site.register(About, AboutAdmin)

# class RoleAdmin(admin.ModelAdmin):
#     model = Role

# admin.site.register(Role, RoleAdmin)

# class MemberAdmin(admin.ModelAdmin):
#     model = Member
#     form = MemberAdminForm
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("photo", "photo_tag"),
#                     ("name", "role",),
#                     ("email", "phone",),
#                     ("about",),
#                 )
#             }
#         ),
#     )
#     list_display = ("name", "role", "email", "phone",)
#     list_filter = ("role",)
#     search_fields = ("name", "role", "email",)
#     ordering = ("name", "role",)
#     readonly_fields = ("photo_tag",)

# admin.site.register(Member, MemberAdmin)

# class CurricularPracticeInline(admin.StackedInline):
#     model = CurricularPractice
#     extra = 1
#     can_delete = True
#     max_num = 99
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)

# class DisciplineAdmin(admin.ModelAdmin):
#     model = Discipline
#     inlines = (CurricularPracticeInline,)

# admin.site.register(Discipline, DisciplineAdmin)

# class EditorialAdmin(admin.ModelAdmin):
#     model = Editorial

# admin.site.register(Editorial, EditorialAdmin)

# class AuthorAdmin(admin.ModelAdmin):
#     model = Author
#     form = AuthorAdminForm
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("photo", "photo_tag"),
#                     ("name",),
#                     ("email", "phone",),
#                     ("about",),
#                 )
#             }
#         ),
#     )
#     list_display = ("name", "email", "phone",)
#     search_fields = ("name", "email",)
#     ordering = ("name",)
#     readonly_fields = ("photo_tag",)

# admin.site.register(Author, AuthorAdmin)

# class PhotographerAdmin(admin.ModelAdmin):
#     model = Photographer
#     form = PhotographerAdminForm
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("photo", "photo_tag"),
#                     ("name",),
#                     ("email", "phone",),
#                     ("about",),
#                 )
#             }
#         ),
#     )
#     list_display = ("name", "email", "phone",)
#     search_fields = ("name", "email",)
#     ordering = ("name",)
#     readonly_fields = ("photo_tag",)

# admin.site.register(Photographer, PhotographerAdmin)

# class NoticeAdmin(admin.ModelAdmin):
#     model = Notice
#     form = NoticeAdminForm
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Statistics"), {
#                 "fields" : (
#                     ("views", "comments", "likes",),
#                 )
#             }
#         ),
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("date", "active", "featured"),
#                     ("editorial", "discipline", "curricular_practice"),
#                     "author",
#                 )
#             }
#         ),
#         (
#             _("Description"), {
#                 "fields" : (
#                     "title",
#                     "subtitle",
#                     "body",
#                     ("photo", "photo_tag",),
#                     "photographer",
#                 )
#             }
#         ),
#     )
#     list_display = ("title", "date", "date_modified", "editorial", "featured", "active",)
#     list_filter = ("date", "editorial__name", "featured", "active",)
#     search_fields = ("date", "date_modified", "editorial__name", "featured", "active",)
#     ordering = ("date_modified", "date", "editorial", "active", "featured")
#     readonly_fields = ("views", "comments", "likes", "photo_tag",)

#     class Media:
#         css = {
#              "all": ("admin/datepicker.css",)
#         }

# admin.site.register(Notice, NoticeAdmin)

# class PhotoInline(admin.StackedInline):
#     model = Photo
#     extra = 1
#     can_delete = True
#     max_num = 99
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     readonly_fields = ("photo_tag",)

# class PhotogalleryAdmin(admin.ModelAdmin):
#     model = Photogallery
#     form = PhotogalleryAdminForm
#     inlines = (PhotoInline,)
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Statistics"), {
#                 "fields" : (
#                     ("views", "comments", "likes",),
#                 )
#             }
#         ),
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("date", "active",),
#                     ("editorial", "discipline", "curricular_practice"),
#                     "author",
#                 )
#             }
#         ),
#         (
#             _("Description"), {
#                 "fields" : (
#                     "title",
#                     "subtitle",
#                     "body",
#                 )
#             }

#         ),
#     )
#     list_display = ("title", "date", "date_modified", "active",)
#     list_filter = ("date", "active",)
#     search_fields = ("date", "date_modified", "active",)
#     ordering = ("date_modified", "date", "active",)
#     readonly_fields = ("views", "comments", "likes",)

#     class Media:
#         css = {
#              "all": ("admin/datepicker.css",)
#         }

# admin.site.register(Photogallery, PhotogalleryAdmin)

# class VideoInline(admin.StackedInline):
#     model = Video
#     extra = 1
#     can_delete = True
#     max_num = 99
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)

# class VideoLibraryAdmin(admin.ModelAdmin):
#     model = VideoLibrary
#     form = VideoLibraryAdminForm
#     inlines = (VideoInline,)
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Statistics"), {
#                 "fields" : (
#                     ("views", "comments", "likes",),
#                 )
#             }
#         ),
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("date", "active",),
#                     ("editorial", "discipline", "curricular_practice"),
#                     "author",
#                 )
#             }
#         ),
#         (
#             _("Description"), {
#                 "fields" : (
#                     "title",
#                     "subtitle",
#                     "body",
#                 )
#             }
#         ),
#     )
#     list_display = ("title", "date", "date_modified", "active",)
#     list_filter = ("date", "active",)
#     search_fields = ("date", "date_modified", "active",)
#     ordering = ("date_modified", "date", "active",)
#     readonly_fields = ("views", "comments", "likes",)

#     class Media:
#         css = {
#              "all": ("admin/datepicker.css",)
#         }

# admin.site.register(VideoLibrary, VideoLibraryAdmin)

# class PodcastAdmin(admin.ModelAdmin):
#     model = Podcast
#     form = PodcastAdminForm
#     classes = ("grp-collapse grp-open",)
#     inline_classes = ("grp-collapse grp-open",)
#     fieldsets = (
#         (
#             _("Statistics"), {
#                 "fields" : (
#                     ("views", "comments", "likes",),
#                 )
#             }
#         ),
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("date", "active",),
#                     "author"
#                 )
#             }
#         ),
#         (
#             _("Description"), {
#                 "fields" : (
#                     "title",
#                     "subtitle",
#                     "body",
#                     "download_url",
#                 )
#             }
#         ),
#     )
#     list_display = ("title", "date", "date_modified", "active",)
#     list_filter = ("date", "active",)
#     search_fields = ("date", "date_modified", "active",)
#     ordering = ("date_modified", "date", "active",)
#     readonly_fields = ("views", "comments", "likes",)

#     class Media:
#         css = {
#              "all": ("admin/datepicker.css",)
#         }

# admin.site.register(Podcast, PodcastAdmin)

# class EventAdmin(admin.ModelAdmin):
#     model = Event
#     form = EventAdminForm
#     fieldsets = (
#         (
#             _("Statistics"), {
#                 "fields" : (
#                     ("views", "comments", "likes",),
#                 )
#             }
#         ),
#         (
#             _("Informations"), {
#                 "fields" : (
#                     ("date", "active",),
#                     "author",
#                 )
#             }
#         ),
#         (
#             _("Description"), {
#                 "fields" : (
#                     "title",
#                     "subtitle",
#                     "body",
#                 )
#             }
#         ),
#         (
#             _("Medias"), {
#                 "fields" : (
#                     "notices",
#                     "photogalleries",
#                     "video_libraries",
#                     "podcasts",
#                 )
#             }
#         ),
#     )
#     filter_horizontal = ("notices", "photogalleries", "video_libraries", "podcasts",)
#     list_display = ("title", "date", "date_modified", "active",)
#     list_filter = ("date", "active",)
#     search_fields = ("date", "date_modified", "active",)
#     ordering = ("date_modified", "date", "active",)
#     readonly_fields = ("views", "comments", "likes",)

#     class Media:
#         css = {
#              "all": ("admin/datepicker.css",)
#         }

# admin.site.register(Event, EventAdmin)

