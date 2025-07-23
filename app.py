from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
from dotenv import load_dotenv
import datetime
import urllib.parse

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection with proper password encoding
username = "konerupoojasree"
password = "Kps@2006"  # In production, never hardcode credentials - use environment variables
cluster_url = "cluster0.duqmiwe.mongodb.net"
database_name = "portfolio_db"  # You can change this to your preferred database name

# Properly encode the password
encoded_password = urllib.parse.quote_plus(password)

# Create the MongoDB URI
mongo_uri = f"mongodb+srv://{username}:{encoded_password}@{cluster_url}/{database_name}?retryWrites=true&w=majority"

# Connect to MongoDB
try:
    client = MongoClient(mongo_uri)
    db = client[database_name]
    contacts_collection = db['contacts']
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        
        # Insert the form data into MongoDB
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