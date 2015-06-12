#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import operator
import datetime

from django.shortcuts import render
from itertools import chain
from django.db.models import F, Q
from django.contrib.auth.models import User
from .generic_view import GenericView
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

class GUI(GenericView):

    def __init__(self):
        pass

    def new_sprint(self, request):
        data = None

        print request.POST
        if request.method == "POST":
            try:
                project_id = request.POST['project_id']
                project_id = Project.objects.raw('SELECT * FROM project WHERE id = %s', [project_id])[0].id

                title = request.POST['title']
                start_date = datetime.datetime.strptime(request.POST['start_date_submit'], "%Y/%m/%d").date()
                end_date = datetime.datetime.strptime(request.POST['end_date_submit'], "%Y/%m/%d").date()
                description = request.POST['description']
                order = request.POST['order']
                
       
                sprint = Sprint.objects.raw('INSERT INTO "sprint" ("title", "start_date", "end_date", "description", "order", "project_id") VALUES (%s, %s, %s, %s, %s, %s) RETURNING sprint.id', [title, start_date, end_date, description, order, project_id])[0]
            except Exception, e:
                logger.error(str(e))

                data = {
                    'leftover' : {
                        'alert-error' : 'Cannot create board.',
                    }
                }

            data = {
                'leftover' : {
                    'alert-success' : 'Board ' + title + ' succefully created.',
                    'redirect' : '/sprints/' + str(project_id),
                }
            }
            

        return data

    def sprints(self, request):
        data = None

        try:
            pk = self.kwargs['pk']
            project = Project.objects.raw('SELECT * FROM project WHERE id = %s', [pk])[0]
            boards = Board.objects.raw('SELECT * FROM board WHERE project_id = %s', [project.id])
        except Exception, e:
            logger.error(str(e))

            data = {
                    'leftover' : {
                        'alert-error' : 'No project found.',
                    }
                }
        else:
            data = {
                'template' : {
                    'project' : project,
                    'boards' : boards,
                }
            }

        return data

    def new_task(self, request):
        data = None
        logger.info(request.POST)

        try:
            sprint_id = request.POST['sprint_id']
            sprint_id = Sprint.objects.raw('SELECT * FROM sprint WHERE id = %s', [sprint_id])[0].id
        except Exception, e:
            logger.warning(str(e))

            sprint_id = None

        try:
            title = request.POST['title']
            description = request.POST['description']
            points = request.POST['points']
            order = request.POST['order']
            status = request.POST['status']
            from_page = request.POST['from_page']

            board_id = request.POST['board_id']
            project_id = request.POST['project_id']
        except Exception, e:
            logger.error(str(e))

            data = {
                'leftover' : {
                    'alert-error' : 'Something went wrong :(',
                }
            }
        else:
            if request.method == "POST" and title:
                try:
                    task = Task.objects.raw('INSERT INTO "task" ("title", "description", "points", "order", "status", "sprint_id", "board_id") VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING task.id', [title, description, points, int(order), status, sprint_id, int(board_id)])[0]
                except Exception, e:
                    logger.error(str(e))

                    data = {
                        'leftover' : {
                            'alert-error' : 'Cannot create task.',
                        }
                    }

                data = {
                    'leftover' : {
                        'alert-success' : 'Task ' + title + ' succefully created.',
                        'redirect' : '/' + from_page + '/' + project_id,
                    }
                }
            else:
                data = {
                    'leftover' : {
                        'alert-error' : 'Task title is mandatory.',
                    }
                }

        return data
             
    def update_task(self, request):
        data = None

        if request.method == 'GET':
            print request.GET

            try:
                task_id = request.GET['task_id']
                order = request.GET['order']
                Task.objects.filter(id=task_id).update(order=order)
            except Exception, e:
                logger.error(str(e))

                data = {
                        'leftover' : {
                            'alert-error' : 'Something went wrong :(',
                        }
                    }

            try:
                task_id = request.GET['task_id']
                board_id = request.GET['board_id']
                Task.objects.filter(id=task_id).update(board_id=board_id)
            except Exception, e:
                logger.error(str(e))

                data = {
                        'leftover' : {
                            'alert-error' : 'Something went wrong :(',
                        }
                    }

            try:
                order = request.GET['order']
            except Exception, e:
                logger.error(str(e))

                order = 0

            try:
                task_id = request.GET['task_id']
                sprint_id = request.GET['sprint_id'] if request.GET['sprint_id'] != '0' else None
                Task.objects.filter(id=task_id).update(sprint_id=sprint_id, order=order)
            except Exception, e:
                logger.error(str(e))

                data = {
                        'leftover' : {
                            'alert-error' : 'Something went wrong :(',
                        }
                    }

        elif request.method == 'POST':
            try:
                task_id = request.POST['task_id']
                title = request.POST['title']
                description = request.POST['description']
                points = request.POST['points']
                order = request.POST['order']
                status = request.POST['status']

                from_page = request.POST['from_page']

                board_id = request.POST['board_id']
                project_id = request.POST['project_id']
            except Exception, e:
                logger.error(str(e))

                data = {
                    'leftover' : {
                        'alert-error' : 'Something went wrong :(',
                    }
                }
            else:
                task = Task.objects.raw('UPDATE "task" SET "title" = %s, "description" = %s, "points" = %s, "order" = %s, "status" = %s, "board_id" = %s WHERE "id" = %s RETURNING task.id', [title, description, points, order, status, int(board_id), task_id])[0]

                data = {
                    'leftover' : {
                        'alert-success' : 'Task ' + title + ' succefully created.',
                        'redirect' : '/' + from_page + '/' + project_id,
                    }
                }

        return data

    def projects(self, request):
        projects = Project.objects.raw('SELECT * FROM project JOIN user_has_project ON project.id = user_has_project.project_id WHERE user_has_project.user_id = %s', [request.user.custom_user.id])

        return {
            'template' : {
                'projects' : projects,
            }
        }

    def project(self, request):
        data = None

        try:
            pk = self.kwargs['pk']
            project = Project.objects.raw('SELECT * FROM project WHERE id = %s', [pk])[0]
            boards = Board.objects.raw('SELECT * FROM board WHERE project_id = %s', [project.id])
        except Exception, e:
            logger.error(str(e))

            data = {
                    'leftover' : {
                        'alert-error' : 'No project found.',
                    }
                }
        else:
            data = {
                'template' : {
                    'project' : project,
                    'boards' : boards,
                }
            }

        return data

    def new_project(self, request):
        data = None
        teams = Team.objects.raw('SELECT * FROM team')

        if request.method == "POST":
            try:
                visibility = request.POST['visibility']
            except Exception, e:
                logger.info(str(e))

                visibility = False

            try:
                name = request.POST['name']
                team_id = request.POST['team_id']
                description = request.POST['description']
            except Exception, e:
                logger.error(str(e))

                data = {
                    'leftover' : {
                        'alert-error' : 'Something went wrong :(',
                    }
                }
            else:
                if name:
                    try:
                        team = Team.objects.raw('SELECT * FROM team WHERE id = %s', [team_id])[0].id
                    except Exception, e:
                        logger.info(str(e))

                        team = None

                    try:
                        project_id = Project.objects.raw('INSERT INTO project (name, team_id, visibility, description) VALUES (%s, %s, %s, %s) RETURNING project.id', [name, team, visibility, description])[0].id
                        user_id = CustomUser.objects.raw('SELECT * FROM custom_user WHERE user_id = %s', [request.user.id])[0].id
                        UserHasProject.objects.raw('INSERT INTO user_has_project (user_id, project_id, manages) VALUES (%s, %s, true) RETURNING user_has_project.id', [user_id, project_id])[0]
                        board1 = Board.objects.raw('INSERT INTO "board" ("title", "order", "project_id") VALUES (%s, %s, %s) RETURNING board.id', ["To Do", 1, project_id])[0]
                        board2 = Board.objects.raw('INSERT INTO "board" ("title", "order", "project_id") VALUES (%s, %s, %s) RETURNING board.id', ["Doing", 2, project_id])[0]
                        board3 = Board.objects.raw('INSERT INTO "board" ("title", "order", "project_id") VALUES (%s, %s, %s) RETURNING board.id', ["Done", 3, project_id])[0]
                    except Exception, e:
                        logger.error('- ' * 20)
                        logger.error(str(e))

                        data = {
                            'leftover' : {
                                'alert-error' : 'Project name is already taken.',
                            }
                        }

                    data = {
                        'leftover' : {
                            'alert-success' : 'Project ' + name + ' succefully created.',
                            'redirect' : '/projects/',
                        }
                    }
                else:
                    data = {
                        'leftover' : {
                            'alert-error' : 'Project name is mandatory.',
                        }
                    }

        elif request.method == "GET":
            data = {
                'template' : {
                    'teams' : teams,
                }
            }

        return data

    def new_board(self, request):
        data = None

        try:
            project_id = request.POST['project_id']
            title = request.POST['title']

            project_id = Project.objects.raw('SELECT * FROM project WHERE id = %s', [project_id])[0].id
        except Exception, e:
            logger.error(str(e))

            data = {
                'leftover' : {
                    'alert-error' : 'Something went wrong :(',
                }
            }
        else:
            if request.method == "POST" and title:
                try:
                    boards = Board.objects.raw('SELECT * FROM board WHERE project_id = %s', [project_id])
                    boards_quantity = sum(1 for board in boards)
                    board = Board.objects.raw('INSERT INTO "board" ("title", "order", "project_id") VALUES (%s, %s, %s) RETURNING board.id', [title, boards_quantity + 1, project_id])[0]
                except Exception, e:
                    logger.error(str(e))

                    data = {
                        'leftover' : {
                            'alert-error' : 'Cannot create board.',
                        }
                    }

                data = {
                    'leftover' : {
                        'alert-success' : 'Board ' + title + ' succefully created.',
                        'redirect' : '/boards/' + str(project_id),
                    }
                }
            else:
                data = {
                    'leftover' : {
                        'alert-error' : 'Board title is mandatory.',
                    }
                }

        return data
    
    def update_board(self, request):
        data = None

        if request.method == 'GET':
            try:
                board_id = request.GET['board_id']
                order = request.GET['order']
                Board.objects.filter(id=board_id).update(order=order)
            except Exception, e:
                logger.error(str(e))

                data = {
                        'leftover' : {
                            'alert-error' : 'Something went wrong :(',
                        }
                    }
        elif request.method == 'POST':
            try:
                sprint_id = request.POST['sprint_id']
                sprint_id = Sprint.objects.raw('SELECT * FROM sprint WHERE id = %s', [sprint_id])[0].id
            except Exception, e:
                logger.warning(str(e))

                sprint_id = None

            try:
                title = request.POST['title']
                description = request.POST['description']
                points = request.POST['points']

                board_id = request.POST['board_id']
                project_id = request.POST['project_id']
            except Exception, e:
                logger.error(str(e))

                data = {
                    'leftover' : {
                        'alert-error' : 'Something went wrong :(',
                    }
                }
            else:
                if request.method == "POST" and title:
                    try:
                        task = Task.objects.raw('INSERT INTO "task" ("title", "description", "points", "sprint_id", "board_id") VALUES (%s, %s, %s, %s, %s) RETURNING task.id', [title, description, points, int(sprint_id), int(board_id)])[0]
                    except Exception, e:
                        logger.error(str(e))

                        data = {
                            'leftover' : {
                                'alert-error' : 'Cannot create task.',
                            }
                        }

                    data = {
                        'leftover' : {
                            'alert-success' : 'Task ' + title + ' succefully created.',
                            'redirect' : '/boards/' + project_id,
                        }
                    }
                else:
                    data = {
                        'leftover' : {
                            'alert-error' : 'Task title is mandatory.',
                        }
                    }

        return data

    def home(self, request):
        data = None

        if request.user.is_authenticated():
            data = {
                'leftover' : {
                    'redirect' : '/projects/',
                }
            }
        else:
            data = {
                'template' : {
                    'title' : 'Progile | Home',
                }
            }

        return data

    def boards(self, request):
        data = None

        try:
            pk = self.kwargs['pk']
            project = Project.objects.raw('SELECT * FROM project WHERE id = %s', [pk])[0]
            boards = Board.objects.raw('SELECT * FROM board WHERE project_id = %s', [project.id])
        except Exception, e:
            logger.error(str(e))

            data = {
                    'leftover' : {
                        'alert-error' : 'No project found.',
                    }
                }
        else:
            data = {
                'template' : {
                    'project' : project,
                    'boards' : boards,
                }
            }

        return data

    def signin(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if first_name and username and email and password:
            user = None

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                custom_user, created = CustomUser.objects.get_or_create(user=user, first_name=first_name, last_name=last_name)
            except Exception, e:
                logger.error(str(e))

            if user:
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)

                    data = {
                        'leftover' : {
                            'alert-success' : 'Account created succefully!',
                            'redirect' : '/projects/'
                        },
                    }
                else:
                    data = {
                        'leftover' : {
                            'alert-error' : 'Something went wrong :(',
                        },
                    }
            else:
                data = {
                    'leftover' : {
                        'alert-error' : 'Username/Email already registered. Try again with another username/email please.',
                    },
                }

        else:
            logger.info("Missing required informations!");

            data = {
                'leftover' : {
                    'alert-error' : 'Missing required informations.',
                },
            }

        return data

    def login(self, request):
        data = None
        user = None

        username = request.POST['username']
        password = request.POST['password']

        try:
            user = authenticate(username=username, password=password)
        except Exception, e:
            logger.error(str(e))

        if user is not None:
            login(request, user)

            data = {
                'leftover' : {
                    'alert-success' : 'Welcome back :)',
                    'redirect' : '/projects/'
                },
            }

        else:
            data = {
                'leftover' : {
                    'alert-error' : 'Invalid login/pass. Try again please.',
                },
            }

        return data

    def logout(self, request):
        try:
            logout(request)
        except Exception, e:
            logger.error(str(e))

        return {
            'leftover' : {
                'redirect' : '/home/',
            },
        }
