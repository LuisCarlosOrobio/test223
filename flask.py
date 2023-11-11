from flask import Flask, request, jsonify, render_template
import requests
import base64
import uuid
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio']

    # Convert the audio file to a hex string (or your required format)
    audio_hex = base64.b64encode(audio_file.read()).decode('utf-8')

    # Generate a UUID for the track
    track_id = str(uuid.uuid4())

    # Get the current timestamp in ISO 8601 format
    current_timestamp = datetime.utcnow().isoformat() + 'Z'

    # Prepare the payload with the generated track ID and current timestamp
    payload = {
        "media": {
            "track": track_id,
            "timestamp": current_timestamp,
            "payload": audio_hex
        },
        "sequenceNumber": "0"  # Adjust as per your requirements
    }

    # Forward the formatted data to your main server
    server_url = 'http://localhost:8080/'  # Adjust if your API endpoint is different
    response = requests.post(server_url, json=payload)

    # Check if the request to the main server was successful
    if response.status_code == 200:
        # Return the response from your main server to the frontend
        return jsonify(response.json())
    else:
        return jsonify({"error": "Error communicating with the main server"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)
