from django.contrib.auth.decorators import login_required
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

@login_required
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

@login_required
def log(request):
    if request.method != 'POST':
        return status(request)
    
    user = request.user
    for item in request.POST.items():
        key = item[0]
        val = item[1]
        
        if key != 'task':
            try:
                task = Task.objects.get(pk=key)
                log = LogEntry()
                log.staff = user
                log.task = task
                log.delta_time = val
                log.save()
            except:
                pass
    
    return task_status(request)        

@login_required
def task_status(request):
    user = request.user
    current_task = None
    task_time = '0:00'
    today_time = '0:00'
    today = date.today()
    
    current_task = Task.objects.get(pk=request.POST['task'])
    # Get time for the current task
    log_entries = LogEntry.objects.filter(staff=user, task=current_task,
                  logged_at__year=today.year, logged_at__month=today.month,
                  logged_at__day=today.day)
    task_mins = 0
    for entry in log_entries:
        task_mins += entry.delta_time
    task_hours = task_mins // 60
    task_mins = task_mins - (60 * task_hours)
    task_time = "%i:%#02i" % (task_hours, task_mins)
    
    # Get the total time for today
    log_entries = LogEntry.objects.filter(staff=user,
                          logged_at__year=today.year, logged_at__month=today.month,
                          logged_at__day=today.day)
    today_mins = 0
    for entry in log_entries:
        today_mins += entry.delta_time
    today_hours = today_mins // 60
    today_mins = today_mins - (60 * today_hours)
    today_time = "%i:%#02i" % (today_hours, today_mins)
    #except:
    #    print 'exception'
    
    return render_to_response('main/log-result.xml', {'current_task': current_task, 'task_time': task_time,
                                                       'today_time': today_time})