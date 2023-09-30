from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        message_dict = [message.to_dict() for message in messages]
        response = make_response(
            jsonify(message_dict),
            200,
        )
    elif request.method == 'POST':
        msg_data = request.get_json()  # get json data from json file
        message = Message(
            body = msg_data['body'],
            username = msg_data['username']
        )
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            201,
        )

    return response



@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()
    if request.method == 'PATCH':
        msg_data = request.get_json()
        for attr in msg_data:
            setattr(message, attr, msg_data[attr])

        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            200,
        )
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        message_body = {
                'delete': True,
                'message': 'The message is delete successfuly'
                }
        response = make_response(
            jsonify(message_body),
            200,
        )
    return response

if __name__ == '__main__':
    app.run(port=5555)
