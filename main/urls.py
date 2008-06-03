from django.conf.urls.defaults import *
from main.models import *

urlpatterns = patterns('main.views',
    (r'^$', 'index'),
    (r'^project/(?P<id>[0-9]+)/$', 'project')
)