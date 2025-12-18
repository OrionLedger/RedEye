import pandas as pd
from sklearn.cluster import KMeans

def k_mean_train(y:pd.DataFrame, n_clusters=3, randoma_state=42):
    kmeans = KMeans(n_clusters=n_clusters, random_state=randoma_state)
    kmeans.fit(y)

    return kmeans