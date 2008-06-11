from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

from datetime import date

from main.models import *

def index(request):
    projects = Project.objects.all()
    return render_to_response('main/index.html', {'projects': projects})

def project(request, id):
    project = get_object_or_404(Project, pk=id)
    return render_to_response('main/project.html', {'project': project})

def status(request):
    user = request.user
    project = None
    task = None
    milestones = []
    task_time = "0:00"
    today = date.today()
    
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=request.POST['task'])
        milestones = task.milestones.all()
        log_entries = LogEntry.objects.filter(staff=user, task=task,
                      logged_at__year=today.year, logged_at__month=today.month,
                      logged_at__day=today.day)
        task_mins = 0
        for entry in log_entries:
            task_mins += entry.delta_time
        task_hours = task_mins // 60
        task_mins = task_mins - (60 * task_hours)
        task_time = "%i:%#02i" % (task_hours, task_mins)
    
    log_entries = LogEntry.objects.filter(staff=user,
                          logged_at__year=today.year, logged_at__month=today.month,
                          logged_at__day=today.day)
    today_mins = 0
    for entry in log_entries:
        today_mins += entry.delta_time
    today_hours = today_mins // 60
    today_mins = today_mins - (60 * today_hours)
    today_time = "%i:%#02i" % (today_hours, today_mins)
    
    tasks = user.tasks.all()
    return render_to_response('main/status.html', {'project': project, 'current_task': task,
                                                   'tasks': tasks, 'milestones': milestones,
                                                   'today_time': today_time,'task_time': task_time})

def log(request):
    print request.POST
    
    return status(request)