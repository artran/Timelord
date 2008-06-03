from django.conf.urls.defaults import *
import sys

urlpatterns = patterns('',
    # The main site
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/timelord/'}),
    (r'^timelord/', include('main.urls')),
)

urlpatterns += patterns('',
    # Admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)

# Static content
if 'runserver' in sys.argv:
    urlpatterns += patterns('',
        (r'^media/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/css'}),
        (r'^media/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/js'}),
        (r'^media/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/images'}),
    )