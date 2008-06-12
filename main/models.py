from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class Customer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, blank=True)
    def __str__(self):
        return self.name
    class Admin:
        pass
    
class Project(models.Model):
    name = models.CharField(max_length=25, unique=True)
    customer = models.ForeignKey(Customer, related_name='projects')
    # needs a 'live' field
    def __str__(self):
        return self.name
    class Admin:
        pass
    
class Task(models.Model):
    name = models.CharField(max_length=25)
    project = models.ForeignKey(Project, related_name='tasks')
    managers = models.ManyToManyField(User, related_name='managed_tasks')
    staff = models.ManyToManyField(User, related_name='tasks')
    # needs a 'live' field or possibly inferred from project
    def __str__(self):
        return "%s: %s" % (self.project, self.name)
    class Meta:
        unique_together = ('name', 'project')
    class Admin:
        pass
    
class Note(models.Model):
    task = models.ForeignKey(Task, related_name='notes')
    staff = models.ForeignKey(User, related_name='notes')
    text = models.TextField()
    def __str__(self):
        return "%s: %s" % (self.task, self.text)
    class Admin:
        pass
    
class Expense(models.Model):
    task = models.ForeignKey(Task, related_name='expenses')
    staff = models.ForeignKey(User, related_name='expenses')
    text = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
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
        
class LogEntry(models.Model):
    task = models.ForeignKey(Task, related_name='log-entries')
    staff = models.ForeignKey(User, related_name='log-entries')
    logged_at = models.DateTimeField(default=datetime.now)
    delta_time = models.PositiveIntegerField() # number of minutes being logged
    note = models.ForeignKey(Note, blank=True, null=True)
    def __str__(self):
        return "%s, %s: %s" % (self.task, self.staff, self.delta_time)
    class Admin:
        pass
