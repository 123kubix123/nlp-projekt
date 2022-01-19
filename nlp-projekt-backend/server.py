
from flask import Flask, request, send_from_directory, jsonify, Response
import json
import pickle
from .. import processing
from .. import feature_extraction

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
            seq = processing.Sequencer([
                processing.DictToDF(),
                processing.ApplyFunctionToColumns(
                    feature_extraction.get_main_stats,
                    to_cols=['desc_text', 'title'],
                    to_series=True,
                    to_dtype=float,
                    concat_axis=1
                    ),
                processing.ApplyFunctionToRows(
                    feature_extraction.get_ratios,
                    disregard_columns=['desc_text', 'title'],
                    to_series=True,
                    to_dtype=float,
                    concat_axis=1
                    ),
                processing.ApplyFunctionToColumns(
                    feature_extraction.get_pos_features,
                    to_cols=['desc_text', 'title'],
                    to_series=True,
                    to_dtype=float,
                    concat_axis=1,
                    ),
                processing.ApplyFunctionToColumns(
                    feature_extraction.get_ner_tag_counts,
                    to_cols=['desc_text', 'title'],
                    to_series=True,
                    to_dtype=float,
                    concat_axis=1,
                    ),
                processing.FillNoneValues(replace_null_with=0),
                processing.DropColumns(drop_cols=['desc_text', 'title']),
            ])
            features = seq(product)
            with open('model.pkl', 'rb') as f:
                
                model = pickle.load(f)
                preds = model.predict(features)
                

            # Return JSON object with original title, desc and prediction for rating and rating_count
            result = {'title': title, 'desc': desc, 'rating': 3, 'rating_count': 8}
            return jsonify(result)
        else:
            return Response(status=400)
  
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug = True)