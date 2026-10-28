import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV
import joblib

def train_svm_classifier(X_train, y_train, kernel='rbf', C=1.0, gamma='scale'):
    """
    Train an SVM classifier.
    """
    print("Training SVM classifier...")
    svm_model = SVC(kernel=kernel, C=C, gamma=gamma, random_state=42)
    svm_model.fit(X_train, y_train)
    return svm_model

def evaluate_model(model, X_test, y_test, model_name="Model"):
    """
    Evaluate the trained model on test data.
    """
    print(f"Evaluating {model_name}...")
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"{model_name} Accuracy: {accuracy:.4f}")
    print(f"{model_name} Classification Report:\n{report}")

    return accuracy, report

def hyperparameter_tuning(X_train, y_train, param_grid=None):
    """
    Perform hyperparameter tuning for SVM using GridSearchCV.
    """
    if param_grid is None:
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1],
            'kernel': ['rbf', 'linear', 'poly']
        }

    print("Performing hyperparameter tuning...")
    svm = SVC(random_state=42)
    grid_search = GridSearchCV(svm, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_

def save_model(model, filename):
    """
    Save the trained model to disk.
    """
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")

def load_model(filename):
    """
    Load a trained model from disk.
    """
    model = joblib.load(filename)
    print(f"Model loaded from {filename}")
    return model

if __name__ == "__main__":
    # Example usage (assuming you have extracted features)
    # from cnn_feature_extraction import extract_and_reduce_features
    # from data_preprocessing import load_and_preprocess_data

    # Load and preprocess data
    # X_train, X_test, y_train, y_test, _ = load_and_preprocess_data("path/to/data")

    # Extract and reduce features
    # train_features, test_features, _, _ = extract_and_reduce_features(X_train, X_test)

    # Train SVM
    # svm_model = train_svm_classifier(train_features, y_train)

    # Evaluate
    # evaluate_model(svm_model, test_features, y_test, "SVM")

    # Optional: Hyperparameter tuning
    # best_model, best_params, best_score = hyperparameter_tuning(train_features, y_train)

    # Save model
    # save_model(best_model, 'svm_model.pkl')

    print("SVM model training module ready. Import and use train_svm_classifier function.")