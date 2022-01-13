
from flask import Flask, request, send_from_directory, jsonify, Response
import json

app = Flask(__name__)
  
@app.route('/')
def index():
   return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def home(path):
   return send_from_directory('frontend', path)
  
@app.route('/api/prediction',methods = ['POST'])
def prediction():
    if request.method == 'POST':
        product = request.get_json()
        title = product['title']
        desc = product['desc']
        if(title and desc):
            # Use model to get prediction here

            # Return JSON object with original title, desc and prediction for rating and rating_count
            result = {'title': title, 'desc': desc, 'rating': 3, 'rating_count': 8}
            return jsonify(result)
        else:
            return Response(status=400)
  
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug = True)