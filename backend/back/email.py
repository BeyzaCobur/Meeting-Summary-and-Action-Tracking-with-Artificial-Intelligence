import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(subject: str, body: str, recipients: list[str]) -> None:
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipients, message.as_string())
            print("📬 E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"❌ E-posta gönderimi başarısız oldu: {e}")
