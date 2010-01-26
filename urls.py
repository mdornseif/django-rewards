# -*- coding: utf-8 -*-

"""URLs for testing django-rewards."""

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
# admin stuff
(r'^admin/doc/', include('django.contrib.admindocs.urls')),
(r'^admin/', include(admin.site.urls)),
# include django-rewards
(r'^rewards/', include('rewards.urls')),
(r'^$', 'django.views.generic.simple.redirect_to', {'url' : '/rewards/'}),
)

# when in development mode, serve static files 'by hand'
# in production the files should be placed at http://s.hdimg.net/django-rewards/
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './media'}),
    )
