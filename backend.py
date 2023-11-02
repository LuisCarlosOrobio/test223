from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    
    # If the user does not select a file, the browser might submit an empty file without a filename
    if file.filename == '':
        return 'No selected file'
    if file:
        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Retrieve and print the text prompt
        textprompt = request.form['textprompt']
        print(f"Received text prompt: {textprompt}")
        
        return 'File and text prompt uploaded successfully!'

if __name__ == '__main__':
    app.run(port=5000)
