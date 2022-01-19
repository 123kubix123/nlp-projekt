import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
import pickle

from sklearn.preprocessing import StandardScaler

df = pd.read_csv('dataset.csv')
y_columns = ['rating', 'rating_count']
text_columns = ['title', 'desc_text']

text_df = df[[*text_columns, 'photos_count']]
df = df.drop(columns=text_columns)

df = df.astype(float)
y_rating = df['rating']
y_cnt = df['rating_count']
X = df.drop(columns=y_columns)

X = X.to_numpy()
y_rating = y_rating.to_numpy()
y_cnt = y_cnt.to_numpy()

X_train, X_test, y_train_rating, y_test_rating, y_train_cnt, y_test_cnt, _, text_test = train_test_split(
    X, y_rating, y_cnt, text_df, test_size=0.2, random_state=42)

text_test.to_excel('test_text.xlsx', index=0)

# scaling
data_scaler = StandardScaler()
data_scaler.fit(X_train)
X_train = data_scaler.transform(X_train)
X_test = data_scaler.transform(X_test)

y_train_rating = np.expand_dims(y_train_rating, axis=-1)
y_test_rating = np.expand_dims(y_test_rating, axis=-1)
y_train_cnt = np.expand_dims(y_train_cnt, axis=-1)
y_test_cnt = np.expand_dims(y_test_cnt, axis=-1)

output_scalers = {'rating': StandardScaler(), 'rating_count': StandardScaler()}
output_scalers['rating'].fit(y_train_rating)
output_scalers['rating_count'].fit(y_train_cnt)

y_train_rating = output_scalers['rating'].transform(y_train_rating)
y_test_rating = output_scalers['rating'].transform(y_test_rating)

y_train_cnt = output_scalers['rating_count'].transform(y_train_cnt)
y_test_cnt = output_scalers['rating_count'].transform(y_test_cnt)

y_train_rating = np.squeeze(y_train_rating)
y_test_rating = np.squeeze(y_test_rating)
y_train_cnt = np.squeeze(y_train_cnt)
y_test_cnt = np.squeeze(y_test_cnt)

ys = {'rating_train': y_train_rating, 'rating_test': y_test_rating,
      'rating_count_train': y_train_cnt, 'rating_count_test': y_test_cnt}

models = [SVR, KNeighborsRegressor, AdaBoostRegressor, RandomForestRegressor]
best_models = {col: {'model': None, 'scaler': output_scalers[col], 'mae': 1e+100} for col in y_columns}

for model in models:
    print('='*50)
    print('Model:', model)
    for col in y_columns:
        current_model = model()
        current_model.fit(X_train, ys[col + '_train'])
        
        preds = current_model.predict(X_test)
        print(col)
        mae = np.mean(np.abs(ys[col + '_test'] - preds))
        
        
        print('MAE:', mae * output_scalers[col].scale_)
        print('MSE:', np.mean((ys[col + '_test'] - preds) ** 2) * output_scalers[col].scale_)
        
        if mae < best_models[col]['mae']:
            best_models[col]['mae'] = mae
            best_models[col]['model'] = current_model
    
for col in best_models.keys():
    with open(f'nlp-projekt-backend/model_{col}.pkl', 'wb') as f:
        pickle.dump(best_models[col]['model'], f)
    with open(f'nlp-projekt-backend/output_scaler_{col}.pkl', 'wb') as f:
        pickle.dump(best_models[col]['scaler'], f)

with open(f'nlp-projekt-backend/data_scaler.pkl', 'wb') as f:
        pickle.dump(data_scaler, f)