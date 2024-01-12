from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    msg_array = []
    for message in Message.query.order_by(Message.created_at.asc()).all():
        msg_dict = message.to_dict()
        
        msg_array.append(msg_dict)

    response = make_response(jsonify(msg_array), 200)

    response.headers["Content-Type"]="application/json"

    return response

@app.route('/messages', methods=["POST"])
def create_message():
    body = request.json["body"]
    username = request.json["username"]
    # created_at = request.form["created_at"]

    new_message = Message(body = body, username = username, created_at=datetime.utcnow())

    db.session.add(new_message)
    db.session.commit()

    new_message_dict = new_message.to_dict()

    response = make_response(new_message_dict, 201)

    return response
   

@app.route('/messages/<int:id>', methods = ["PATCH"])
def messages_by_id(id):
    updated_message = Message.query.filter(id==id).first()

    for attr in request.json:
        setattr( updated_message, attr, request.json.get(attr))

    db.session.add(updated_message)
    db.session.commit()

    updated_message_dict = updated_message.to_dict()

    response = make_response(updated_message_dict, 200)

    return response


@app.route('/messages/<int:id>', methods = ["DELETE"])
def delete_messages(id):
    deleted_msg = Message.query.get_or_404(id)

    db.session.delete(deleted_msg)
    db.session.commit()

    response_body = {"msg":"Message deleted successfully"}

    response = make_response(response_body, 200)
    return response



if __name__ == '__main__':
    app.run(port=5555)
