from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import psycopg2


router = APIRouter()

class Summarizer:
    def __init__(self, model: str = "mistral"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def db_connection(self):
        return psycopg2.connect(
            dbname="toplantidb",
            user="postgres",
            password="230565",
            host="localhost"
        )
    
    def fetch_transcript(self, meeting_id: str) -> str:
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute("SELECT content FROM transcripts WHERE meeting_id = %s", (meeting_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            raise ValueError("Transkript bulunamadı")
        return row[0]
    
    
    def save_summary(self, meeting_id: str, summary: str):
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO summaries (meeting_id, content) VALUES (%s, %s)",
            (meeting_id, summary)
        )
        conn.commit()
        cur.close()
        conn.close()

    async def summarize_text(self, text: str) -> str:
        prompt = f"Bu metni özetle:\n\n{text}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

        if response.status_code == 200:
            data = response.json()
            return data.get("response", "").strip()
        else:
            raise HTTPException(status_code=response.status_code, detail="Özetleme hatası")


summarizer = Summarizer()

@router.post("/summarize")
async def summarize(request: Request):
    try:
        body = await request.json()
        meeting_id = body.get("meeting_id")
        if not meeting_id:
            raise HTTPException(status_code=400, detail="meeting_id eksik")

        transcript = summarizer.fetch_transcript(meeting_id)
        summary = await summarizer.summarize_text(transcript)
        summarizer.save_summary(meeting_id, summary)

        return JSONResponse(content={"summary": summary})

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
