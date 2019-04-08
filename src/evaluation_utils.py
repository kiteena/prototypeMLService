from surprise import accuracy

def getRMSEofPredictions(predictions): 
    return accuracy.rmse(predictions)