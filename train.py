import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor

df = pd.read_csv('dataset.csv').astype(float)

# normalization
m = df.mean()
std = df.std()
df = (df - m) / std

y_rating = df['rating']
y_cnt = df['rating_count']
y_columns = ['rating', 'rating_count']
X = df.drop(columns=y_columns)

X = X.to_numpy()
y_rating = y_rating.to_numpy()
y_cnt = y_cnt.to_numpy()

X_train, X_test, y_train_rating, y_test_rating, y_train_cnt, y_test_cnt = train_test_split(
    X, y_rating, y_cnt, test_size=0.2, random_state=42)

ys = {'rating_train': y_train_rating, 'rating_test': y_test_rating,
      'rating_count_train': y_train_cnt, 'rating_count_test': y_test_cnt}

models = [SVR, KNeighborsRegressor, AdaBoostRegressor, RandomForestRegressor]
for model in models:
    print('='*50)
    print('Model:', model)
    for col in y_columns:
        m = model()
        m.fit(X_train, ys[col + '_train'])
        
        preds = m.predict(X_test)
        print(col)
        print('MAE:', np.mean(np.abs(ys[col + '_test'] - preds)) * std[col])
        print('MSE:', np.mean((ys[col + '_test'] - preds) ** 2) * std[col])
    
preds = preds * std['rating'] + m['rating']
y_test_cnt = y_test_cnt * std['rating'] + m['rating']
