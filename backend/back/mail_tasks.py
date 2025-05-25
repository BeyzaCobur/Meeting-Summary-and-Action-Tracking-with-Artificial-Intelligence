from fastapi import APIRouter, Request
from back.email import send_email

router = APIRouter()

EMAIL_MAP = {
    "Sena": "sena@example.com",
    "Beyza": "beyza@example.com"
}

@router.post("/send_tasks")
async def send_tasks(request: Request):
    body = await request.json()
    tasks = body.get("tasks", [])

    if not tasks:
        return {"error": "Görev listesi boş"}

    email_body = ""
    recipients = set()

    for task in tasks:
        name = task.get("assignee")
        description = task.get("description")

        if name and description:
            email_body += f"{name}: {description}\n"
            if name in EMAIL_MAP:
                recipients.add(EMAIL_MAP[name])

    if not recipients:
        return {"error": "Alıcı bulunamadı"}

    send_email("Toplantı Görevleri", email_body, list(recipients))
    return {"status": "success", "message": "E-postalar gönderildi"}
