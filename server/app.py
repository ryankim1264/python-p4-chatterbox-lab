from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


db.init_app(app)
migrate = Migrate(app, db)
CORS(app)


@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    try:
        new_msg = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_msg)
        db.session.commit()
        return jsonify(new_msg.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = db.session.get(Message, id)
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    data = request.get_json()
    msg.body = data.get('body', msg.body)
    db.session.commit()
    return jsonify(msg.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = db.session.get(Message, id)
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    db.session.delete(msg)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)