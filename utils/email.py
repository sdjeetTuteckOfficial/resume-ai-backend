# ==================== utils/email.py ====================
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.FROM_EMAIL, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def send_otp_email(email: str, otp: str, purpose: str):
    if purpose == "verification":
        subject = "Verify Your Email"
        body = f'''
        <html>
            <body>
                <h2>Email Verification</h2>
                <p>Your OTP for email verification is: <strong>{otp}</strong></p>
                <p>This OTP will expire in {settings.OTP_EXPIRE_MINUTES} minutes.</p>
            </body>
        </html>
        '''
    else:  # reset_password
        subject = "Reset Your Password"
        body = f'''
        <html>
            <body>
                <h2>Password Reset</h2>
                <p>Your OTP for password reset is: <strong>{otp}</strong></p>
                <p>This OTP will expire in {settings.OTP_EXPIRE_MINUTES} minutes.</p>
            </body>
        </html>
        '''
    
    return send_email(email, subject, body)