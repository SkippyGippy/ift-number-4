from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'CHANGE TO YOUR MONGO DB STRING' # REPLACE WITH YOUR LINK ADD "/stars" before "?" and after ".net"
mongo = PyMongo(app)

@app.route('/star', methods=['GET'])
def get_all_stars():
    stars_collection = mongo.db.stars
    output = []
    for s in stars_collection.find():
        output.append({'name': s['name'], 'distance': s['distance']})
    return jsonify({'result': output})

@app.route('/star', methods=['POST'])
def add_star():
    stars_collection = mongo.db.stars
    name = request.json['name']
    distance = request.json['distance']
    
    # Use insert_one instead of deprecated insert
    result = stars_collection.insert_one({'name': name, 'distance': distance})
    new_star = stars_collection.find_one({'_id': result.inserted_id})
    
    output = {'name': new_star['name'], 'distance': new_star['distance']}
    return jsonify({'result': output})

if __name__ == "__main__":
    app.run(debug=True)