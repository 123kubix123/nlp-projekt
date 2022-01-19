from flask import Flask, request, send_from_directory, jsonify, Response
import json
import pickle

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import processing
import feature_extraction
import pandas as pd
import numpy as np

app = Flask(__name__)

#load models
with open('model_rating.pkl', 'rb') as f:
    model_rating = pickle.load(f)
    
with open('model_rating_count.pkl', 'rb') as f:
    model_count = pickle.load(f)
    
#load scalers
with open('data_scaler.pkl', 'rb') as f:
    data_scaler = pickle.load(f)
    
with open('output_scaler_rating.pkl', 'rb') as f:
    output_scaler_rating = pickle.load(f)
    
with open('output_scaler_rating_count.pkl', 'rb') as f:
    output_scaler_count = pickle.load(f)
    
columns = pd.read_csv('../dataset.csv').drop(columns=['rating', 'rating_count']).columns
  
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
            product['desc_text'] = product.pop('desc')
            product['photos_count'] = 0
            
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
            features = {col: features[col] for col in features.keys() if col in columns}
            for col in columns:
                if col not in features:
                    features[col] = 0
            features = pd.DataFrame([features]).to_numpy()
            features = data_scaler.transform(features)
            
            rating_pred = model_rating.predict(features)[0]
            count_pred = model_count.predict(features)[0]
            
            rating_pred = rating_pred * output_scaler_rating.scale_ + output_scaler_rating.mean_
            count_pred = count_pred * output_scaler_count.scale_ + output_scaler_count.mean_
                
            rating_pred = np.round(rating_pred.squeeze()[()], decimals=3)
            count_pred = np.round(count_pred.squeeze()[()], decimals=3)
            
            rating_pred = np.clip(rating_pred, 0, 5)
            count_pred = np.clip(count_pred, 0, None)
            # Return JSON object with original title, desc and prediction for rating and rating_count
            result = {'title': title, 'desc': desc, 'rating': rating_pred, 'rating_count': count_pred}
            return jsonify(result)
        else:
            return Response(status=400)
  
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug = True)