from django.contrib import admin

from models import *


class CustomerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, CustomerAdmin)


class ProjectAdmin(admin.ModelAdmin):
    # list_display = ('customer', 'name', 'live')
    # list_display_links = ('name',)
    # ordering = ('customer', 'name')
    # list_filter = ('customer', 'name')
    pass
admin.site.register(Project, ProjectAdmin)


class TaskAdmin(admin.ModelAdmin):
    # list_display = ('project', 'name')
    # list_display_links = ('name',)
    # ordering = ('project', 'name')
    # list_filter = ('project', 'name')
    pass
admin.site.register(Task, TaskAdmin)


class LogEntryAdmin(admin.ModelAdmin):
    # save_on_top = True
    # list_display = ('task', 'staff', 'delta_time', 'logged_at')
    # list_filter = ('task', 'logged_at')
    # ordering = ['-logged_at']
    pass
admin.site.register(LogEntry, LogEntryAdmin)

    
class NoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Note, NoteAdmin)


class ExpenseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Expense, ExpenseAdmin)


class MilestoneAdmin(admin.ModelAdmin):
        pass
admin.site.register(Milestone, MilestoneAdmin)


class UserProfileAdmin(admin.ModelAdmin):
        pass
admin.site.register(UserProfile, UserProfileAdmin)