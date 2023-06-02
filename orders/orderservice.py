import requests
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

USER_SERVICE_URL = 'http://user-service:5000'
PRODUCT_SERVICE_URL = 'http://products-service:5001'


def validate_login_token(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{USER_SERVICE_URL}/validate-login', headers=headers)
    if response.status_code == 200:
        return True, response.json()['username']
    else:
        return False, None
    
def validate_product(product_id):
    response = requests.get(f'{PRODUCT_SERVICE_URL}/products/validate/{product_id}')
    if response.status_code == 200:
        data = response.json()
        return data['valid']
    else:
        return False

orders = {
    1: {
        'id': 1,
        'product_id': 1,
        'quantity': 2,
        'status': 'pending',
        'username': 'user1'
    },
    2: {
        'id': 2,
        'product_id': 2,
        'quantity': 1,
        'status': 'completed',
        'username': 'user2'
    },
    3: {
        'id': 3,
        'product_id': 3,
        'quantity': 3,
        'status': 'pending',
        'username': 'user1'
    }
}

@app.route('/orders', methods=['GET'])
def get_user_orders():
    token = request.headers.get('Authorization', '').split()[1]
    is_valid_token, username = validate_login_token(token)
    if not is_valid_token:
        return jsonify({'message': 'Invalid login token'}), 401

    user_orders = [order for order in orders.values() if order['username'] == username]

    return jsonify(user_orders), 200

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    token = request.headers.get('Authorization', '').split()[1]
    is_valid_token, username = validate_login_token(token)
    if not is_valid_token:
        return jsonify({'message': 'Invalid login token'}), 401

    if id in orders:
        order = orders[id]
        if order['username'] == username:
            return jsonify(order), 200
        else:
            return jsonify({'message': 'Access denied'}), 403
    else:
        return jsonify({'message': 'Order not found'}), 404

@app.route('/orders/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    token = request.headers.get('Authorization', '').split()[1]
    is_valid_token, username = validate_login_token(token)
    if not is_valid_token:
        return jsonify({'message': 'Invalid login token'}), 401

    if id in orders:
        order = orders[id]
        if order['username'] == username:
            order['status'] = 'cancelled'
            return jsonify({'message': 'Order cancelled successfully'}), 200
        else:
            return jsonify({'message': 'Access denied'}), 403
    else:
        return jsonify({'message': 'Order not found'}), 404
    
@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    token = request.headers.get('Authorization', '').split()[1]
    product_id = data.get('product_id')

    if not token or not product_id:
        abort(400, 'User token and product ID are required')

    token_valid, username = validate_login_token(token)
    if not token_valid:
        abort(401, 'Invalid user token')

    if not validate_product(product_id):
        abort(400, 'Invalid product')

    order_id = len(orders) + 1
    orders[order_id] = {'id': order_id, 'product_id': product_id, 'quantity': 1, 'status': 'pending', 'username': username}

    return jsonify({'order_id': order_id}), 201

if __name__ == '__main__':
    app.run()
