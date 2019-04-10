import pandas as pd
import numpy as np
import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import NMF


columns = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
train_df = pd.read_csv('/home/kristina/.surprise_data/ml-100k/ml-100k/u.data', sep='\t', names=columns,encoding='latin-1')
test_df = pd.read_csv('/home/kristina/.surprise_data/ml-100k/ml-100k/u.data', sep='\t', names=columns,encoding='latin-1')

df = pd.pivot_table(train_df, index='user_id', columns='movie_id', aggfunc=np.max).fillna(0)

# implements nearest neighbor (instead of rating) using KNN
start = time.time()
model_knn = NearestNeighbors(metric = 'cosine')
model_knn.fit(df)
for index, _ in df[:-1].iterrows():
    distances, indices = model_knn.kneighbors(df.iloc[index, :].values.reshape(1, -1), n_neighbors = 5)
end = time.time() - start
print(f'NearestNeighbor -- time: {end}')

# implements nearest neighbor using SVD
start = time.time()
SVD = TruncatedSVD(n_components=12, random_state=42)
matrix = SVD.fit_transform(df)
corr = np.corrcoef(matrix)
for index, _ in df[:-1].iterrows():
    res = corr[index].argsort()[-20:][::-1]
recons_matrix = SVD.inverse_transform(matrix)
err = mean_squared_error(df, recons_matrix)
end = time.time() - start
print(f'SVD -- err: {err}, time: {end}')

# non-negative matrix factorization; just looking at time and error 
start = time.time()
nmf = NMF(n_components=12, init='random', random_state=42)
matrix = nmf.fit_transform(df)
recons_matrix = nmf.inverse_transform(matrix)
err = mean_squared_error(df, recons_matrix)
end = time.time() - start
print(f'NMF -- err: {err}, time: {end}')








