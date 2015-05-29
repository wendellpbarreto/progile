from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib import admin
from progile.apps.core.views import *

urlpatterns = [
    # url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^redactor/', include('redactor.urls')),

    url(r'^$', RedirectView.as_view(url='/home/')),
    url(r'^home/', HomeView.as_view()),

    # url(r'^(?P<slug>\w+)/$', core.as_view(), name='core',),
	# url(r'^(?P<slug>\w+)/(?P<pk>\d+)$', core.as_view(), name='core',),


]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)