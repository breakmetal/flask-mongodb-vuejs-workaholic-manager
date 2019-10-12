from bson.objectid import ObjectId
import datetime
from flask import Flask, jsonify, request
from app import mongo
from bson.json_util import dumps

class Project(object):
    
    def __init__(self,title ,description ):
        self.title = title
        self.created_at = datetime.datetime.utcnow()
        self.description = description

    def  insert(self):
        data = self.__dict__
        mongo.db.projects.insert_one(data)
        return 'ok'

    @staticmethod
    def get_all_projects():
        projects = mongo.db.projects.find() 
        json_str = dumps(projects)
        return json_str
    
    @staticmethod
    def update_project(id, kwargs):
        data = kwargs.get_json()
        return mongo.db.projects.update({"_id": ObjectId(id)}, {"$set": {"title": data['title'], "description": data['description']}} , upsert = True)

    @staticmethod
    def delete_project(id):
        mongo.db.projects.delete_one({"_id": ObjectId(id)})

    