from fastapi import APIRouter, Depends, HTTPException, status,BackgroundTasks
from fastapi.responses import StreamingResponse


stram_rt = APIRouter(
    prefix="/streams",
    tags=["streams"],
    responses={404: {"description": "Not found"}},
    )

bg_rt = APIRouter(
    prefix="/background",
    tags=["background"],
    responses={404: {"description": "Not found"}},
)

def send_main(email: str):
    print(f"Sending email to {email}...")
    return f"Email sent to {email}"

@stram_rt.get("/")
async def read_streams():
    def iterate_stream():
        for i in range(100):
            yield f"data: Stream item {i}\n\n"
    return StreamingResponse(iterate_stream(), media_type="text/event-stream")

@bg_rt.get("/")
async def read_background(bg: BackgroundTasks):
    def background_task():
        for i in range(100):
            print(f"Background task item {i}")
    mail = "hello.1@gmail.com"
    bg.add_task(send_main, email=mail)
    return {"message": "Background task started"}

