from django.shortcuts import render_to_response, get_object_or_404
from main.models import *

def index(request):
    projects = Project.objects.all()
    return render_to_response('main/index.html', {'projects': projects})

def project(request, id):
    project = get_object_or_404(Project, pk=id)
    return render_to_response('main/project.html', {'project': project})