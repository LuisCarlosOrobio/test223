import asyncio
import websockets
import ffmpeg
import json

async def process_audio(websocket, path):
    try:
        print("Connected to client")
        audio_chunks = bytearray()

        # Receive audio data from the client
        async for message in websocket:
            audio_chunk = json.loads(message)
            audio_chunks.extend(audio_chunk['data'])

            # Process the audio data using FFmpeg
            input_audio = ffmpeg.input('pipe:', format='wav')
            output_audio = ffmpeg.output(
                input_audio, 'pipe:', format='mulaw', acodec='pcm_mulaw', ar='8000'
            )
            out, _ = ffmpeg.run(output_audio, input=audio_chunks, capture_stdout=True, capture_stderr=True)

            # Send processed audio data to another server
            await send_to_server(out)

    except Exception as e:
        print(f"Exception occurred: {e}")

async def send_to_server(audio_bytes):
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as ws:
        for i in range(0, len(audio_bytes), 1024):
            message = {
                "event": "media",
                "sequenceNumber": str(i // 1024 + 1),
                "media": {
                    "track": "outbound",
                    "chunk": str(i // 1024 + 1),
                    "timestamp": str(i // 1024 * 125),
                    "payload": audio_bytes[i : i + 1024].hex(),
                },
                "streamSid": "MZ18ad3ab5a668481ce02b83e7395059f0",
            }
            await ws.send(json.dumps(message))
            print("Message sent to server")

start_server = websockets.serve(process_audio, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
