from flask_pymongo import PyMongo, ObjectId
from flask import Flask

bioapp = Flask(__name__)
bioapp.config["MONGO_URI"] = "mongodb://localhost:27017/agrobioapp"
mongodb_client = PyMongo(bioapp)
db = mongodb_client.db
