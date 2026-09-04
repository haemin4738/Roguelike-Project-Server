import smtplib
from email.mime.text import MIMEText
from app import config


def send_verification_email(to_email: str, token: str) -> None:
    url = f"https://roguelike-project-server-production.up.railway.app/auth/verify/{token}"
    body = (
        f"안녕하세요!\n\n"
        f"아래 링크를 클릭해 이메일 인증을 완료해주세요:\n\n"
        f"{url}\n\n"
        f"링크는 24시간 후 만료됩니다."
    )
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "[Roguelike] 이메일 인증"
    msg["From"] = config.GMAIL_USER
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(config.GMAIL_USER, config.GMAIL_PASSWORD)
        smtp.send_message(msg)
