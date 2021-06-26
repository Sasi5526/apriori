import pandas as pd
import os
from os  import getcwd
import pickle
from flask import Flask, render_template, request


app = Flask(__name__)

directory = getcwd()


# # Import the required Pickle files


model = pickle.load(open(os.path.join(directory,'apriori_model.pkl', 'rb')))



# This function structures the HTML code for displaying the table on website
def html_code_table(df,table_name,file_name,side):
    table_style = '<table style="border: 2px solid; float: ' + side + '; width: 40%;">'
    table_head = '<caption style="text-align: center; caption-side: top; font-size: 140%; font-weight: bold; color:black;"><strong>' + table_name + '</strong></caption>'
    table_head_row = '<tr><th>Recommendation</th></tr>'
    
    html_code = table_style + table_head + table_head_row
    
    for i in range(len(df.index)):
        row = '<tr><td>' + str(df['Recommendation'][i]) +'</td></tr>'
        html_code = html_code + row
        
    html_code = html_code + '</table>'
    
    file_path = os.path.join(directory,'templates/')
    
    hs = open(file_path + file_name + '.html', 'w')
    
    
def apriori(prod_name):
    apriori = model.loc[prod_name].sort_values(ascending=False)
    
    input_index = apriori[apriori['In Cart'] == prod_name].index
    apriori.drop(index=input_index,inplace=True)
    
    apriori = model[~model['In Cart'].str.contains(prod_name, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)
    
    
    html_code_table(apriori,'Recommendation of Next product in cart page is :','next_product','center')
    

@app.route("/")
def home():

    return render_template('home.html')


@app.route("/login")
def login():

    prod_name = str(request.args.get('name')).upper()
    
    if prod_name in model['In Cart'].unique():
        return render_template('cust_home.html',name=prod_name,new='n')
    else:
        return render_template('cust_home.html',name=prod_name,new='y')

if __name__ == '__main__':
    app.run(debug=True)
