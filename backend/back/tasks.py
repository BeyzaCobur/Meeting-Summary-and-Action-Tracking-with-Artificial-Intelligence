from fastapi import APIRouter, Request, HTTPException
import httpx
import psycopg2

router = APIRouter()

@router.post("/extract_tasks")
async def extract_tasks(request: Request):
    try:
        body = await request.json()
        meeting_id = body.get("meeting_id")
        if not meeting_id:
            raise HTTPException(status_code=400, detail="meeting_id eksik")

        # 1. Transkripti veritabanından al
        conn = psycopg2.connect(
            dbname="toplantidb",
            user="postgres",
            password="230565",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("SELECT content FROM transcripts WHERE meeting_id = %s", (meeting_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Transkript bulunamadı")

        transcript = row[0]

        # 2. Prompt oluştur ve Ollama'ya gönder
        prompt = (
            "Aşağıdaki toplantı transkriptinden görevleri çıkar. Her satır şu formatta olsun:\n"
            "[KİŞİ]: [Görev açıklaması]\n\n"
            "Transkript:\n" + transcript
        )

        async with httpx.AsyncClient() as client:
            ollama_response = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": "mistral", "prompt": prompt},
                timeout=60
            )

        if ollama_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Görev çıkarımı başarısız")

        lines = ollama_response.json()["response"].split("\n")

        tasks = []
        for line in lines:
            if ":" in line:
                name, description = line.split(":", 1)
                name = name.strip()
                description = description.strip()

                # 3. Kullanıcıyı ve katılımcıyı kontrol et / oluştur
                cur.execute("SELECT id FROM users WHERE title = %s", (name,))
                user_row = cur.fetchone()
                if user_row:
                    user_id = user_row[0]
                else:
                    cur.execute("INSERT INTO users (title) VALUES (%s) RETURNING id", (name,))
                    user_id = cur.fetchone()[0]

                cur.execute(
                    "SELECT id FROM participants WHERE user_id = %s AND meeting_id = %s",
                    (user_id, meeting_id)
                )
                part_row = cur.fetchone()
                if part_row:
                    participant_id = part_row[0]
                else:
                    cur.execute(
                        "INSERT INTO participants (user_id, meeting_id, email) VALUES (%s, %s, %s) RETURNING id",
                        (user_id, meeting_id, f"{name.lower()}@example.com")
                    )
                    participant_id = cur.fetchone()[0]

                # 4. Görevi kaydet
                cur.execute(
                    "INSERT INTO tasks (description, status, participant_id, meeting_id) VALUES (%s, %s, %s, %s)",
                    (description, "todo", participant_id, meeting_id)
                )

                tasks.append({
                    "assignee": name,
                    "description": description
                })

        conn.commit()
        cur.close()
        conn.close()

        return {"tasks": tasks}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
