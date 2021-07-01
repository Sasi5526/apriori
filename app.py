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

def get_recommendations(title):
    
    data = (title)
    
    return_df = model[~model['product_name'].str.contains(data, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']]

    return return_df

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['post'])
def predict():


    if request.method == 'post':
        m_name = request.form['product_name']
#        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        result_final = get_recommendations(m_name)
        names = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])
        return render_template('result.html',prediction=result_final)


if __name__ == '__main__':
    app.run()
