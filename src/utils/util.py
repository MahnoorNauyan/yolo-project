import smtplib
from email.mime.text import MIMEText


def send_email(email, token):
    
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "cognimindai@gmail.com"
    smtp_password = ""

    
    sender_email = "cognimindai@gmail.com"
    recipient_email = email
    subject = "Password Reset Request"
    body = f'''
        To reset your password, click the following link:
        [Reset Link](http://localhost:8501/?page=reset&token={token})

        If you did not make this request, please ignore this email.
    '''

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = recipient_email

            server.sendmail(sender_email, recipient_email, msg.as_string())

        return True
    except Exception as e:
        print(e)
        return False