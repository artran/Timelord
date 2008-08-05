# This Python file uses the following encoding: utf-8

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class Customer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
    class Admin:
        pass
    
class Project(models.Model):
    name = models.CharField(max_length=25, unique=True, core=True)
    customer = models.ForeignKey(Customer, related_name='projects', edit_inline=models.TABULAR)
    live = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
    class Admin:
        list_display = ('customer', 'name', 'live')
        list_display_links = ('name',)
        ordering = ('customer', 'name')
        list_filter = ('customer', 'name')
    
class Task(models.Model):
    name = models.CharField(max_length=25)
    project = models.ForeignKey(Project, related_name='tasks')
    managers = models.ManyToManyField(User, related_name='managed_tasks')
    staff = models.ManyToManyField(User, related_name='tasks')
    # TODO: 'live' inferred from project
    def __str__(self):
        return "%s: %s" % (self.project, self.name)
    class Meta:
        unique_together = ('name', 'project')
        ordering = ['name']
    class Admin:
        list_display = ('project', 'name')
        list_display_links = ('name',)
        ordering = ('project', 'name')
        list_filter = ('project', 'name')

class LogEntry(models.Model):
    task = models.ForeignKey(Task, related_name='log-entries')
    staff = models.ForeignKey(User, related_name='log-entries')
    logged_at = models.DateTimeField(default=datetime.now)
    delta_time = models.IntegerField(help_text="Number of minutes being logged")
    def __str__(self):
        return "%s, %s: %s" % (self.task, self.staff, self.delta_time)
    class Admin:
        save_on_top = True
        list_display = ('task', 'staff', 'delta_time', 'logged_at')
        list_filter = ('task', 'logged_at')
        ordering = ['-logged_at']
    
class Note(models.Model):
    text = models.TextField(core=True)
    log_entry = models.ForeignKey(LogEntry, edit_inline=models.TABULAR, num_in_admin=1)
    def __str__(self):
        return "%s: %s" % (self.task, self.text)
    class Admin:
        pass
    
class Expense(models.Model):
    text = models.TextField()
    amount = models.DecimalField(max_digits=5, decimal_places=2, help_text="£", core=True)
    log_entry = models.ForeignKey(LogEntry, edit_inline=models.TABULAR, num_in_admin=1)
    def __str__(self):
        return "%s: %s" % (self.task, self.text)
    class Admin:
        pass
    
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
    class Admin:
        pass
