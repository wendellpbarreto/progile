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

logger = logging.getLogger(__name__)

STATES = (
    ("AC", "AC"),
    ("AL", "AL"),
    ("AP", "AP"),
    ("AP", "AP"),
    ("BA", "BA"),
    ("CE", "CE"),
    ("DF", "DF"),
    ("GO", "GO"),
    ("ES", "ES"),
    ("MA", "MA"),
    ("MT", "MT"),
    ("MS", "MS"),
    ("MG", "MG"),
    ("PA", "PA"),
    ("PB", "PB"),
    ("PR", "PR"),
    ("PE", "PE"),
    ("PI", "PI"),
    ("RJ", "RJ"),
    ("RN", "RN"),
    ("RS", "RS"),
    ("RO", "RO"),
    ("RR", "RR"),
    ("SP", "SP"),
    ("SC", "SC"),
    ("SE", "SE"),
    ("TO", "TO"),
)

class Organization(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        db_table = "organization"

    def __unicode__(self):
        return u"%s" % (self.name.lowercase())

class Speciality(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    class Meta:
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"
        db_table = "speciality"

    def __unicode__(self):
        return u"%s" % (self.name.lowercase())

class User(models.Model):
    CPF = models.CharField(max_length=11, primary_key=True)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=16)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    bio = models.CharField(max_length=512)
    user_has_organization = models.ManyToManyField(Organization, through='UserHasOrganization')
    user_has_speciality = models.ManyToManyField(Speciality, through='UserHasSpeciality')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    def __unicode__(self):
        return u"%s" % (self.email.lowercase())

class UserHasOrganization(models.Model):
    user_CPF = models.ForeignKey(User, db_column='user_CPF')
    organization_name = models.ForeignKey(Organization, db_column='organization_name')

class UserHasSpeciality(models.Model):
    user_CPF = models.ForeignKey(User, db_column='user_CPF')
    speciality_name = models.ForeignKey(Speciality, db_column='speciality_name')

class Visibility(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    
    class Meta:
        verbose_name = "Visibility"
        verbose_name_plural = "Visibilities"
        db_table = "visibility"

    def __unicode__(self):
        return u"%s" % (self.name.lowercase())

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    organization_name = models.ForeignKey(Organization, null=True)
    visibility_name = models.ForeignKey(Visibility)
    project_has_user = models.ManyToManyField(User, through='ProjectHasUser')

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        db_table = "project"

    def __unicode__(self):
        return u"%s" % (self.name.lowercase())

class ProjectHasUser(models.Model):
    user_CPF = models.ForeignKey(User, db_column='user_CPF')
    project_id = models.ForeignKey(Project, db_column='project_id')
    manages = models.BooleanField(default=False)

class Sprint(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=124)
    description = models.CharField(max_length=512)
    order = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    project = models.ForeignKey(Project)

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
    project = models.ForeignKey(Project)
    
    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        db_table = "board"

    def __unicode__(self):
        return u"%s" % (self.title.capitalize())

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=16)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        db_table = "tag"

    def __unicode__(self):
        return u"%s" % (self.name.capitalize())

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=124)
    description = models.CharField(max_length=512)
    points = models.IntegerField()
    sprint_id = models.ForeignKey(Sprint, null=True)
    board_id = models.ForeignKey(Board)
    task_has_tag = models.ManyToManyField(Tag, through='TaskHasTag')

    class Meta: 
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = "task"

    def __unicode__(self):
        return u"%s" % (self.title.capitalize())

class TaskHasTag(models.Model):
    task_id = models.ForeignKey(Task, db_column='task_id')
    tag_id = models.ForeignKey(Tag, db_column='tag_id')




