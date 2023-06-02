from flask import Flask, request, jsonify
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hala lalay lalay la la lay laaaay'

users = {}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username not in users or users[username]['password'] != password:
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token}), 200

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users:
        return jsonify({'message': 'Username already exists!'}), 400

    users[username] = {"password": password, "profile": {}}

    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/profile', methods=['GET', 'PUT'])
@token_required
def profile(current_user):
    if request.method == 'GET':
        profile = users[current_user]['profile']
        return jsonify(profile), 200
    elif request.method == 'PUT':
        profile = users[current_user]['profile']
        data = request.json

        if 'name' in data:
            profile['name'] = data['name']
        if 'email' in data:
            profile['email'] = data['email']
        if 'address' in data:
            profile['address'] = data['address']

        users[current_user]['profile'] = profile

        return jsonify({'message': 'User profile updated successfully!'}), 200

@app.route('/validate-login', methods=['POST'])
@token_required
def validate_login(current_user):
    return jsonify({'valid': True, 'username': current_user}), 200

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': 'Protected resource accessed by {}'.format(current_user)}), 200

if __name__ == '__main__':
    app.run()
