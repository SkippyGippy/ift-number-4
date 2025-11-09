from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'CHANGE TO YOUR MONGO DB STRING' # REPLACE WITH YOUR LINK ADD "/stars" before "?" and after ".net"
mongo = PyMongo(app)
@app.route('/icecream', methods=['GET'])
def get_all_icecreams():
    icecreams_collection = mongo.db.icecreams
    output = []
    for s in icecreams_collection.find():
        output.append({'name': s['name'], 'flavor': s['flavor']})
    return jsonify({'result': output})
@app.route('/icecream', methods=['POST'])
def add_icecream():
    icecreams_collection = mongo.db.icecreams
    name = request.json['name']
    flavor = request.json['flavor']
    
    # Use insert_one instead of deprecated insert
    result = icecreams_collection.insert_one({'name': name, 'flavor': flavor})
    new_icecream = icecreams_collection.find_one({'_id': result.inserted_id})
    
    output = {'name': new_icecream['name'], 'flavor': new_icecream['flavor']}
    return jsonify({'result': output})
if __name__ == "__main__":
    app.run(debug=True)