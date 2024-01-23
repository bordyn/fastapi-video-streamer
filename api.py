import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from video import VideoStreamer
from http import HTTPStatus
from fastapi.responses import StreamingResponse, Response
from contextlib import asynccontextmanager

video_streamer: Optional[VideoStreamer] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global video_streamer
    video_streamer = VideoStreamer(os.environ["VIDEO_SOURCE"])
    yield
    await video_streamer.release()

app = FastAPI(lifespan=lifespan)

async def video_streaming():
    # simplified version from 
    # https://github.com/mpimentel04/rtsp_fastapi/blob/master/webstreaming.py
    while True:
        frame = await video_streamer.read()
        if not frame:
            raise GeneratorExit
        yield b''.join(
            [
                b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n',
                frame,
                b'\r\n'
            ]
        )
    
@app.get("/video")
async def video_endpoint():
    return StreamingResponse(
        video_streaming(), 
        media_type="multipart/x-mixed-replace;boundary=frame"
    )

@app.get("/image")
async def image_endpoint():
    frame = await video_streamer.read()
    if frame is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Unable to retrieve frame",
        )
    return Response(
        content=frame, media_type="image/png"
    )
