from flask import Flask, jsonify, request

app = Flask(__name__)

products = {
    1: {
        'id': 1,
        'name': 'Product 1',
        'price': 10.99
    },
    2: {
        'id': 2,
        'name': 'Product 2',
        'price': 19.99
    },
    3: {
        'id': 3,
        'name': 'Product 3',
        'price': 7.99
    }
}

@app.route('/products', methods=['GET'])
def get_all_products():
    return jsonify(products), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    if id in products:
        return jsonify(products[id]), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/products/<int:id>/reviews', methods=['POST'])
def add_product_review(id):
    if id in products:
        review = request.json.get('review')
        if review:
            products[id].setdefault('reviews', []).append(review)
            return jsonify({'message': 'Review added successfully'}), 201
        else:
            return jsonify({'message': 'Review data is missing'}), 400
    else:
        return jsonify({'message': 'Product not found'}), 404
    
@app.route('/products/validate/<int:product_id>', methods=['GET'])
def validate_product(product_id):
    return jsonify({'valid': product_id in products})

if __name__ == '__main__':
    app.run()