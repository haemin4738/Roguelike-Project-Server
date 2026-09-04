import json
import urllib.request
from app import config


def send_verification_email(to_email: str, token: str) -> None:
    url = f"https://roguelike-project-server-production.up.railway.app/auth/verify/{token}"
    body = (
        f"안녕하세요!\n\n"
        f"아래 링크를 클릭해 이메일 인증을 완료해주세요:\n\n"
        f"{url}\n\n"
        f"링크는 24시간 후 만료됩니다."
    )
    data = json.dumps({
        "from": "Roguelike <onboarding@resend.dev>",
        "to": [to_email],
        "subject": "[Roguelike] 이메일 인증",
        "text": body,
    }).encode()

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=data,
        headers={
            "Authorization": f"Bearer {config.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    urllib.request.urlopen(req)
