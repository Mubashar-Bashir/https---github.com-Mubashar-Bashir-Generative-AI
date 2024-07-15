# Gmail_gateway.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import List
from app.notification_settings import SMTP_SERVER,SMTP_PORT,SMTP_USERNAME,SMTP_PASSWORD

async def send_email_gmail(from_email:str , to_emails:List[str], subject:str, message: str):
    try:
        sender_email = SMTP_USERNAME
        receiver_emails = to_emails

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Sender', sender_email))
        msg['To'] = ", ".join(receiver_emails)
        msg['Subject'] = subject

        # Add message body
        msg.attach(MIMEText(message, 'plain'))

        # Connect to Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, SMTP_PASSWORD)  # Use your Gmail password or app-specific password

            # Send email
            server.sendmail(sender_email, receiver_emails, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage:
async def email_gateway_example():
    await send_email_gmail(
        from_email=SMTP_USERNAME,
        to_emails=["mubasharbashir003@gmail.com", "mubashar_bashir03@yahoo.com"],
        subject="Test Email Python Integration E-mail",
        message="This is a test email message."
    )

# Run the example
if __name__ == "__main__":
    import asyncio
    asyncio.run(email_gateway_example())
