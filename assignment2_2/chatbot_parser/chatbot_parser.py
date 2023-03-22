from flask import Flask, jsonify, request
import requests
import json
import argparse
from urllib.parse import urljoin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/chatbot_db"
db = SQLAlchemy(app)

class commands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(20))
    server_url = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'command': self.command,
            'server_url': self.server_url
        }

@app.route("/")

@app.route("/message", methods=["POST"])
def message():
    input = request.get_json()
    if input == None:
        response = {"data":{"command":None,"message":"No input given"}} 
        response_code = 400 
    else:
        data = input["data"]["message"]
        words = data.split()
        command = words[0]
        if command[0] == '/':
            message = " ".join(words[1:])
            command = command[1:]
            if len(command) == 0 or len(message) == 0 or command is None or message is None:
                response = {"data":{"command":command,"message":"Invalid Input"}} 
                response_code = 200
                return response, response_code
        else: 
            message = " ".join(words[0:])
            command = None
        response = {"data":{"command":command,"message":message}} 
        response_code = 200
        c = commands.query.filter_by(command=command).first()
        if c:
        # with open('serverMapping.json') as f:
        #     val = json.load(f)
        # if val.get(command):
        #     url = val.get(command)
            url = c.server_url
            full_url = urljoin(url, "/execute")
            # return {"data":{"command":command,"message":full_url}}, response_code
            r= requests.post(full_url, json={"data": {"command": command, "message": message }})
            r.raise_for_status()
            output = r.json()
            return {"data":{"command":command,"message":output["data"]["message"]}}, response_code
        else:
            return response, response_code 

@app.route("/register", methods=["POST"])
def register():
    input = request.get_json()
    url = input["data"]["server_url"]
    url = url.strip(" ")
    command = input["data"]["command"]
    if command is None or command == "" or url is None or url == "":
            return {"data":{"command":None,"message":"Invalid input"}}, 400
    response = {"data": {"command": command, "message": "saved"}}
    response_code = 200
    c = commands.query.filter_by(command=command).first()
    if c:
        return jsonify({'error': 'Command already exists'}), 400
    else: 
        new = commands(command=command, server_url = url)
        db.session.add(new)
        try:
            db.session.commit() 
            return response, response_code
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': 'Command already exists'})
    # with open('serverMapping.json') as f:
 
    #     val = json.load(f)
    # val.update({command:url})  
    # with open('serverMapping.json', '+w') as f:
    #     json.dump(val, f)
    # return response, response_code
   

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)