from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import Http404, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404

from datetime import date

from timelord.main.models import *


def index(request):
    projects = Project.objects.all()
    return render_to_response('reports/index.html', {'projects': projects})


def summary_for_dates(request, start, end):
    try:
        start_date = date(int(start[0:4]), int(start[4:6]), int(start[6:8]))
        end_date = date(int(end[0:4]), int(end[4:6]), int(end[6:8]))
    except ValueError:
        return HttpResponseServerError('Invalid date format')

    log_totals = LogEntry.objects.filter(logged_on__range=(start_date, end_date)).values('task__name').annotate(total_time=Sum('delta_time'))
    tasks = Task.objects.all()

    return render_to_response('reports/summary-for-dates.html', {'log_totals': log_totals, 'tasks': tasks})

def invoice_project(request, project_id):
    filtered = LogEntry.objects.filter(task__project=project_id, invoiced=False)
    log_totals = filtered.values('task__name', 'logged_on').annotate(total_time=Sum('delta_time'))
    total_time = filtered.aggregate(time=Sum('delta_time'))
    return render_to_response('reports/invoice.html', {'log_totals': log_totals, 'total_time': total_time['time']})
