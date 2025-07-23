from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Local MongoDB configuration
MONGO_HOST = "localhost"
MONGO_PORT = 27017  # Default MongoDB port
DATABASE_NAME = "portfolio_db"
COLLECTION_NAME = "contacts"

# Connect to local MongoDB
try:
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client[DATABASE_NAME]
    contacts_collection = db[COLLECTION_NAME]
    print("Successfully connected to local MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        
        contacts_collection.insert_one({
            'name': data['name'],
            'email': data['email'],
            'subject': data['subject'],
            'message': data['message'],
            'timestamp': datetime.datetime.utcnow()
        })
        
        return jsonify({'success': True, 'message': 'Form submitted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
