import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Creates 'fancy' email using HTML
def create_email(sender_email, receiver_email, code):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verification"
    message["From"] = sender_email
    message["To"] = receiver_email

    # email contents.
    text = f"""\
    Helloo! 
    You're almost in! Below is your unique code that you'll need to DM me on Discord!
    Your code: 
    {code}"""
    html = f"""\
    <html>
      <body>
        <p style="font-size:18px; color:#008fb3">Hello!<br><br>
           You're almost in! Below is your unique code that you'll need to DM me on Discord!<br><br>
           <b>Your code:</b><br><br></p>
           <p style"font-size:26px>{code}</p>
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    return message.as_string()
