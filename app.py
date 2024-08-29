from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort, render_template
from flask_pymongo import PyMongo
from prometheus_client import Gauge, generate_latest
from prometheus_client.exposition import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os
from bson import ObjectId
import json
from src.validators import validate_video_request, validate_video_id, ValidationError

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")


print("HERE WE ARE: ")
print(app.config["MONGO_URI"])

app.config["FLASK_ENV"] = os.getenv("FLASK_ENV", "DEV")
app.config["HOST"] = os.getenv("HOST", "0.0.0.0")
app.config["VIDEOS_APP_PORT_INTERNAL"] = os.getenv("VIDEOS_APP_PORT_INTERNAL", "5000")

mongo = PyMongo(app)

# Prometheus metrics
VIDEO_COUNT = Gauge('video_count', 'Total number of videos')

def mongo_to_json(document):
    if isinstance(document, ObjectId):
        return str(document)
    if isinstance(document, dict):
        return {k: mongo_to_json(v) for k, v in document.items()}
    if isinstance(document, list):
        return [mongo_to_json(i) for i in document]
    return document


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/videos', methods=['GET'])
def get_all_videos():
    try:
        videos = mongo.db.videos.find()
        video_list = [mongo_to_json(video) for video in videos]
        return jsonify(video_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/videos/<string:video_id>', methods=['GET'])
def get_video(video_id):
    try:
        validate_video_id(video_id)
        video = mongo.db.videos.find_one_or_404({"_id": ObjectId(video_id)})
        return jsonify(mongo_to_json(video))
    except ValidationError as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/videos', methods=['POST'])
def create_video():
    try:
        validate_video_request(request)
        video = {
            'title': request.json['title'],
            'description': request.json.get('description', ""),
        }
        result = mongo.db.videos.insert_one(video)
        return jsonify({"_id": str(result.inserted_id)}), 201
    except ValidationError as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/videos/<string:video_id>', methods=['PUT'])
def update_video(video_id):
    try:
        validate_video_id(video_id)
        validate_video_request(request)
        video = mongo.db.videos.find_one_or_404({"_id": ObjectId(video_id)})
        update_data = request.json
        mongo.db.videos.update_one({"_id": ObjectId(video_id)}, {"$set": update_data})
        return jsonify({"_id": video_id})
    except ValidationError as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/videos/<string:video_id>', methods=['DELETE'])
def delete_video(video_id):
    try:
        validate_video_id(video_id)
        result = mongo.db.videos.delete_one({"_id": ObjectId(video_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Video not found"}), 404
        return jsonify({"result": "deleted"})
    except ValidationError as e:
        return jsonify({"error": e.message}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthcheck')
def healthcheck():
    return '', 200

@app.route('/metrics')
def metrics():
    VIDEO_COUNT.set(mongo.db.videos.count_documents({}))
    return generate_latest()

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["VIDEOS_APP_PORT_INTERNAL"], debug=False)

