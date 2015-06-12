#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import uuid

from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User

from django import template

register = template.Library()

logger = logging.getLogger(__name__)

STATUS = (
    ("open", "open"),
    ("closed", "closed"),
)

class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True, blank=False)

    objects = GetOrNoneManager()

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        db_table = "team"

    def __unicode__(self):
        return u"%s" % (self.name.lower())

class Speciality(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True, blank=False)

    objects = GetOrNoneManager()

    class Meta:
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"
        db_table = "speciality"

    def __unicode__(self):
        return u"%s" % (self.name.lower())

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512, blank=True)
    visibility = models.BooleanField(default=False)
    team_id = models.ForeignKey(Team, null=True, db_column='team_id')

    objects = GetOrNoneManager()

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        db_table = "project"

    def __unicode__(self):
        return u"%s" % (self.name.lower())

class Sprint(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=124)
    description = models.CharField(max_length=512)
    order = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    project_id = models.ForeignKey(Project, db_column='project_id', related_name='sprints')

    objects = GetOrNoneManager()

    class Meta: 
        verbose_name = "Sprint"
        verbose_name_plural = "Sprints"
        db_table = "sprint"

    def __unicode__(self):
        return u"%s" % (self.title.capitalize())

class Board(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    order = models.IntegerField()
    project_id = models.ForeignKey(Project, db_column='project_id', related_name='boards')
    
    objects = GetOrNoneManager()

    def get_tasks_without_sprint(self):
        return self.tasks.filter(sprint_id=None)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        db_table = "board"

    def __unicode__(self):
        return u"%s" % (self.title.capitalize())

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=16)

    objects = GetOrNoneManager()

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        db_table = "tag"

    def __unicode__(self):
        return u"%s" % (self.name.capitalize())

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=512)
    order = models.IntegerField(default=0)
    points = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=12)
    sprint_id = models.ForeignKey(Sprint, null=True, db_column='sprint_id', related_name='tasks')
    board_id = models.ForeignKey(Board, db_column='board_id', related_name='tasks')

    task = models.ManyToManyField(Tag, through='TaskHasTag')

    objects = GetOrNoneManager()

    class Meta: 
        ordering = ['order', 'title']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = "task"

    def __unicode__(self):
        return u"%s" % (self.title.capitalize())

class TaskHasTag(models.Model):
    task_id = models.ForeignKey(Task, db_column='task_id')
    tag_id = models.ForeignKey(Tag, db_column='tag_id')

    class Meta:
        db_table = "task_has_tag"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1024)
    task_id = models.ForeignKey(Task, null=True, db_column='task_id')

    class Meta: 
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        db_table = "comment"

    def __unicode__(self):
        return u"%s" % (self.id)

class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name='custom_user')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128, blank=True)
    bio = models.CharField(max_length=512, blank=True)

    team = models.ManyToManyField(Team, through='UserHasTeam')
    speciality = models.ManyToManyField(Speciality, through='UserHasSpeciality')
    project = models.ManyToManyField(Project, through='UserHasProject')
    task = models.ManyToManyField(Task, through='UserHasTask')

    objects = GetOrNoneManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "custom_user"

    def __unicode__(self):
        return u"%s" % (self.user.username.lower())

class UserHasTask(models.Model):
    user_id = models.ForeignKey(CustomUser, db_column='user_id')
    task_id = models.ForeignKey(Task, db_column='task_id')
    onws = models.BooleanField(default=False)

    class Meta:
        db_table = "user_has_task"

class UserHasTeam(models.Model):
    user_id = models.ForeignKey(CustomUser, db_column='user_id')
    team_id = models.ForeignKey(Team, db_column='team_id')
    manages = models.BooleanField(default=False)

    class Meta:
        db_table = "user_has_team"

class UserHasSpeciality(models.Model):
    user_id = models.ForeignKey(CustomUser, db_column='user_id')
    speciality_id = models.ForeignKey(Speciality, db_column='speciality_id')

    class Meta:
        db_table = "user_has_speciality"

class UserHasProject(models.Model):
    user_id = models.ForeignKey(CustomUser, db_column='user_id')
    project_id = models.ForeignKey(Project, db_column='project_id')
    manages = models.BooleanField(default=False)

    class Meta:
        db_table = "user_has_project"

