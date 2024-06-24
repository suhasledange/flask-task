from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongo_uri)
db = client.get_database('taskDB') 
task_collection = db['tasks']

@app.route('/')
def home():
    return 'Task Web Application Home route'


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

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task_id = ObjectId(task_id)
        updated_data = request.json
        updated_task = task_collection.find_one_and_update(
            {'_id': task_id},
            {'$set': updated_data},
            return_document=True
        )

        if updated_task:
            updated_task['_id'] = str(updated_task['_id'])
            return jsonify({'success': True, 'task': updated_task})
        else:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 500

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task_id = ObjectId(task_id)
        deleted_task = task_collection.find_one_and_delete({'_id': task_id})

        if deleted_task:
            deleted_task['_id'] = str(deleted_task['_id'])
            return jsonify({'success': True, 'task': deleted_task})
        else:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 500


if __name__ == '__main__':
    app.run()
