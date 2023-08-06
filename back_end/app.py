from flask import Flask, request, make_response, redirect, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from queue import Queue
from database import get_document, update_database

index = -1

app = Flask(__name__)
CORS(app)


@app.route('/getDocument', methods=['GET'])
def get_one_document():
    global index
    index += 1
    return jsonify(get_document(index))  # 改哪个角色前端自己处理。


@app.route('/updateDatabase', methods=['POST'])
def update_one_database():
    data = request.get_json()
    update_database(data['id'], data['role'], data['response'], name=data['name'])
    return jsonify({"message": "Success"})


@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    print(data)
    return jsonify({"message": "Success"})

if __name__ == '__main__':
    app.run(port=5000)
