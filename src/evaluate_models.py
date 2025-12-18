import numpy as np
import pandas as pd
from eval.load_model import load_kmeans_model
from eval.models.kmeans_model import evaluate_kmeans_model
from preprocessing.users import cat_label_features_encoder, one_hot_features_encoder, standard_scale, clean_users, log_transform
# from repo.users.T_Users_Retrieving import fetch_T_users

# mock_users = fetch_T_users().iloc[150000:]

def evaluate_k_means_users_clustering(X):
    print("Evaluating KMeans model Started ...")
    X = clean_users(X)
    X = standard_scale(X)
    X = X.select_dtypes(include=['number'])
    print(X)
    model = load_kmeans_model()
    score = evaluate_kmeans_model(model, X, 25000)
    
    return score