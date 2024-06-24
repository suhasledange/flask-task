from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database('your_database_name')
task_collection = db['tasks']

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = list(task_collection.find().sort('createdAt', -1))
        for task in tasks:
            task['_id'] = str(task['_id'])
        return jsonify({'result': tasks})
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        task_data = request.json
        new_task = task_collection.insert_one(task_data)
        task_data['_id'] = str(new_task.inserted_id)
        return jsonify({'success': True, 'task': task_data}), 201
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 500

if __name__ == '__main__':
    app.run()
    
