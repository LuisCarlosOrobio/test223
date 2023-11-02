from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # get the text prompt from the form
        textprompt = request.form.get("textprompt")

        # You might want to handle the image data as well, but for simplicity, I'm focusing on the text prompt.

        # Construct the payload for Llama server
        payload = {
            "prompt": textprompt,
            "n_predict": 128  # or whatever value you prefer
        }

        # make a POST request to the Llama server
        response = requests.post("http://127.0.0.1:5000/completion", json=payload)

        # For debugging purposes:
        print(response.text)

        # You can process the response from the Llama server and return something meaningful to the client
        try:
            json_data = response.json()
            # You might want to process json_data further, extract the content or handle errors.
            return jsonify(json_data)
        except Exception as e:
            return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)

