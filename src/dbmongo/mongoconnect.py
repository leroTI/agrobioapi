from flask_pymongo import PyMongo, ObjectId
from flask import Flask

bioapp = Flask(__name__)
# bioapp.config["MONGO_URI"] = "mongodb://mongodb:27017/agrobioapp?authSource=admin&readPreference=primary&appname=agrobioapi&ssl=false"
bioapp.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/agrobioapp?authSource=admin&readPreference=primary&appname=agrobioapi&ssl=false"
mongodb_client = PyMongo(bioapp)
db = mongodb_client.db
