from fastapi import APIRouter, Form, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from uuid import UUID
import whisper
import os
from sqlalchemy.orm import Session


from back.database import get_db
from back import crud, schemas

from back.websocket import notify_clients

router = APIRouter()

class Transcriber:
    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe_audio(self, path: str) -> str:
        result = self.model.transcribe(path, language="en")
        return result["text"]

transcriber = Transcriber()

@router.post("/transcribe")
async def transcribe_endpoint(
    
    meeting_id: UUID = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # 🔧 Geçici dosyaya kaydet
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # 🎙️ Transkript üret
        text = transcriber.transcribe_audio(temp_path)
        os.remove(temp_path)

        # 🧠 Meeting ID'yi frontend'den alman gerekiyor, şimdilik örnek UUID kullanalım
          # TODO: Flutter'dan alınmalı

        # 📦 ORM ile kaydet
        transcript_data = schemas.TranscriptCreate(
            filename=file.filename,
            content=text,
            meeting_id=meeting_id
        )

        await notify_clients("yeni_transkript")

        new_transcript = crud.create_transcript(db, transcript_data)
        return new_transcript

        
        
        return JSONResponse(content={"status": "success", "message": "Transkript başarıyla kaydedildi."})

    except Exception as e:
         print("HATA:", e)  
         return JSONResponse(status_code=500, content={"error": str(e)})
