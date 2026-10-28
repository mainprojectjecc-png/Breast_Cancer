import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_machine_learning.algorithms import QSVC
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib

def prepare_data_for_qsvm(X_train, X_test, y_train, y_test, max_features=4):
    """
    Prepare classical data for quantum SVM by selecting and scaling features.
    """
    print("Preparing data for Quantum SVM...")

    # For QSVM, we need to reduce features to a small number (typically 2-4 for current quantum devices)
    # Select the most important features (you can modify this based on your feature importance)
    if X_train.shape[1] > max_features:
        # Simple feature selection: take first max_features
        X_train_q = X_train[:, :max_features]
        X_test_q = X_test[:, :max_features]
    else:
        X_train_q = X_train
        X_test_q = X_test

    # Scale features to [0, 1] range as required by quantum circuits
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_train_scaled = scaler.fit_transform(X_train_q)
    X_test_scaled = scaler.transform(X_test_q)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def create_quantum_kernel(feature_dim):
    """
    Create a quantum kernel for QSVM.
    """
    print(f"Creating quantum kernel for {feature_dim} features...")
    
    # Import feature map
    from qiskit.circuit.library import ZZFeatureMap
    
    # Create feature map with the appropriate dimension
    feature_map = ZZFeatureMap(feature_dimension=feature_dim, reps=2)
    
    # Use FidelityQuantumKernel with the feature map
    quantum_kernel = FidelityQuantumKernel(feature_map=feature_map, evaluate_duplicates='all')

    return quantum_kernel

def train_qsvm_classifier(X_train, y_train, quantum_kernel=None):
    """
    Train a Quantum Support Vector Machine classifier.
    """
    print("Training Quantum SVM classifier...")

    if quantum_kernel is None:
        quantum_kernel = create_quantum_kernel(X_train.shape[1])

    # Initialize QSVC
    qsvm = QSVC(quantum_kernel=quantum_kernel)

    # Train the model
    qsvm.fit(X_train, y_train)

    return qsvm, quantum_kernel

def evaluate_qsvm_model(qsvm, X_test, y_test):
    """
    Evaluate the trained QSVM model.
    """
    print("Evaluating Quantum SVM model...")

    y_pred = qsvm.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"QSVM Accuracy: {accuracy:.4f}")
    print(f"QSVM Classification Report:\n{report}")

    return accuracy, report

def save_qsvm_model(qsvm, scaler, filename_prefix):
    """
    Save the trained QSVM model and scaler.
    """
    joblib.dump(qsvm, f'{filename_prefix}_qsvm.pkl')
    joblib.dump(scaler, f'{filename_prefix}_scaler.pkl')
    print(f"QSVM model and scaler saved with prefix: {filename_prefix}")

def load_qsvm_model(filename_prefix):
    """
    Load a trained QSVM model and scaler.
    """
    qsvm = joblib.load(f'{filename_prefix}_qsvm.pkl')
    scaler = joblib.load(f'{filename_prefix}_scaler.pkl')
    print(f"QSVM model and scaler loaded with prefix: {filename_prefix}")
    return qsvm, scaler

def predict_with_qsvm(qsvm, scaler, X_new):
    """
    Make predictions with the trained QSVM on new data.
    """
    # Scale the new data
    X_scaled = scaler.transform(X_new)

    # Make predictions
    predictions = qsvm.predict(X_scaled)

    return predictions

if __name__ == "__main__":
    # Example usage
    # from data_preprocessing import load_and_preprocess_data
    # from cnn_feature_extraction import extract_and_reduce_features

    # Load and preprocess data
    # X_train, X_test, y_train, y_test, _ = load_and_preprocess_data("path/to/data")

    # Extract features (optional, for better performance)
    # train_features, test_features, _, _ = extract_and_reduce_features(X_train, X_test, n_components=10)

    # Prepare data for QSVM
    # X_train_q, X_test_q, y_train_q, y_test_q, scaler = prepare_data_for_qsvm(train_features, test_features, y_train, y_test)

    # Train QSVM
    # qsvm_model, quantum_kernel = train_qsvm_classifier(X_train_q, y_train_q)

    # Evaluate
    # evaluate_qsvm_model(qsvm_model, X_test_q, y_test_q)

    # Save model
    # save_qsvm_model(qsvm_model, scaler, 'qsvm_model')

    print("Quantum SVM model training module ready. Import and use train_qsvm_classifier function.")
    print("Note: Requires Qiskit and Qiskit Machine Learning packages.")