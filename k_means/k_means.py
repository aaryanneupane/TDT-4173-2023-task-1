import numpy as np 
import pandas as pd 
# IMPORTANT: DO NOT USE ANY OTHER 3RD PARTY PACKAGES
# (math, random, collections, functools, etc. are perfectly fine)


class KMeans:
    
    def __init__(self, k = 2):
        # NOTE: Feel free add any hyperparameters 
        # (with defaults) as you see fit
        self.k = k
        self.centroids = None
        self.maxIt = 500

    def init_centroids(self, X: pd.DataFrame):
        #Select a random centroid from the given data set X
        centroids = np.array(X.sample().to_numpy())   

        # make X into a numpy array
        X = np.array(X.to_numpy())

        #While the amount of centroids is less than the given k, this assigns a new centroid according to the furthest distance from the previous centroids
        while len(centroids) < self.k:
            #Find distance between all points and centroids
            distances = np.array(cross_euclidean_distance(X, centroids))

            #Find distance from point to its centroid, by finding the minimum distance of the centroids  
            distance_to_nearest = distances.min(axis=1)

            #Find the point furthest away from its centroid, in order to add it as a new centroid
            max_index_row = np.argmax(distance_to_nearest)

            #Add as new centroid
            centroids = np.append(centroids, [X[max_index_row]], axis=0) 

        return centroids
    
        
    def fit(self, X: pd.DataFrame):
        """
        Estimates parameters for the classifier
            
        Args:
            X (array<m,n>): a matrix of floats with
                m rows (#samples) and n columns (#features)
        """
        # TODO: Implement 

        #Initialise the centroids and choose the one with the lowest distortion score
        best_centroids = None
        self.centroids = self.init_centroids(X)
        distortion_score = euclidean_distortion(X, self.predict(X))

        for _ in range(15):
            new_centroids = self.init_centroids(X)
            self.centroids = new_centroids  
            new_distortion_score = euclidean_distortion(X, self.predict(X))
            if new_distortion_score < distortion_score:
                distortion_score = new_distortion_score
                best_centroids = new_centroids

        #Assign the best centroids to the class 
        self.centroids = best_centroids

        # make X into a numpy array
        X = np.array(X.to_numpy())

        for iteration in range(self.maxIt):
            distances = cross_euclidean_distance(X, self.centroids)  # Calculate distances between the given data and centroids
            assigned_points = np.argmin(distances, axis=1) #Assigning a cluster to each given data point by the closest distance

            # Creating new centroids in the positional mean of each cluster by using list comprehension
            new_centroids = np.array([X[assigned_points == temp].mean(axis=0) for temp in range(self.k)])

            # Convolution check for the centroids
            if np.all(new_centroids == self.centroids):
                break

            self.centroids = new_centroids
    
    def predict(self, X: pd.DataFrame):
        """
        Generates predictions
        
        Note: should be called after .fit()
        
        Args:
            X (array<m,n>): a matrix of floats with 
                m rows (#samples) and n columns (#features)
            
        Returns:
            A length m integer array with cluster assignments
            for each point. E.g., if X is a 10xn matrix and 
            there are 3 clusters, then a possible assignment
            could be: array([2, 0, 0, 1, 2, 1, 1, 0, 2, 2])
        """
        # TODO: Implement 

    # make X into a numpy array 
        X = np.array(X.to_numpy())
    #Calculate the distances between the given data points and the ultimate centroids after fit()
        distances = cross_euclidean_distance(X, self.centroids)
    #Return the assigned centroid for each data point in the format [ cluster k, k-3, k-1 ,...., k] the size is determined by size(X)
        return np.argmin(distances, axis=1)
    
    def get_centroids(self):
        """
        Returns the centroids found by the K-mean algorithm
        
        Example with m centroids in an n-dimensional space:
        >>> model.get_centroids()
        numpy.array([
            [x1_1, x1_2, ..., x1_n],
            [x2_1, x2_2, ..., x2_n],
                    .
                    .
                    .
            [xm_1, xm_2, ..., xm_n]
        ])
        """

    #Return the centroids of a given Kmeans class
        return self.centroids
    
    
    
    
# --- Some utility functions 

def euclidean_distance(x, y):
    """
    Computes euclidean distance between two sets of points 
    
    Note: by passing "y=0.0", it will compute the euclidean norm
    
    Args:
        x, y (array<...,n>): float tensors with pairs of 
            n-dimensional points 
            
    Returns:
        A float array of shape <...> with the pairwise distances
        of each x and y point
    """
    return np.linalg.norm(x - y, ord=2, axis=-1)

def cross_euclidean_distance(x, y=None):
    """
    
    
    """
    y = x if y is None else y 
    assert len(x.shape) >= 2
    assert len(y.shape) >= 2
    return euclidean_distance(x[..., :, None, :], y[..., None, :, :])


def euclidean_distortion(X: pd.DataFrame, z):
    """
    Computes the Euclidean K-means distortion
    
    Args:
        X (array<m,n>): m x n float matrix with datapoints 
        z (array<m>): m-length integer vector of cluster assignments
    
    Returns:
        A scalar float with the raw distortion measure 
    """
    X, z = np.asarray(X), np.asarray(z)

    assert len(X.shape) == 2
    assert len(z.shape) == 1
    assert X.shape[0] == z.shape[0]
    
    distortion = 0.0
    clusters = np.unique(z)
    for i, c in enumerate(clusters):
        Xc = X[z == c]
        mu = Xc.mean(axis=0)
        distortion += ((Xc - mu) ** 2).sum()
        
    return distortion


def euclidean_silhouette(X, z):
    """
    Computes the average Silhouette Coefficient with euclidean distance 
    
    More info:
        - https://www.sciencedirect.com/science/article/pii/0377042787901257
        - https://en.wikipedia.org/wiki/Silhouette_(clustering)
    
    Args:
        X (array<m,n>): m x n float matrix with datapoints 
        z (array<m>): m-length integer vector of cluster assignments
    
    Returns:
        A scalar float with the silhouette score
    """
    X, z = np.asarray(X), np.asarray(z)
    assert len(X.shape) == 2
    assert len(z.shape) == 1
    assert X.shape[0] == z.shape[0]
    
    # Compute average distances from each x to all other clusters
    clusters = np.unique(z)
    D = np.zeros((len(X), len(clusters)))
    for i, ca in enumerate(clusters):
        for j, cb in enumerate(clusters):
            in_cluster_a = z == ca
            in_cluster_b = z == cb
            d = cross_euclidean_distance(X[in_cluster_a], X[in_cluster_b])
            div = d.shape[1] - int(i == j)
            D[in_cluster_a, j] = d.sum(axis=1) / np.clip(div, 1, None)
    
    # Intra distance 
    a = D[np.arange(len(X)), z]
    # Smallest inter distance 
    inf_mask = np.where(z[:, None] == clusters[None], np.inf, 0)
    b = (D + inf_mask).min(axis=1)
    
    return np.mean((b - a) / np.maximum(a, b))

#To find a random point in the given data set X to initialise the first centroids
def random_init(X, k):
        n_samples, _ = X.shape
        # Randomly select k unique indices from the data points
        centroid_indices = np.random.choice(n_samples, size=k, replace=False)
        # Use the selected indices to extract the corresponding data points as centroids
        centroids = X.loc[centroid_indices]
        return centroids
  