
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from scraper import get_prices

def build_email(products):
    text_lines = ["Atualização de preços:\n"]
    html_lines = ["<h2>Atualização de preços</h2><ul>"]

    for p in products:
        name = p["name"]
        url = p["url"]
        results = get_prices(url)

        text_lines.append(f"== {name} ==")
        html_lines.append(f"<li><strong>{name}</strong><ul>")

        if not results:
            text_lines.append("Sem resultados\n")
            html_lines.append("<li>Sem resultados</li>")
        else:
            for r in results:
                line = f"- {r['produto']} :: {r['preco']}"
                text_lines.append(line)
                html_lines.append(f"<li>{r['produto']} — {r['preco']}</li>")

        html_lines.append("</ul></li>")
        text_lines.append("")

    text_body = "\n".join(text_lines)
    html_body = "<html><body>" + "".join(html_lines) + "</ul></body></html>"
    return text_body, html_body

def send_email(subject, text_body, html_body, sender, recipient, password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())

def main():
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_USER_RECEIVER = os.getenv("EMAIL_USER_RECEIVER")
    if not EMAIL_USER or not EMAIL_PASS:
        raise RuntimeError("Faltam as variáveis EMAIL_USER e/ou EMAIL_PASS.")

    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    text_body, html_body = build_email(products)

    send_email(
        subject="Atualização de preços",
        text_body=text_body,
        html_body=html_body,
        sender=EMAIL_USER,
        recipient=EMAIL_USER_RECEIVER,
        password=EMAIL_PASS
    )
    print("Email enviado com sucesso.")

if __name__ == "__main__":
    main()