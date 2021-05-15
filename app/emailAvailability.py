import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_availability_email ( receiver_email, search_term, new_text ): 
  current_date = str(datetime.now()).split(" ")[0]
  short_date = current_date.split("-")[1] + "/" + current_date.split("-")[2]
  sender_email = "kextra12345@gmail.com"
  password = os.environ.get('password')
  
  message = MIMEMultipart("alternative")
  message["Subject"] = f"[{short_date}] COVID Appointment Openings" 
  message["From"] = "COVID-19 Vaccine Updates from Andrea and Katie"
  message["To"] = receiver_email

  # Create the plain-text and HTML version of your message
  text = f"""\
  Covid Vaccine Availabilities for {search_term}: 
  Sent on: {current_date}

  {new_text}"""

  html = f"""\
  <html>
    <body>
      <h3>Covid Vaccine Availabilities for {search_term}</h3>
        <p>Sent on: {current_date}<br>
        {new_text}
      </p>
    </body>
  </html>
  """

  # Turn these into plain/html MIMEText objects
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(part1)
  message.attach(part2)

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, receiver_email, message.as_string()
      )