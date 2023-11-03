from flask import Flask, request, jsonify
import base64
import requests

app = Flask(__name__)

@app.route('/completion', methods=['POST'])
def completion():
    # Convert the image to a base64 string
    with open("path_to_your_image.jpg", "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode()

    # Define the URL and the data payload for the POST request
    url = "https://933c-136-56-201-191.ngrok-free.app"  # Removed '/completion'
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": "Describe the image: [img-1]",
        "image_data": [
            {"data": base64_string, "id": 1}
        ]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the response contains valid JSON
    try:
        response_json = response.json()
        return jsonify(response_json), response.status_code
    except requests.exceptions.JSONDecodeError:
        return f"Failed to decode JSON. Status code: {response.status_code}\nResponse content:\n{response.text}", response.status_code

if __name__ == '__main__':
    app.run(debug=True)
