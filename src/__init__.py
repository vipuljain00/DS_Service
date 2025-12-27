from flask import Flask
from flask import request, jsonify
from app.service.messageService import MessageService   

app = Flask(__name__)

messageService = MessageService()

@app.route('/v1/ds/message/', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)
    if result is None:
        return jsonify({"error": "Not a valid bank message"}), 400
    return jsonify(result.model_dump())

@app.route('/', methods=['GET'])
def handle_get():
    return "Hello World"

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
