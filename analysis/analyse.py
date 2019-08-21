from trackerstudies.utils import load_runs
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import EllipticEnvelope
from MulticoreTSNE import MulticoreTSNE as TSNE
from sklearn import svm
import pandas
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import umap

def load_data():
    # Load the pandas dataframe
    runs = load_runs()  # First time will take a while

    runs = runs.loc[runs.fill__era.isin([ "2018D","2018C","2018B","2018A"]), :]
    runs = runs.loc[runs.reco.isin(["express", "prompt"]), :]
    runs = runs.loc[runs["Hits.Pixel.mean"] > 0, :]
    runs = runs.loc[runs["Hits.Strip.mean"] > 0, :]

    runs.tracking = pandas.Categorical(runs.tracking, ["GOOD", "BAD"])
    runs.bad_reason.fillna("GOOD", inplace=True)

    runs.reset_index(inplace=True)  # Reset index

    return runs

def run_principal_component_analysis(runs):

    # Decide what features you want
    column_names = list(runs)
    feature_tokens = [
        ".rms",
        "mean",
    ]  # Only features for the RMS and mean value of histograms
    my_feature_list = [
        column
        for column in column_names
        if any(token in column for token in feature_tokens) or column in ["recorded_lumi"]
    ]  # List of feature column names

    # Extract feature matrix
    feature_df = runs[my_feature_list].copy()
    feature_df.fillna(0, inplace=True)  # Handle missing values
    feature_df.reset_index(inplace=True)  # Reset Index
    X = feature_df.loc[:, :].values  # Create feature matrix

    # Extract labels
    label_column_names = [
        "run_number",
        "fill_number",
        "reco",
        "fill__era",
        "pixel",
        "strip",
        "tracking",
        "bad_reason",
    ]
    labels = runs[label_column_names]

    y = runs.tracking.cat.codes
    # y = pandas.Categorical(runs.tracking, ["GOOD", "BAD"]).codes

    # Feature scaling
    X = StandardScaler().fit_transform(X)

    ## PCA
    number_of_principal_components = 2
    pca = PCA(n_components=number_of_principal_components)
    classifier = pca.fit(X)
    principal_components = classifier.transform(X)
    variance_ratio = sum(pca.explained_variance_ratio_)
    eigenvalues = pca.explained_variance_
    ## Create a PCA Dataframe
    pca_df = pandas.DataFrame(principal_components, columns=["pca1", "pca2"])
    pca_df = pandas.concat([pca_df, labels], axis=1)
    pca_df.sort_values(["tracking", "run_number"], inplace=True)

    bad_reason_colors = [
        (0.7019607843137254, 0.7019607843137254, 0.7019607843137254),
        (0.6509803921568628, 0.807843137254902, 0.8901960784313725),
        (0.12156862745098039, 0.47058823529411764, 0.7058823529411765),
        (0.6980392156862745, 0.8745098039215686, 0.5411764705882353),
        (0.2, 0.6274509803921569, 0.17254901960784313),
        (0.984313725490196, 0.6039215686274509, 0.6),
        (0.8901960784313725, 0.10196078431372549, 0.10980392156862745),
        (0.9921568627450981, 0.7490196078431373, 0.43529411764705883),
        (1.0, 0.4980392156862745, 0.0),
        (0.792156862745098, 0.6980392156862745, 0.8392156862745098),
        (0.41568627450980394, 0.23921568627450981, 0.6039215686274509),
        (1.0, 1.0, 0.6),
        (0.6941176470588235, 0.34901960784313724, 0.1568627450980392),
    ]

    return pca_df

def run_tsne(runs):

    # Decide what features you want
    column_names = list(runs)
    feature_tokens = [
        ".rms",
        "mean",
    ]  # Only features for the RMS and mean value of histograms
    my_feature_list = [
        column
        for column in column_names
        if any(token in column for token in feature_tokens)
        and "charge" in column
        or column in ["recorded_lumi", "delivered_lumi"]
    ]  # List of feature column names

    # Extract feature matrix
    feature_df = runs[my_feature_list].copy()
    feature_df.fillna(0, inplace=True)  # Handle missing values
    X = feature_df.loc[:, :].values  # Create feature matrix

    X = StandardScaler().fit_transform(X)

    tsne = TSNE(learning_rate=50.0)
    tsne_components = tsne.fit_transform(X)

    tsne_df = pandas.DataFrame(tsne_components, columns=["tsne1", "tsne2"])

    big_df = pandas.concat([runs, tsne_df], axis=1)

    return big_df

def run_umap(runs):

    # Decide what features you want
    column_names = list(runs)
    feature_tokens = [
        ".rms",
        "mean",
    ]  # Only features for the RMS and mean value of histograms
    my_feature_list = [
        column
        for column in column_names
        if any(token in column for token in feature_tokens)
        and "charge" in column
        or column in ["recorded_lumi", "delivered_lumi"]
    ]  # List of feature column names

    # Extract feature matrix
    feature_df = runs[my_feature_list].copy()
    feature_df.fillna(0, inplace=True)  # Handle missing values
    X = feature_df.loc[:, :].values  # Create feature matrix

    X = StandardScaler().fit_transform(X)

    umap_inst = umap.UMAP(n_neighbors=20, metric="manhattan", min_dist=0.2)
    umap_components = umap_inst.fit_transform(X)

    umap_df = pandas.DataFrame(umap_components, columns=["umap1", "umap2"])

    big_df = pandas.concat([runs, umap_df], axis=1)

    return big_df 

