from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz
import random   
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/show_users')
@login_required
def show_users():
    items_list = User.query.all()
    result = "\n".join([f"User ID: {item.id}, Name: {item.username}" for item in items_list])
    return Response(result, content_type='text/plain;charset=utf-8')

@app.route('/delete_user/<string:user_name>')
@login_required
def delete_user(user_name):
    user = user_name
    item = User.query.filter_by(username=user).first()
    db.session.delete(item)
    db.session.commit()
    return f"{user} has been deleted"

@app.route('/add_user/<string:username>/<string:password>')
@login_required
def add_user(username, password):

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return "new user was added"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('show_messages'))

    return render_template('login.html')

@app.route('/login_curl', methods=['POST'])
def login_curl():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            expires= timedelta(days=7)
            access_token = create_access_token(identity=user.id, expires_delta=expires)
            return jsonify(access_token=access_token)

    return jsonify({'error': 'Invalid credentials'}), 401  # Unauthorized

@app.route('/show_messages')
@login_required
def show_messages():
    items_list = Item.query.all()
    result = "\n".join([f"id: {item.id} | Time: {item.time}, Name: {item.name}, Message: {item.message}" for item in items_list])
    return Response(result, content_type='text/plain;charset=utf-8')

@app.route('/curl_messages')
@jwt_required()
def curl_messages():
    items_list = Item.query.all()
    result = "\n".join([f"{item.id} | {item.time} | {item.name} | {item.message}" for item in items_list])
    return Response(result, content_type='text/plain;charset=utf-8')

@app.route('/clear_message_id/<int:item_id>')
@jwt_required()
def clear_message_id(item_id):
    item_to_delete = Item.query.get(item_id)

    if item_to_delete:
        db.session.delete(item_to_delete)
        db.session.commit()
        return f"Item with ID {item_id} has been deleted"
    else:
        return f"No item found with ID {item_id}"

@app.route('/clear_message_name/<string:item_name>')
@jwt_required()
def clear_message_name(item_name):
    item_to_delete = Item.query.filter_by(name=item_name).all()

    for item in item_to_delete:
        db.session.delete(item)
    db.session.commit()

    return f"Items with the name {item_name} have been deleted"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "You are now logged out."

@app.route('/create_tables')
def create_tables():
    with app.app_context():
        db.create_all()
    return "Tables have been created"

@app.route('/delete_item_table')
@jwt_required()
def delete_item_table():
    with app.app_context():
        Item.__table__.drop(db.engine)

    return "Item table has been deleted"

@app.route('/', methods=['GET', 'POST'])
def slash():
    return render_template('index.html')

@app.route('/messenger', methods=['GET', 'POST'])
def messenger():
    return render_template('messenger.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    name = request.args.get('name')
    message = request.args.get('message')
   
    time = datetime.now(pytz.timezone('EST'))
    time = time.strftime("%Y-%m-%d %H:%M:%S")

    new_item = Item(time=time, name=name, message=message)
    db.session.add(new_item)
    db.session.commit()
    return jsonify(success=True), 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
