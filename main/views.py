from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from datetime import date

from models import *

import api_views


def index(request):
    projects = Project.objects.all()
    return render_to_response('main/index.html', {'projects': projects})


def project(request, id):
    project = get_object_or_404(Project, pk=id)
    return render_to_response('main/project.html', {'project': project})


@login_required
def status(request):
    'Return the current task, all tasks for this user, all milestones for this task and times for task and day.'

    user = request.user
    task = None
    milestones = []
    task_time = "0:00"
    today = date.today()

    try:
        task = Task.objects.get(pk=request.REQUEST['task'])
    except:
        try:
            profile = user.get_profile()
            task = profile.preferred_task
        except UserProfile.DoesNotExist:
            task = None

    if task and task in user.tasks.all():
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

    tasks = user.tasks.order_by('project__name', 'name')
    return render_to_response('main/status.html', {'current_task': task, 'tasks': tasks, 'milestones': milestones,
                                                   'today_time': today_time, 'task_time': task_time, 'user': user}, context_instance=RequestContext(request))


@login_required
def log(request):
    'Add log entries for an arbitary number of tasks. The task_id is a key into a map and the delta is the value.'

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

    return api_views.task_status(request)


@login_required
def adjust_time(request):
    'Add a log entry for a single task. The POST parameters are the task_id and delta_time in minutes.'

    if request.method != 'POST':
        return status(request)
    user = request.user
    current_task = Task.objects.get(pk=request.POST['task'])
    log = LogEntry()
    log.staff = user
    log.task = current_task
    log.delta_time = request.POST['adjust']
    log.save()
    return api_views.task_status(request)
