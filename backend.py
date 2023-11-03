from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Parse the incoming JSON data
        incoming_data = request.json

        # Extract the text prompt
        textprompt = incoming_data["prompt"]

        # Extract images (if any)
        images = incoming_data.get("image_data", [])
        
        # Process the images to construct the expected payload for Llama server
        image_data_list = []
        for img in images:
            split_result = textprompt.split(f"[img-{img['id']}]")
            image_data_list.append({
                "id": str(img["id"]),  # Converting ID to string
                "prefix": split_result[0]
            })
            textprompt = split_result[1] if len(split_result) > 1 else ""

        # Construct the payload for Llama server
        payload = {
            "prompt": textprompt,  
            "image_data": image_data_list
        }

        # Enhanced Logging: Print the payload to ensure it's constructed correctly
        print("Constructed Payload for Llama Server:", payload)

        try:
            # Make a POST request to the Llama server
            response = requests.post("http://127.0.0.1:5000/completion", json=payload)
            
            # For debugging purposes:
            print("Response from Llama Server:", response.text)
            
            # Process the response from the Llama server and return something meaningful to the client
            json_data = response.json()
            return jsonify(json_data)
        except requests.RequestException as re:
            print(f"Request Error: {str(re)}")
            return f"An error occurred with the request: {str(re)}", 500
        except Exception as e:
            print(f"General Error: {str(e)}")
            return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
