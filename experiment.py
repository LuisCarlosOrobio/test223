import base64
import requests

with open("image.jpg", "rb") as image_file:
    base64_string = base64.b64encode(image_file.read()).decode()

url = "http://127.0.0.1:5000/completion"
headers = {
        "Content-Type": "application/json"
}
data = {
        "prompt": "Describe the image: [img-1]",
        "image_data": [
            {"data": base64_string, "id": 1}
        ]
}

response = requests.post(url, headers=headers, json=data)

try:
    response_json = response.json()
    print(response_json)
except requests.exceptions.JSONDecodeError:
    print(f"Failed to decode JSON. Status code: {response.status_code}\nResponse content:\n{response.text}")
