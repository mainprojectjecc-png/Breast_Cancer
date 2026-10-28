import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit_machine_learning.algorithms import VQC
from qiskit_machine_learning.optimizers import COBYLA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib

def prepare_data_for_qvc(X_train, X_test, y_train, y_test, max_features=4):
    """
    Prepare classical data for Quantum Variational Classifier.
    """
    print("Preparing data for Quantum Variational Classifier...")

    # For QVC, we need to reduce features to a small number (typically 2-4 for current quantum devices)
    if X_train.shape[1] > max_features:
        # Simple feature selection: take first max_features
        X_train_q = X_train[:, :max_features]
        X_test_q = X_test[:, :max_features]
    else:
        X_train_q = X_train
        X_test_q = X_test

    # Scale features to [0, 1] range
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_train_scaled = scaler.fit_transform(X_train_q)
    X_test_scaled = scaler.transform(X_test_q)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def create_quantum_circuit(num_features, num_classes):
    """
    Create a quantum circuit for variational classification.
    """
    print(f"Creating quantum circuit for {num_features} features and {num_classes} classes...")

    # Feature map
    feature_map = ZZFeatureMap(feature_dimension=num_features, reps=2)

    # Variational ansatz
    ansatz = RealAmplitudes(num_features, reps=2)

    return feature_map, ansatz

def train_qvc_classifier(X_train, y_train, max_iter=100):
    """
    Train a Quantum Variational Classifier.
    """
    print("Training Quantum Variational Classifier...")

    num_features = X_train.shape[1]
    
    # Import necessary Qiskit components
    from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
    from qiskit_machine_learning.algorithms import VQC
    from qiskit_machine_learning.optimizers import COBYLA
    
    # Create feature map
    feature_map = ZZFeatureMap(feature_dimension=num_features, reps=2)

    # Create variational ansatz
    ansatz = RealAmplitudes(num_features, reps=2)

    # Initialize VQC - note: no num_classes parameter in newer versions
    optimizer = COBYLA(maxiter=max_iter)
    qvc = VQC(
        feature_map=feature_map,
        ansatz=ansatz,
        optimizer=optimizer
    )

    # Train the model
    qvc.fit(X_train, y_train)

    return qvc, feature_map, ansatz

def evaluate_qvc_model(qvc, X_test, y_test):
    """
    Evaluate the trained QVC model.
    """
    print("Evaluating Quantum Variational Classifier...")

    y_pred = qvc.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"QVC Accuracy: {accuracy:.4f}")
    print(f"QVC Classification Report:\n{report}")

    return accuracy, report

def save_qvc_model(qvc, scaler, filename_prefix):
    """
    Save the trained QVC model and scaler.
    """
    joblib.dump(qvc, f'{filename_prefix}_qvc.pkl')
    joblib.dump(scaler, f'{filename_prefix}_scaler.pkl')
    print(f"QVC model and scaler saved with prefix: {filename_prefix}")

def load_qvc_model(filename_prefix):
    """
    Load a trained QVC model and scaler.
    """
    qvc = joblib.load(f'{filename_prefix}_qvc.pkl')
    scaler = joblib.load(f'{filename_prefix}_scaler.pkl')
    print(f"QVC model and scaler loaded with prefix: {filename_prefix}")
    return qvc, scaler

def predict_with_qvc(qvc, scaler, X_new):
    """
    Make predictions with the trained QVC on new data.
    """
    # Scale the new data
    X_scaled = scaler.transform(X_new)

    # Make predictions
    predictions = qvc.predict(X_scaled)

    return predictions

if __name__ == "__main__":
    # Example usage
    # from data_preprocessing import load_and_preprocess_data
    # from cnn_feature_extraction import extract_and_reduce_features

    # Load and preprocess data
    # X_train, X_test, y_train, y_test, _ = load_and_preprocess_data("path/to/data")

    # Extract features (optional, for better performance)
    # train_features, test_features, _, _ = extract_and_reduce_features(X_train, X_test, n_components=10)

    # Prepare data for QVC
    # X_train_q, X_test_q, y_train_q, y_test_q, scaler = prepare_data_for_qvc(train_features, test_features, y_train, y_test)

    # Train QVC
    # num_classes = len(np.unique(y_train_q))
    # qvc_model, feature_map, ansatz = train_qvc_classifier(X_train_q, y_train_q, num_classes)

    # Evaluate
    # evaluate_qvc_model(qvc_model, X_test_q, y_test_q)

    # Save model
    # save_qvc_model(qvc_model, scaler, 'qvc_model')

    print("Quantum Variational Classifier training module ready. Import and use train_qvc_classifier function.")
    print("Note: Requires Qiskit and Qiskit Machine Learning packages.")