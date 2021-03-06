from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
import apyori

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

@app.route('/predict', methods=['POST'])
def predict():
	if request.method == 'POST':
		m_name = request.form['product_name']
		m_name = m_name.title()
       	        result_final = get_recommendations(m_name)
                names = []
                for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
        return render_template('result.html',prediction=names)


if __name__ == '__main__':
    app.run()
