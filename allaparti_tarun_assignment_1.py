from flask import Flask, request
import requests
import json
import argparse
from urllib.parse import urljoin
app = Flask(__name__)
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
        with open('serverMapping.json') as f:
            val = json.load(f)
        if val.get(command):
            url = val.get(command)
            full_url = urljoin(url, "/execute")
            r= requests.post(full_url, json={"data": {"command": "shrug", "message": message }})
            r.raise_for_status()
            output = r.json()
            return {"data":{"command":command,"message":output["data"]["message"]}}, response_code
        else:
            return response, response_code 

@app.route("/register", methods=["POST"])
def register():
    input = request.get_json()
    url = input["data"]["server_url"]
    command = input["data"]["command"]
    response = {"data": {"command": command, "message": "saved"}}
    response_code = 200
    with open('serverMapping.json') as f:
 
        val = json.load(f)
    val.update({command:url})  
    with open('ServerMapping.json', 'w') as f:
        json.dump(val, f)
    return response, response_code
   

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)