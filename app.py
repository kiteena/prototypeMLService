from flask import Flask, Response, request, render_template
import requests
import json 
from surprise import Dataset

from src.recommenders import Recommenders
from src.evaluation_utils import getRMSEofPredictions
from src.utils import makeDictionary

data = Dataset.load_builtin('ml-100k')

rec = Recommenders(data, "SVD")
algoSVDPred = rec.getAllUsersPredictions()

app = Flask(__name__, template_folder='src/static')


@app.route("/", methods=['GET'])
def hello(): 
    return render_template('home_screen.html')


@app.route("/predictionspretty/")
def get_pretty_predictions(): 
    data = makeDictionary(algoSVDPred[:10])
    return Response(json.dumps(data, indent=4), status=200, mimetype='application/json')


@app.route("/predictions/", methods=['GET'])
def get_predictions(): 
    return Response(json.dumps(algoSVDPred[:10], indent=4), status=200, mimetype='application/json')


@app.route("/predictions/<userID>/", methods=['GET'])
def get_K_user_predictions(userID):
    if not rec._verifyUserID(userID): 
        return Response(status=400, mimetype='application/json')
    if 'k' in request.args:
        k = request.args.get('k')
        if not k.isdigit(): 
            return Response(status=400, mimetype='application/json')
        k_data = makeDictionary(rec.getKPredictionsforaUser(userID, int(k))) 
    else: 
        k_data = makeDictionary(rec.getKPredictionsforaUser(userID)) 
    return Response(json.dumps(k_data, indent=4), status=200, mimetype='application/json')


@app.route("/predictionuseritem/", methods=['GET'])
def get_user_predictions():
    if 'user' in request.args and 'item' in request.args: 
        user = request.args.get('user')
        if not rec._verifyUserID(user): 
            print('here')
            return Response(status=400, mimetype='application/json')
        item = request.args.get('item')
        if not user.isdigit() or not item.isdigit(): 
            return Response(status=400, mimetype='application/json')
        result = rec._algo().predict(user, item)
    else: 
        return Response(status=400, mimetype='application/json')
    return Response(json.dumps(result, indent=4), status=200, mimetype='application/json')


@app.route("/rmse/", methods=['GET'])
def get_accuracy(): 
    return json.dumps({"rmse" : str(getRMSEofPredictions(algoSVDPred))})
    

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=80)


 
