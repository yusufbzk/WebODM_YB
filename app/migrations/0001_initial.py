# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-12 15:35
from __future__ import unicode_literals

import app.models
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nodeodm', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='File uploaded by a user', upload_to=app.models.image_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A label used to describe the project', max_length=255)),
                ('description', models.TextField(blank=True, help_text='More in-depth description of the project', null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date')),
                ('deleting', models.BooleanField(db_index=True, default=False, help_text='Whether this project has been marked for deletion. Projects that have running tasks need to wait for tasks to be properly cleaned up before they can be deleted.')),
                ('owner', models.ForeignKey(help_text='The person who created the project', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectGroupObjectPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Project')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectUserObjectPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Project')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Permission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, db_index=True, default='', help_text="Identifier of the task (as returned by OpenDroneMap's REST API)", max_length=255)),
                ('name', models.CharField(blank=True, help_text='A label for the task', max_length=255, null=True)),
                ('processing_lock', models.BooleanField(default=False, help_text='A flag indicating whether this task is currently locked for processing. When this flag is turned on, the task is in the middle of a processing step.')),
                ('processing_time', models.IntegerField(default=-1, help_text='Number of milliseconds that elapsed since the beginning of this task (-1 indicates that no information is available)')),
                ('status', models.IntegerField(blank=True, choices=[(10, 'QUEUED'), (20, 'RUNNING'), (30, 'FAILED'), (40, 'COMPLETED'), (50, 'CANCELED')], db_index=True, help_text='Current status of the task', null=True)),
                ('last_error', models.TextField(blank=True, help_text='The last processing error received', null=True)),
                ('options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, help_text='Options that are being used to process this task', validators=[app.models.validate_task_options])),
                ('console_output', models.TextField(blank=True, default='', help_text="Console output of the OpenDroneMap's process")),
                ('ground_control_points', models.FileField(blank=True, help_text='Optional Ground Control Points file to use for processing', null=True, upload_to=app.models.gcp_directory_path)),
                ('orthophoto', models.CharField(blank=True, help_text='Orthophoto created by OpenDroneMap', null=True, max_length=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date')),
                ('pending_action', models.IntegerField(blank=True, choices=[(1, 'CANCEL'), (2, 'REMOVE'), (3, 'RESTART')], db_index=True, help_text='A requested action to be performed on the task. The selected action will be performed by the scheduler at the next iteration.', null=True)),
                ('processing_node', models.ForeignKey(blank=True, help_text='Processing node assigned to this task (or null if this task has not been associated yet)', null=True, on_delete=django.db.models.deletion.CASCADE, to='nodeodm.ProcessingNode')),
                ('project', models.ForeignKey(help_text='Project that this task belongs to', on_delete=django.db.models.deletion.CASCADE, to='app.Project')),
            ],
        ),
        migrations.AddField(
            model_name='imageupload',
            name='task',
            field=models.ForeignKey(help_text='Task this image belongs to', on_delete=django.db.models.deletion.CASCADE, to='app.Task'),
        ),
        migrations.AlterUniqueTogether(
            name='projectuserobjectpermission',
            unique_together=set([('user', 'permission', 'content_object')]),
        ),
        migrations.AlterUniqueTogether(
            name='projectgroupobjectpermission',
            unique_together=set([('group', 'permission', 'content_object')]),
        ),
    ]
