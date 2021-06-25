import numpy as np
from flask import Flask, request, jsonify, render_template
import pandas as pd       
import pickle

app = Flask(__name__)
model = pickle.load(open('apriori_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():

	recommendation = request.form['message']
	data = [recommendation]		
	prediction = model[~model['In Cart'].str.contains(data, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)
	return render_template('home.html',pred='Recommendation of Next product in cart page is :'.format(prediction))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
	  data_unseen = pd.DataFrame([data])		
	  output = model[~model['In Cart'].str.contains(data_unseen, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
