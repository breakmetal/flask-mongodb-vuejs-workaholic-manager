from bson.objectid import ObjectId
import datetime
from flask import Flask, jsonify, request
from app import mongo
from bson.json_util import dumps
from bson.json_util import DEFAULT_JSON_OPTIONS


class Task(object):

    def __init__(self,kwargs):
        id = kwargs['project_id']
        self.project_id = ObjectId( ObjectId(id))
        self.title = kwargs["title"]
        self.created_at = datetime.datetime.utcnow()
        self.date_limit = kwargs["date_limit"]
        self.description = kwargs["description"]

    
    @staticmethod
    def get_all_tasks(id):
        tasks = mongo.db.tasks.find({ "project_id": ObjectId(id) }) 
        DEFAULT_JSON_OPTIONS.datetime_representation = 2
        json_str = dumps(tasks)
        return json_str

    @staticmethod
    def get_one(id):
        task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
        return task
    
    def  insert(self):
        data = self.__dict__
        mongo.db.tasks.insert_one(data)

    @staticmethod
    def insert_sub_task(kwargs):
        id = kwargs['idTask']
        #data = {"title" : 'hola', "description": "adios"}
        #mongo.db.tasks.update({"title": 'working hard'}, {'$push':{"sub-task": {'$each': [data]}}})
        #mongo.db.tasks.update({"_id": ObjectId(id)}, {'$push':{"sub-task": {"title": 'it is live'}}})
        #mongo.db.tasks.update({"title": 'Analisis de requerimiento'},{'$push':{"sub-task": {"title" : 'ok, its work' }})
        mongo.db.tasks.update({"_id": ObjectId(id)}, {'$push':{"subTasks": {"title": kwargs['title'],"description": kwargs['description']}}})
        return 'hi'

    def update_sub_task(self, parameter_list):
        mongo.db.tasks.update({"title": 'working hard'}, {'$set':{"sub-task":[ {"title": 'I fine'}]}})
        return 'hi'

        