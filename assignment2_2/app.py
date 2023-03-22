import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient('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')
from_email = Email("tarun.allaparti@berkeley.edu")  # Change to your verified sender
to_email = To("tarun.allaparti@gmail.com")  # Change to your recipient
subject = "Reminder"
content = Content("text/plain", "research call @ 2, mse party @ 4")
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)
