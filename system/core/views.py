#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import operator

from django.shortcuts import render
from itertools import chain
from django.db.models import F, Q

from .generic_view import GenericView
from .models import *

logger = logging.getLogger(__name__)

class GUI(GenericView):

    def __init__(self):
       pass

    def home(self, request):
       

        return {
            'template' : {
                'title' : 'progile | início',
            }
        }

    def about(self, request):
        abouts = About.objects.all()
        members = Member.objects.all().order_by('name')
        addresses = Address.objects.all()
        contacts = Contact.objects.all()

        return {
            'template' : {
                'title' : 'progile | início',
                'disciplines' : self.disciplines,
                'editorials' : self.editorials,
                'populars' : self.populars,
                'recents' : self.recents,
                'commenteds' : self.commenteds,
                'social_networks' : self.social_networks,
                'abouts' : abouts,
                'members' : members,
                'addresses' : addresses,
                'contacts' : contacts,
            }
        }

    def posts(self, request):
        notices, photogalleries, video_libraries = None, None, None
        discipline, curricular_practice, editorial = None, None, None


        try:
            discipline = Discipline.objects.get(pk=request.GET['discipline'])
        except Exception, e:
            discipline = None
            logger.error(str(e))
        else:
            notices = Notice.objects.filter(active=True, discipline=discipline).order_by('-date')
            photogalleries = Photogallery.objects.filter(active=True, discipline=discipline).order_by('-date')
            video_libraries = VideoLibrary.objects.filter(active=True, discipline=discipline).order_by('-date')


        try:
            curricular_practice = CurricularPractice.objects.get(pk=request.GET['curricular_practice'])
        except Exception, e:
            curricular_practice = None
            logger.error(str(e))
        else:
            if notices and photogalleries and video_libraries:
                notices = notices.filter(curricular_practice=curricular_practice).order_by('-date')
                photogalleries = photogalleries.filter(curricular_practice=curricular_practice).order_by('-date')
                video_libraries = video_libraries.filter(curricular_practice=curricular_practice).order_by('-date')
            else:
                notices = Notice.objects.filter(active=True, curricular_practice=curricular_practice).order_by('-date')
                photogalleries = Photogallery.objects.filter(active=True, curricular_practice=curricular_practice).order_by('-date')
                video_libraries = VideoLibrary.objects.filter(active=True, curricular_practice=curricular_practice).order_by('-date')


        try:
            editorial = Editorial.objects.get(pk=request.GET['editorial'])
        except Exception, e:
            editorial = None
            logger.error(str(e))
        else:
            if notices and photogalleries and video_libraries:
                notices = notices.filter(editorial=editorial).order_by('-date')
                photogalleries = photogalleries.filter(editorial=editorial).order_by('-date')
                video_libraries = video_libraries.filter(editorial=editorial).order_by('-date')
            else:
                notices = Notice.objects.filter(active=True, editorial=editorial).order_by('-date')
                photogalleries = Photogallery.objects.filter(active=True, editorial=editorial).order_by('-date')
                video_libraries = VideoLibrary.objects.filter(active=True, editorial=editorial).order_by('-date')


        try:
            author = Author.objects.get(pk=request.GET['author'])
        except Exception, e:
            author = None
            logger.error(str(e))
        else:
            if notices and photogalleries and video_libraries:
                notices = notices.filter(author=author).order_by('-date')
                photogalleries = photogalleries.filter(author=author).order_by('-date')
                video_libraries = video_libraries.filter(author=author).order_by('-date')
            else:
                notices = Notice.objects.filter(active=True, author=author).order_by('-date')
                photogalleries = Photogallery.objects.filter(active=True, author=author).order_by('-date')
                video_libraries = VideoLibrary.objects.filter(active=True, author=author).order_by('-date')


        try:
            keywords = request.GET['keywords'].split()
        except Exception, e:
            keywords = None
            logger.error(str(e))
        else:
            if keywords:
                if notices and photogalleries and video_libraries:
                    notices = notices.filter(reduce(lambda x, y: x | y, [Q(title__icontains=unicode(keyword)) for keyword in keywords]))
                    photogalleries = photogalleries.filter(reduce(lambda x, y: x | y, [Q(title__icontains=unicode(keyword)) for keyword in keywords]))
                    video_libraries = video_libraries.filter(reduce(lambda x, y: x | y, [Q(title__icontains=unicode(keyword)) for keyword in keywords]))
                else:
                    notices = Notice.objects.filter(reduce(lambda x, y: x | y, [Q(title__icontains=unicode(keyword)) for keyword in keywords]), active=True).order_by('-date')
                    photogalleries = Photogallery.objects.filter(reduce(lambda x, y: x | y, [Q(title__icontains=unicode(keyword)) for keyword in keywords]), active=True).order_by('-date')
                    video_libraries = VideoLibrary.objects.filter(reduce(lambda x, y: x | y, [Q(title__icontains=unicode(keyword)) for keyword in keywords]), active=True).order_by('-date')
            elif (not discipline) and (not curricular_practice) and (not editorial) and (not author):
                notices = Notice.objects.filter(active=True).order_by('-date')
                photogalleries = Photogallery.objects.filter(active=True).order_by('-date')
                video_libraries = VideoLibrary.objects.filter(active=True).order_by('-date')
        finally:
            if (not discipline) and (not curricular_practice) and (not editorial) and (not author):
                notices = Notice.objects.filter(active=True).order_by('-date')
                photogalleries = Photogallery.objects.filter(active=True).order_by('-date')
                video_libraries = VideoLibrary.objects.filter(active=True).order_by('-date')

        posts = list(chain(notices, photogalleries, video_libraries))
        posts = sorted(posts, key=operator.attrgetter('date'), reverse=True)

        try:
            page = int(request.GET['page'])
        except:
            page = 1
        finally:
            posts = self.paginate(obj=posts, page=page, num_per_page=5)

        return {
            'template' : {
                'title' : 'progile | início',
                'disciplines' : self.disciplines,
                'editorials' : self.editorials,
                'populars' : self.populars,
                'recents' : self.recents,
                'commenteds' : self.commenteds,
                'social_networks' : self.social_networks,
                'posts' : posts,
                'editorial' : editorial,
                'author' : author,
            }
        }

    def notices(self, request):
        data = None
        notices = Notice.objects.filter(active=True).order_by('-date')

        data = {
            'template' : {
                'title' : 'progile | notícias',
                'disciplines' : self.disciplines,
                'editorials' : self.editorials,
                'populars' : self.populars,
                'recents' : self.recents,
                'commenteds' : self.commenteds,
                'social_networks' : self.social_networks,
                'notices' : notices,
            }
        }

        return data

    def notice(self, request):
        data = None

        try:
            pk = self.kwargs['pk']
            notice = Notice.objects.get(pk=pk)
            notice.views+=1
            notice.save()
        except Exception, e:
            logger.error(str(e))
        else:

            data =  {
                'template' : {
                    'title' : 'progile | notícia',
                    'disciplines' : self.disciplines,
                    'editorials' : self.editorials,
                    'populars' : self.populars,
                    'recents' : self.recents,
                    'commenteds' : self.commenteds,
                    'social_networks' : self.social_networks,
                    'notice' : notice,
                }
            }
        finally:
            return data

    def photogalleries(self, request):
        data = None
        photogalleries = Photogallery.objects.filter(active=True).order_by('-date')

        data = {
            'template' : {
                'title' : 'progile | fotogalerias',
                'disciplines' : self.disciplines,
                'editorials' : self.editorials,
                'populars' : self.populars,
                'recents' : self.recents,
                'commenteds' : self.commenteds,
                'social_networks' : self.social_networks,
                'photogalleries' : photogalleries,
            }
        }
        return data

    def photogallery(self, request):
        data = None

        try:
            pk = self.kwargs['pk']
            photogallery = Photogallery.objects.get(pk=pk)
            photogallery.views+=1
            photogallery.save()
        except Exception, e:
            logger.error(str(e))
        else:

            data =  {
                'template' : {
                    'title' : 'progile | fotogaleria',
                    'disciplines' : self.disciplines,
                    'editorials' : self.editorials,
                    'populars' : self.populars,
                    'recents' : self.recents,
                    'commenteds' : self.commenteds,
                    'social_networks' : self.social_networks,
                    'photogallery' : photogallery,
                }
            }
        finally:
            return data

    def video_libraries(self, request):
        data = None
        video_libraries = VideoLibrary.objects.filter(active=True).order_by('-date')

        data = {
            'template' : {
                'title' : 'progile | videotecas',
                'disciplines' : self.disciplines,
                'editorials' : self.editorials,
                'populars' : self.populars,
                'recents' : self.recents,
                'commenteds' : self.commenteds,
                'social_networks' : self.social_networks,
                'video_libraries' : video_libraries,
            }
        }

        return data

    def video_library(self, request):
        data = None

        try:
            pk = self.kwargs['pk']
            video_library = VideoLibrary.objects.get(pk=pk)
            video_library.views+=1
            video_library.save()
        except Exception, e:
            logger.error(str(e))
        else:

            data =  {
                'template' : {
                    'title' : 'progile | videoteca',
                    'disciplines' : self.disciplines,
                    'editorials' : self.editorials,
                    'populars' : self.populars,
                    'recents' : self.recents,
                    'commenteds' : self.commenteds,
                    'social_networks' : self.social_networks,
                    'video_library' : video_library,
                }
            }
        finally:
            return data

    def events(self, request):
        data = None
        events = Event.objects.filter(active=True).order_by('-date')

        data = {
            'template' : {
                'title' : 'progile | eventos',
                'disciplines' : self.disciplines,
                'editorials' : self.editorials,
                'populars' : self.populars,
                'recents' : self.recents,
                'commenteds' : self.commenteds,
                'social_networks' : self.social_networks,
                'events' : events,
            }
        }

        return data

    def event(self, request):
        data = None

        try:
            pk = self.kwargs['pk']
            event = Event.objects.get(pk=pk)
            event.views+=1
            event.save()
        except Exception, e:
            logger.error(str(e))
        else:

            data =  {
                'template' : {
                    'title' : 'progile | videoteca',
                    'disciplines' : self.disciplines,
                    'editorials' : self.editorials,
                    'populars' : self.populars,
                    'recents' : self.recents,
                    'commenteds' : self.commenteds,
                    'social_networks' : self.social_networks,
                    'event' : event,
                }
            }
        finally:
            return data
