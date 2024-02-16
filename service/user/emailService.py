import smtplib, os
from database import session
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def verifyEmail(email: str) -> str:
    if email is not None:
        session.flush()
    return f"Email verified."


async def send_verification_email(receiver: str, name: str, link: str):

    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT")
    smtp_username = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")

    message = MIMEMultipart()
    message['From'] = os.environ.get("SMTP_USER")
    message['To'] = receiver
    message["Subject"] = "Verify Your Email"

    html_content = f"""
        <html>
        <body>
            <p>Dear {name},</p>
            <p>Please click the following link to verify your email:</p>
            <a href="{link}">Verify Email</a>
        </body>
        </html>
    """
    message.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(os.environ.get("SMTP_USER"), receiver, message.as_string())