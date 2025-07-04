from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
events = db["events"]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data:
        events.insert_one({
            "event": data["event"],
            "author": data["author"],
            "from_branch": data.get("from_branch", ""),
            "to_branch": data.get("to_branch", ""),
            "timestamp": data["timestamp"]
        })
    return jsonify({"status": "success"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    latest_events = list(events.find().sort("timestamp", -1).limit(10))
    for event in latest_events:
        event["_id"] = str(event["_id"])
    return jsonify(latest_events)

if __name__ == '__main__':
    app.run(port=5000)
