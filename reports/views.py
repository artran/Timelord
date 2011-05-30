from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

from datetime import date

from timelord.main.models import *


def index(request):
    projects = Project.objects.all()
    return render_to_response('reports/index.html', {'projects': projects})
