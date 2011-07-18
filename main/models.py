# This Python file uses the following encoding: utf-8
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, date


class LiveProjectManager(models.Manager):
    """Return only projects that are live"""
    def get_query_set(self):
        return super(LiveProjectManager, self).get_query_set().filter(live=True)


class Customer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Project(models.Model):
    name = models.CharField(max_length=25, unique=True,)
    customer = models.ForeignKey(Customer, related_name='projects')
    live = models.BooleanField(default=True)
    info = models.TextField(blank=True)
    url = models.URLField(blank=True, verify_exists=False)

    # Managers
    objects = models.Manager()  # If this isn't first then non-live projects can't edited in the admin interface
    live_objects = LiveProjectManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @models.permalink
    def get_absolute_url(self):
        return ('timelord_project_detail', (), {'id': self.pk})


class Task(models.Model):
    name = models.CharField(max_length=25)
    project = models.ForeignKey(Project, related_name='tasks')
    info = models.TextField(blank=True)
    managers = models.ManyToManyField(User, related_name='managed_tasks')
    staff = models.ManyToManyField(User, related_name='tasks')
    # TODO: 'live' inferred from project

    def __str__(self):
        return "%s: %s" % (self.project, self.name)

    class Meta:
        unique_together = ('name', 'project')
        ordering = ['name']


class LogEntry(models.Model):
    task = models.ForeignKey(Task, related_name='log-entries')
    staff = models.ForeignKey(User, related_name='log-entries')
    logged_at = models.DateTimeField(default=datetime.now, help_text='The time that the event was logged. The date should be taken from Logged_on.')
    logged_on = models.DateField(default=date.today)
    delta_time = models.IntegerField(help_text="Number of minutes being logged")

    def __unicode__(self):
        return "%s: %s, %s: %s" % (self.logged_at, self.task, self.staff, self.delta_time)


class Note(models.Model):
    text = models.TextField()
    log_entry = models.ForeignKey(LogEntry)

    def __unicode__(self):
        return "%s: %s" % (self.log_entry.task, self.text)


class Expense(models.Model):
    text = models.TextField()
    amount = models.DecimalField(max_digits=5, decimal_places=2, help_text="£")
    log_entry = models.ForeignKey(LogEntry)

    def __unicode__(self):
        return "%s: %s, GBP %s" % (self.log_entry.task, self.text, self.amount)


class Milestone(models.Model):
    MILESTONE_TYPES = (
        ('deadline', 'Deadline'),
        ('delivery', 'Delivery expected'),
        ('cust_info', 'Customer info required'),
        ('other', 'Other')
    )
    name = models.CharField(max_length=25)
    task = models.ForeignKey(Task, related_name='milestones')
    milestone_type = models.CharField(max_length=10, choices=MILESTONE_TYPES, default='deadline')
    occurs_at = models.DateTimeField()
    hit_at = models.DateTimeField(blank=True, null=True)
    email_overdue = models.BooleanField(default=False)

    def __str__(self):
        return "%s: %s" % (self.task, self.name)

    class Meta:
        unique_together = ('name', 'task')


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    preferred_task = models.ForeignKey(Task, help_text='Task selected by default in widgets')

    def __unicode__(self):
        return unicode(self.user)
