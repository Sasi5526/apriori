from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# load the model from disk
filename = 'apriori_model.pkl'
model = pickle.load(open(filename, 'rb'))
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():


	if request.method == 'POST':
		apriori = request.form['In Cart']
		data = [apriori]
		my_prediction = model[~model['In Cart'].str.contains(data, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)
	return render_template('result.html',prediction = my_prediction)



if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080)
