from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

#admin
from django.contrib import admin
admin.autodiscover()

# local static
from django.views.static import *
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'engine.views.display_cluster_engine'),
    url(r'^engine/', include('engine.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^.*/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^admin/', include(admin.site.urls)),


)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
