import os
import pandas as pd
import joblib
# from repo.users.T_Users_Retrieving import fetch_T_users
from preprocessing.users.clean_users import clean_users
from preprocessing.users.encode_cat_features import one_hot_features_encoder, cat_label_features_encoder
from preprocessing.users.scaling_users import standard_scale
from preprocessing.users import log_transform
from train.k_means_clustering import k_mean_train as train_k


def k_means_users_avtivities_training(users, model_saving_path = os.environ.get("MODELS")):
    print("Training K_Mean Clustering model Started ...")

    # users = fetch_T_users().iloc[:150000]
    users = clean_users(users)
    users = log_transform(users)


    scaled_users = standard_scale(users)

    users = users.select_dtypes(include=['number'])

    model = train_k(users)

    print("Labels: ")
    for label in model.labels_ : print(label)

    models_path = model_saving_path
    if models_path is None:
        raise EnvironmentError("Please set the MODELS environment variable to save the trained model.")

    os.makedirs(models_path, exist_ok=True)
    model_file = os.path.join(models_path, "kmeans_model.joblib")
    joblib.dump(model, model_file)

    print(f"Model saved to {model_file}")
    
    return model
