from django.conf.urls.defaults import *
from main.models import *

urlpatterns = patterns('main.views',
    (r'^$', 'index'),
    (r'^project/(?P<id>[0-9]+)/$', 'project'),
    (r'^status/$', 'status'),
    (r'^log/$', 'log'),
    (r'^task-status/$', 'task_status'),
    (r'^adjust-time/$', 'adjust_time'),
)