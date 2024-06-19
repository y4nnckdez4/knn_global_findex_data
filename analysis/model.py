import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline



def model(processed_data):

    # I specify my X
    X = processed_data.select_dtypes(include='float64')

    # I specify my preprocessing pipeline
    preproc = make_pipeline(SimpleImputer(strategy='median'), MinMaxScaler(), PCA(n_components=20))

    # I look at my X_processed
    X_processed = pd.DataFrame(preproc.fit_transform(X))

    # I define the algorithm (with the n. of clusters I want) and fit the data
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(X_processed)

    # I add a cluster according to they belong
    cluster_labels = kmeans.labels_
    processed_data['Cluster'] = cluster_labels

    return processed_data
