from django.conf.urls.defaults import *
from django.contrib import admin

import sys

admin.autodiscover()

# The main site
urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/timelord/'}),
    (r'^timelord/', include('timelord.main.urls')),
)

urlpatterns += patterns('',
    (r'^reports/', include('timelord.reports.urls')),
)

# The admin site
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

# Authentication
urlpatterns += patterns('',
	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

# Static content
if 'runserver' in sys.argv:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    )