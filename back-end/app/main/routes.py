from flask import Flask, jsonify, render_template, request, url_for
from . import main
from ..models.task import Task
from ..models.project import Project

@main.route('/')
def index():
    response = Task.get_all_tasks()
    return response

@main.route('/form_task', methods = ["GET"])
def form():
    return """
    <form method="post"  action="/add_task">
        <input type="text" name="title">
        <input type="date" name="date_limit" id="txt2">
        <input type="text" name="description" id="txt3">  
        <input type="submit">
    </form>"""


@main.route('/add_task', methods = ["POST"])
def addTask():
    
    newTask = Task(request.form)
    newTask.insert()
    return "listo"

###############################################
@main.route('/form_sub_task', methods = ["GET"])
def form_sub_task():
    return """
    <form method="post"  action="/add_sub_task">
        <input type="text" name="title">
        <input type="date" name="date_limit" id="txt2">
        <input type="text" name="description" id="txt3">  
        <input type="submit">
    </form>"""

@main.route('/add_sub_task', methods = ["POST"])
def addSubTask():
    id = "5d9217b53a42882864214a42"
    response = Task.insert_sub_task(id, request.form)
    return response

############################
###### API for projects#####
############################

@main.route('/api/list_projects', methods = ['GET'])
def listProjects():
    response = Project.get_all_projects()
    return response

@main.route('/api/add_project', methods = ["POST"])
def addProject():
    obj = request.get_json()
    newProject = Project(obj['title'], obj['description'])
    return newProject.insert()
    

@main.route('/api/update_project/<id>', methods = ['PUT'])
def updateProject(id):
    project = request
    return Project.update_project(id, project)


@main.route('/api/delete_project/<id>', methods = ['DELETE'])
def deleteProject(id):
    Project.delete_project(id)
    return 'ok'