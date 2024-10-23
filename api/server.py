from flask import Flask, jsonify, request
import redis
import json

app = Flask(__name__)

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


@app.route('/set', methods=['POST'])
def set_key():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    
    if not key or not value:
        return jsonify({"error": "Key and value required"}), 400
    
    try:
        redis_client.set(key, json.dumps(value))
        return jsonify({"message": f"Key {key} set with value: {json.dumps(value)}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get/<key>', methods=['GET'])
def get_key(key):
    try:
        value = redis_client.get(key)
        if value:
            json_value = json.loads(value)
            return jsonify({"key": key, "value": json_value}), 200
        else:
            return jsonify({"error": f"Key {key} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete/<key>', methods=['DELETE'])
def delete_key(key):
    try:
        result = redis_client.delete(key)
        if result == 1:
            return jsonify({"message": f"Key {key} deleted"}), 200
        else:
            return jsonify({"error": f"Key {key} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)