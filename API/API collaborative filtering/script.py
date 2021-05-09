# %%
import json
import pandas as pd
import numpy as np
import os
import pickle
import implicit

def init():
    
    global model
    global sparse_user_item
    first_model_name = 'model_col'
    first_model_version = '1'
    first_model_path =  os.path.join(os.getenv('AZUREML_MODEL_DIR'),first_model_name, first_model_version,  'Collaborative_Filtering.joblib')
    print(first_model_path)
    with open(first_model_path, 'rb') as handle:
        model = pickle.load(handle)
 
    # loading
    second_model_name = 'user_item'
    second_model_version = '1'
    second_model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), second_model_name, second_model_version, 'sparse_user_item.joblib')
    print(second_model_path)
    with open(second_model_path, 'rb') as handle:
        sparse_user_item = pickle.load(handle)

def run(data):
    try:    
        print("into Run")   
        user_id = json.loads(data)['userId']
        user_id = int(user_id)
        print('Recommande')
        recommended = model.recommend(user_id, sparse_user_item)
        print('Make list 5')
        k = []
        for i in range(0,5):
            k.append(str(recommended[i][0]))
        return k
        
    except Exception as e:
        error = str(e)
        return error

    