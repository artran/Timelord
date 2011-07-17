# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Customer'
        db.create_table('main_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
        ))
        db.send_create_signal('main', ['Customer'])

        # Adding model 'Project'
        db.create_table('main_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['main.Customer'])),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('main', ['Project'])

        # Adding model 'Task'
        db.create_table('main_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tasks', to=orm['main.Project'])),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['Task'])

        # Adding unique constraint on 'Task', fields ['name', 'project']
        db.create_unique('main_task', ['name', 'project_id'])

        # Adding M2M table for field managers on 'Task'
        db.create_table('main_task_managers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['main.task'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('main_task_managers', ['task_id', 'user_id'])

        # Adding M2M table for field staff on 'Task'
        db.create_table('main_task_staff', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['main.task'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('main_task_staff', ['task_id', 'user_id'])

        # Adding model 'LogEntry'
        db.create_table('main_logentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='log-entries', to=orm['main.Task'])),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(related_name='log-entries', to=orm['auth.User'])),
            ('logged_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('delta_time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['LogEntry'])

        # Adding model 'Note'
        db.create_table('main_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('log_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.LogEntry'])),
        ))
        db.send_create_signal('main', ['Note'])

        # Adding model 'Expense'
        db.create_table('main_expense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('log_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.LogEntry'])),
        ))
        db.send_create_signal('main', ['Expense'])

        # Adding model 'Milestone'
        db.create_table('main_milestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='milestones', to=orm['main.Task'])),
            ('milestone_type', self.gf('django.db.models.fields.CharField')(default='deadline', max_length=10)),
            ('occurs_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('hit_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('email_overdue', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('main', ['Milestone'])

        # Adding unique constraint on 'Milestone', fields ['name', 'task']
        db.create_unique('main_milestone', ['name', 'task_id'])

        # Adding model 'UserProfile'
        db.create_table('main_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('preferred_task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Task'])),
        ))
        db.send_create_signal('main', ['UserProfile'])

    def backwards(self, orm):

        # Removing unique constraint on 'Milestone', fields ['name', 'task']
        db.delete_unique('main_milestone', ['name', 'task_id'])

        # Removing unique constraint on 'Task', fields ['name', 'project']
        db.delete_unique('main_task', ['name', 'project_id'])

        # Deleting model 'Customer'
        db.delete_table('main_customer')

        # Deleting model 'Project'
        db.delete_table('main_project')

        # Deleting model 'Task'
        db.delete_table('main_task')

        # Removing M2M table for field managers on 'Task'
        db.delete_table('main_task_managers')

        # Removing M2M table for field staff on 'Task'
        db.delete_table('main_task_staff')

        # Deleting model 'LogEntry'
        db.delete_table('main_logentry')

        # Deleting model 'Note'
        db.delete_table('main_note')

        # Deleting model 'Expense'
        db.delete_table('main_expense')

        # Deleting model 'Milestone'
        db.delete_table('main_milestone')

        # Deleting model 'UserProfile'
        db.delete_table('main_userprofile')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.customer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Customer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        },
        'main.expense': {
            'Meta': {'object_name': 'Expense'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.LogEntry']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'main.logentry': {
            'Meta': {'object_name': 'LogEntry'},
            'delta_time': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logged_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'log-entries'", 'to': "orm['auth.User']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'log-entries'", 'to': "orm['main.Task']"})
        },
        'main.milestone': {
            'Meta': {'unique_together': "(('name', 'task'),)", 'object_name': 'Milestone'},
            'email_overdue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hit_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone_type': ('django.db.models.fields.CharField', [], {'default': "'deadline'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'occurs_at': ('django.db.models.fields.DateTimeField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'milestones'", 'to': "orm['main.Task']"})
        },
        'main.note': {
            'Meta': {'object_name': 'Note'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.LogEntry']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'main.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['main.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'main.task': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'project'),)", 'object_name': 'Task'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'managed_tasks'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks'", 'to': "orm['main.Project']"}),
            'staff': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tasks'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preferred_task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['main']
