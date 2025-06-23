from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import whisper
import shutil
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set to your React origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = whisper.load_model("base")  # you can use "tiny", "small", "medium", "large"

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    temp_filename = f"temp_{uuid.uuid4()}.mp3"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = model.transcribe(temp_filename)
    os.remove(temp_filename)

    return {"text": result["text"]}
