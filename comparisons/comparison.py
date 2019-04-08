from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
import time 

import sys  
sys.path.insert(0, '/home/kristina/Documents/prototypeMLService')

from src.algorithms import labels, algorithms

data = Dataset.load_builtin('ml-100k')
trainset, testset = train_test_split(data, test_size=.25)

print('Movie100K Dataset')

for l, rec in zip(labels, algorithms): 
    start = time.time()
    predictions = rec.fit(trainset).test(testset)
    rec_rmse = accuracy.rmse(predictions, verbose = False)
    end = time.time() - start 
    print(f'{l} -- RMSE:{rec_rmse:2f} time: {end:2f}')
    
    
