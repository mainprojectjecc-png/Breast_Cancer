import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def extract_features_from_layer(model, X_data, layer_index=-2):
    """
    Extract features from a specific layer of the CNN model.
    layer_index: -2 means second last layer (before output layer)
    """
    from tensorflow.keras.models import Model as KerasModel
    
    feature_extractor = KerasModel(inputs=model.input, outputs=model.layers[layer_index].output)
    features = feature_extractor.predict(X_data)
    
    return features

def flatten_features(features):
    """
    Flatten multi-dimensional features to 2D array.
    """
    if len(features.shape) > 2:
        return features.reshape(features.shape[0], -1)
    return features

def apply_pca(X_train, X_test, n_components=50):
    """
    Apply PCA for dimensionality reduction.
    """
    print(f"Applying PCA with {n_components} components...")
    
    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    
    explained_variance = np.sum(pca.explained_variance_ratio_)
    print(f"Explained variance ratio: {explained_variance:.4f}")
    
    return X_train_pca, X_test_pca, pca

def apply_standardization(X_train, X_test):
    """
    Standardize features using StandardScaler.
    """
    print("Applying standardization...")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, scaler

def plot_pca_variance(pca, n_components_to_show=None):
    """
    Plot cumulative explained variance ratio.
    """
    if n_components_to_show is None:
        n_components_to_show = min(50, len(pca.explained_variance_ratio_))
    
    cumsum = np.cumsum(pca.explained_variance_ratio_[:n_components_to_show])
    
    plt.figure(figsize=(10, 6))
    plt.plot(cumsum, marker='o')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance Ratio')
    plt.title('PCA - Cumulative Explained Variance')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('pca_variance.png')
    plt.show()

def extract_and_reduce_features(X_train, X_test, n_components=50, apply_standardize=True):
    """
    Complete feature extraction and reduction pipeline.
    """
    print("\n=== Feature Extraction and Reduction ===")
    
    # Flatten if necessary
    X_train_flat = flatten_features(X_train)
    X_test_flat = flatten_features(X_test)
    print(f"Original feature shape: {X_train_flat.shape}")
    
    # Standardization
    if apply_standardize:
        X_train_std, X_test_std, scaler = apply_standardization(X_train_flat, X_test_flat)
    else:
        X_train_std, X_test_std = X_train_flat, X_test_flat
        scaler = None
    
    # PCA
    if n_components < X_train_std.shape[1]:
        X_train_reduced, X_test_reduced, pca = apply_pca(X_train_std, X_test_std, n_components)
    else:
        X_train_reduced = X_train_std
        X_test_reduced = X_test_std
        pca = None
    
    print(f"Reduced feature shape: {X_train_reduced.shape}")
    print("=== Feature Extraction Complete ===\n")
    
    return X_train_reduced, X_test_reduced, scaler, pca

if __name__ == "__main__":
    # Example: Feature extraction from pre-trained model
    print("CNN Feature Extraction module loaded successfully.")