from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handling the image and text data
    image = request.files['image']
    textprompt = request.form['textprompt']

    # For this example, we'll save the image locally, but you can handle it as required
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    # Forward the data to the "llama server"
    with open(image_path, 'rb') as img_file:
        response = requests.post("http://localhost:5000/upload", data={'textprompt': textprompt}, files={'image': img_file})

    # Return the response from the "llama server" or handle as required
    return response.content

if __name__ == '__main__':
    app.run(port=5001)
