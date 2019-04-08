from surprise import SVD, KNNBasic, KNNWithMeans, KNNBaseline, NMF, SlopeOne, CoClustering, BaselineOnly, NormalPredictor
'''
    "SVD" -- https://en.wikipedia.org/wiki/Singular_value_decomposition
    "KNN" -- https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
    "Centered KNN" -- KNN with mean user ratings considered 
    "KNN with Baseline" -- KNN with baseline considered 
    "NMF" -- https://en.wikipedia.org/wiki/Non-negative_matrix_factorization
    "SlopeOne" -- https://en.wikipedia.org/wiki/Slope_One
    "CoClustering" -- https://en.wikipedia.org/wiki/Biclustering
    "BaselineOnly" -- baseline predicted for specific user/item
    "NormalPredictor" -- predict random rating from normal distribution 

    https://surprise.readthedocs.io/en/stable/basic_algorithms.html#surprise.prediction_algorithms.baseline_only.BaselineOnly

'''
labels = [
    "SVD", 
    "KNN", 
    "Centered KNN", 
    "KNN with Baseline", 
    "NMF", 
    "SlopeOne", 
    "CoClustering", 
    "BaselineOnly", 
    "NormalPredictor"
    ]

algorithms = [ 
    SVD(), 
    KNNBasic(), 
    KNNWithMeans(), 
    KNNBaseline(), 
    NMF(), 
    SlopeOne(), 
    CoClustering(), 
    BaselineOnly(),
    NormalPredictor()
    ] 