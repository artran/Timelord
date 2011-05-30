from django.conf.urls.defaults import *
from models import *

# Views for the HTML web interface
urlpatterns = patterns('timelord.main.views',
    (r'^$', 'index'),
    (r'^project/(?P<id>[0-9]+)/$', 'project'),
    (r'^status/$', 'status'),
    (r'^log/$', 'log'),
    (r'^adjust-time/$', 'adjust_time'),
)

# Views for the XML api
urlpatterns += patterns('timelord.main.api_views',
    (r'^project-list/$', 'project_list'),
    (r'^task-list/$', 'task_list'),
    (r'^task-status/$', 'task_status'),
)