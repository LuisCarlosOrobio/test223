from fastapi import FastAPI, UploadFile, File, WebSocket, HTTPException
from starlette.responses import HTMLResponse
import base64
import uuid
from datetime import datetime

app = FastAPI()

# Serve the HTML page
@app.get('/')
async def get():
    with open('index.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# WebSocket route
@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            data = await websocket.receive_text()
            # Here you would handle incoming messages
            # For example, echo the message back to the client
            await websocket.send_text(f"Message text was: {data}")
        except Exception as e:
            print(f"Error: {e}")
            break

# Handle the audio upload
@app.post('/upload')
async def upload_audio(audio: UploadFile = File(...)):
    try:
        audio_content = await audio.read()
        audio_hex = base64.b64encode(audio_content).decode('utf-8')
        track_id = str(uuid.uuid4())
        current_timestamp = datetime.utcnow().isoformat() + 'Z'

        # Since we cannot create a new WebSocket connection inside a regular HTTP endpoint,
        # you would need to handle the WebSocket communication in the '/ws' route.
        # The '/upload' endpoint would typically be used to handle file uploads only.
        
        # Return a response indicating the WebSocket path to connect to
        return {"websocket_route": "/ws", "track_id": track_id, "timestamp": current_timestamp, "audio_hex": audio_hex}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
