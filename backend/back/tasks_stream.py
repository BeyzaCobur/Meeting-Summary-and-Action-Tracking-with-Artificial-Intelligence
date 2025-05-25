from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import httpx
import asyncio
import json
import re

router = APIRouter()

@router.post("/extract_tasks_stream")
async def extract_tasks_stream(request: Request):
    body = await request.json()
    transcript = body.get("text", "")

    prompt = (
    "Aşağıdaki transkripti oku ve her kişiye ait görevleri çıkar. "
    "Her görev için sadece şu formatta bir JSON nesnesi üret:\n"
    '{"assignee": "<İsim>", "description": "<Görev açıklaması>"}\n'
    "Yalnızca görev cümlelerini dikkate al, açıklamaları sade ve Türkçe yaz. "
    "Boş ya da anlamsız görevler yazma.\n\n"
    f"Transkript:\n{transcript}"
)




    async def task_streamer():
        buffer = ""
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": True
                }
            ) as response:
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        json_obj = json.loads(line)
                        partial = json_obj.get("response", "")
                        buffer += partial

                        while "\n" in buffer:
                            full_line, buffer = buffer.split("\n", 1)
                            match = re.match(r"\d*\.*\s*(.+?):\s*(.+)", full_line.strip())
                            if match:
                                assignee, description = match.groups()
                                task = {
                                    "assignee": assignee.strip(),
                                    "description": description.strip()
                                }
                                yield f"data: {json.dumps(task, ensure_ascii=False)}\n\n"

                            await asyncio.sleep(0.05)

                    except json.JSONDecodeError:
                        continue

    return StreamingResponse(task_streamer(), media_type="text/event-stream")
