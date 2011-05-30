from django.conf.urls.defaults import *
from timelord.main.models import *

project_list_dict = {
    'queryset': Project.live_objects.all(),
    'template_name': 'reports/project_list.html',
    'template_object_name': 'project',
}

project_detail_dict = {
    'queryset': Project.live_objects.all(),
    'template_name': 'reports/project_detail.html',
    'template_object_name': 'project',
}

# Views for the reports
urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', project_list_dict, 'timelord_project_list'),
    (r'^project/(?P<object_id>[0-9]+)/$', 'object_detail', project_detail_dict, 'timelord_project_detail'),
)