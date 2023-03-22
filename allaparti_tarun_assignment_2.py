from flask import Flask, request
app = Flask(__name__)
@app.route("/")

@app.route("/execute", methods=["POST"])
def shrug():
    input = request.get_json()
    data = input.get("data")
    command = data.get("command")
    if command == "shrug":
        message = data.get("message")
        message = message + r"¯\_(ツ)_/¯"
        response = {"data": {"command": command, "message": message}}
        response_code = 200
    else:
        response = ''
        response_code = 400
    return response, response_code 


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5051)
