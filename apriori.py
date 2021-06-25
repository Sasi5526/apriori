# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 20:12:49 2021

@author: sasim
"""


import pandas as pd 
import pickle
df = pd.read_csv('D:\\sasi\\Metric Bees\\kz_new.csv')


df.info()





df.head(3)

def prepare_data(df):
    current_order_id = df.iloc[0,1]
    carts = []
    products = []
    for row in df.iterrows():
        order_id = row[1]['order_id']
        product_name = row[1]['category_code']
        if  order_id == current_order_id:
            products.append(product_name)
        else:
            carts.append(products)
            products = []
            products.append(product_name)
            current_order_id = order_id
    carts.append(products)
    
    return pd.DataFrame(carts)

carts_df = prepare_data(df)



transactions = []
for i in range(carts_df.shape[0]):
    transactions.append([str(carts_df.values[i,j]) for j in range(12)])
print(f'----Sameple cart ---- \n{transactions[0]}')


from apyori import apriori
rules = apriori(transactions= transactions, 
                min_support = 0.003, #Support shows transactions with items purchased together in a single transaction.
                min_confidence = 0.3, #Confidence shows transactions where the items are purchased one after the other.
                min_lift=3,
                min_length=2,
                max_length=7
               )
 

results = list(rules)
print(f'Number of Rules = {len(results)}')


print('----------- Sample rule --------------')
results[0]


def inspect(results):
    lhs         = [" + ".join(tuple(result[2][0][0])) for result in results]
    rhs         = [" + ".join(tuple(result[2][0][1])) for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))



resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['In Cart', 'Recommendation', 
                                                                'Support', 'Confidence', 'Lift'])
resultsinDataFrame.sort_values(by='Lift', ascending=False)


result = resultsinDataFrame[~resultsinDataFrame['In Cart'].str.contains('electronics.video.tv', regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)

da = str(input("enter"))

resultsinDataFrame[~resultsinDataFrame['In Cart'].str.contains(da, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)


resultsinDataFrame.to_csv('D:\\sasi\\Metric Bees\\apriori\\apriori.csv',index=False)

pickle.dump(resultsinDataFrame, open('apriori_model.pkl','wb'))
































