import os
import shutil
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from back.transcribe import router as transcribe_router
from back.transcripts import router as transcripts_router
from back.websocket import websocket_endpoint
from back.summarize import router as summarize_router
from back.mail_tasks import router as mail_tasks_router
from back.tasks import router as tasks_router

from back.database import Base, engine, SessionLocal, get_db  # Base & engine -> tabloları oluşturmak için, SessionLocal -> DB oturumu
import back.models  # modelleri import etmeliyiz ki Base.metadata.create_all çalışsın

# FastAPI & veritabanı işlemleri
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text  # Eğer raw SQL çalıştırmak istersen kullanılır

# Router'lar
from back.routers import meetings, participants, transcripts, summaries, tasks





app = FastAPI()

# Router'ları bağla
app.include_router(transcribe_router)
app.include_router(summarize_router)
app.include_router(mail_tasks_router)
app.include_router(tasks_router)

app.include_router(transcripts_router)
app.websocket("/ws")(websocket_endpoint)


# database ve modeller






# Router'ları bağla

app.include_router(meetings.router)
app.include_router(participants.router)
app.include_router(transcripts.router)
app.include_router(summaries.router)
app.include_router(tasks.router)





@app.get("/")
def hello():
    return {"message": "Merhaba"}

@app.get("/uploads")
def list_uploaded_files():
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        return {"files": []}
    
    files = os.listdir(upload_dir)
    return {"files": files}

@app.post("/uploads")
async def upload_audio(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"{file.filename} dosyası yüklendi"}

active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("WebSocket bağlandı")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Alınan mesaj: {data}")
            await websocket.send_text(f"Sunucu yanıtı: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("WebSocket bağlantısı kesildi")

# Bildirim fonksiyonu
