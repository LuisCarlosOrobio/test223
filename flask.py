from fastapi import FastAPI, UploadFile, File, WebSocket
from starlette.responses import HTMLResponse
import base64
import uuid
from datetime import datetime
import asyncio

app = FastAPI()

# Serve the HTML page
@app.get('/')
async def get():
    with open('index.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Handle the audio upload
@app.post('/upload')
async def upload_audio(audio: UploadFile = File(...)):
    audio_content = await audio.read()

    # Convert the audio file to a hex string
    audio_hex = base64.b64encode(audio_content).decode('utf-8')

    # Generate a UUID for the track
    track_id = str(uuid.uuid4())

    # Get the current timestamp in ISO 8601 format
    current_timestamp = datetime.utcnow().isoformat() + 'Z'

    # Prepare the payload
    payload = {
        "media": {
            "track": track_id,
            "timestamp": current_timestamp,
            "payload": audio_hex
        },
        "sequenceNumber": "0"
    }

    # Connect to the WebSocket server and send the data
    async with WebSocket(f'ws://localhost:8080/') as websocket:
        await websocket.send_json(payload)
        response = await websocket.receive_json()
        return response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
