# %%
import json
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity

def init():

    global matrice_emb_art
    global interact_small
    first_model_name = 'model_contbase'
    first_model_version = '1'
    first_model_path =  os.path.join(os.getenv('AZUREML_MODEL_DIR'), first_model_name, first_model_version, 'articles_embeddings.pickle')
    print(first_model_path)
    with open(first_model_path, 'rb') as handle:
        matrice_emb_art = pickle.load(handle)
    print('matrice_emb_art.shape', matrice_emb_art.shape)
 
    # loading
    second_model_name = 'clicks'
    second_model_version = '1'
    second_model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'),second_model_name, second_model_version, 'clicks_small.csv')
    print(second_model_path)
    interact_small = pd.read_csv(second_model_path)

def run(data):
    try: 
        print("into Run")   
        user_id = json.loads(data)['userId']
        userId = int(user_id)
        print('Recommande')
        ee=matrice_emb_art
        # Choix de l'article le derniere
        value =  interact_small[(interact_small['user_id']==userId) & 
                        (interact_small['click_timestamp'] == 
                                    interact_small[interact_small['user_id']==
                                                    userId].click_timestamp.max())].click_article_id[0:1].values[0]
        #get all articles read by user
        var= interact_small.loc[interact_small ['user_id']==userId]['click_article_id'].tolist()
        for i in range(0, len(var)):
            if i != value:
                ee=np.delete(ee,[i],0)
        arr=[]
        
        #delecte selected article in the new matrix
        f=np.delete(ee,[value],0)
        #get 5 articles the most similar to the selected one
        for i in range(0,5):
            distances = cosine_similarity([ee[value]], f)[0]
            min_index = np.argmin(distances)
            f=np.delete(f,[min_index],0)
            #find corresponding matrix in original martix
            result = np.where(matrice_emb_art == f[min_index])
            arr.append(str(result[0][0]))   

        print("5 results")
        return arr
        
    except Exception as e:
        error = str(e)
        return error