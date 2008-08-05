from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

from datetime import date

from main.models import *

@login_required
def project_list(request):
    '''
    select *
      from main_project
      where id in(
        select distinct project_id
          from main_task, main_task_staff
          where main_task_staff.user_id=:user
            and main_task.id=main_task_staff.task_id
      )
    '''    
    user = request.user
    projects =  Project.objects.extra(where=['''
        id in (
            select distinct project_id
            from main_task, main_task_staff
            where main_task_staff.user_id=%s
              and main_task.id=main_task_staff.task_id)
    '''], params=[user.id])
    return render_to_response('main/project-list.xml', {'projects': projects})

@login_required
def task_list(request):
    '''
    Get all the tasks for this user on a given project. If the project isn't specified return all
    of the task for the user.
    '''
    user = request.user
    project = None
    try:
        project_id = request['project']
        project = Project.objects.get(pk=project_id)
    except KeyError:
        pass
    except Project.DoesNotExist:
        pass
    
    tasks = None
    if project != None:
        tasks = user.tasks.filter(project=project)
    else:
        tasks = user.tasks.all()
    return render_to_response('main/task-list.xml', {'tasks': tasks})

@login_required
def task_status(request):
    '''
    Return the time on a task and the total time for today when given a task_id as a POST parameter.
    If the task_id isn't present or is not valid it will return 0:00 for the task-time'
    '''
    
    user = request.user
    current_task = None
    task_time = '0:00'
    today_time = '0:00'
    today = date.today()
    
    try:
        current_task = Task.objects.get(pk=request.POST['task'])
    except KeyError:
        pass
    except Task.DoesNotExist:
        pass
        
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
    return render_to_response('main/log-result.xml', {'current_task': current_task, 'task_time': task_time,
                                                       'today_time': today_time})

@login_required
def get_profile(request):
    "Get the user's profile if it exists"
    user = request.user
    try:
        profile = user.get_profile()
    except UserProfile.DoesNotExist:
        profile = None
    
    return render_to_response('main/profile.xml', {'profile': profile})