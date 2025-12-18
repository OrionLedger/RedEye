from sklearn.metrics import silhouette_score
import numpy as np

def evaluate_kmeans_model(model, X, sample_size, print_silhouette=True):
    labels = model.predict(X)
    print("Cluster counts:")
    unique, counts = np.unique(labels, return_counts=True)
    for cluster, count in zip(unique, counts):
        print(f"Cluster {cluster}: {count} samples")
    
    print("\nCluster centers:")
    print(model.cluster_centers_)
    
    if print_silhouette:
        if X.shape[0] > 1 and len(unique) > 1:
            print('Start calculating Score ...')
            score = silhouette_score(X, labels, sample_size=sample_size)
            print(f"\nSilhouette Score: {score:.4f}")
        else:
            print("\nSilhouette Score: Cannot compute (need >1 sample and >1 cluster)")
    
    return score
