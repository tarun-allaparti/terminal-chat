from flask import Flask, request
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
app = Flask(__name__)
@app.route("/")

@app.route("/execute", methods=["POST"])
def send():
    input = request.get_json()
    data = input["data"]
    c = data["command"]
    if c != "email":
        response = ''
        response_code = 400
        return response, response_code
    m = data["message"]
    words = m.split()
    if len(words)<3:
        return {"data": {"command": "command", "message": "Invalid message" }}, 200
    email = words[0]
    subject1 = words[1]
    message = " ".join(words[2:])
    sg = sendgrid.SendGridAPIClient('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')
    from_email = Email("tarun.allaparti@berkeley.edu")  # Change to your verified sender
    to_email = To(email)  # Change to your recipient
    subject = subject1
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    check = sg.client.mail.send.post(request_body=mail_json)
    response_code = 200
    if check:
        response = {"data": {"command": "command", "message": "Email was sent" }}
    else: 
        response = {"data": {"command": "command", "message": "Invalid input" }}
    return response, response_code

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5052)