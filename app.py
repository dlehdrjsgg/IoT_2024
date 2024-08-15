from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  

def getItem():
    with open('items.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    #remove sample
    data['items'] = data['items'][1:]
    return data

def removeItem(barcode,timestamp):
    with open('items.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get('items'):
        if item.get('barcode') == barcode and item.get('timestamp') == timestamp:
            data.get('items').remove(item)
    with open('items.json', 'w', encoding="utf-8") as f:
        json.dump(data, f,ensure_ascii = False ,indent = 4)
    return data

@app.route('/api/get-item-details', methods=['POST'])
def get_item_details():
    data = request.get_json()
    items = getItem().get('items')
    #remove sample
    return jsonify({"items": items})

@app.route('/api/remove-item', methods=['POST'])
def remove_item():
    data = request.get_json()
    barcode = data.get('barcode')
    timestamp = data.get('timestamp')
    items = removeItem(barcode,timestamp).get('items')
    return jsonify({"items": items})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)