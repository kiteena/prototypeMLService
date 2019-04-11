from collections import defaultdict
from surprise import SVD, KNNBasic
from surprise import Dataset
# from surprise.model_selection import train_test_split

# import sys  
# sys.path.insert(0, '/home/kristina/Documents/prototypeMLService')

from src.algorithms import labels, algorithms


class Recommenders: 
    def __init__(self, dataset, algorithm): 
        # self.trainSet, self.testSet =  train_test_split(dataset, test_size=.25)
        raw_ratings = dataset.raw_ratings
        threshold = int(.9 * len(raw_ratings))
        self.trainSet = dataset.build_full_trainset()
        self.testSet = dataset.construct_testset(raw_ratings[threshold:])
        self.algo = algorithms[labels.index(algorithm)]
        self.unorderedPredictions = None
        self.orderedPredictions = defaultdict(list)

    def _algo(self):
        return self.algo

    def _verifyUserID(self, userID):
        if not self.orderedPredictions: 
            self.createOrderedDictionary() 
        return userID in self.orderedPredictions.keys()

    def getAllUsersPredictions(self):
        self.algo.train(self.trainSet)        
        self.unorderedPredictions = self.algo.test(self.testSet)
        return self.unorderedPredictions


    def createOrderedDictionary(self): 
        if not self.unorderedPredictions: 
            self.getAllUsersPredictions()
        for uid, iid, true_r, est, _ in self.unorderedPredictions:
            self.orderedPredictions[uid].append((uid, iid, true_r, est))
        for uid, user_ratings in self.orderedPredictions.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            self.orderedPredictions[uid] = user_ratings 
        return self.orderedPredictions


    def getKPredictionsforaUser(self, userID, K=10):
        if not self.orderedPredictions: 
            self.createOrderedDictionary() 
        return self.orderedPredictions[userID][:K]
        

         



    
    

    

    
