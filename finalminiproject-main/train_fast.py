"""
Fast ML Training - CNN and SVM only
Trains the fastest models first for quick evaluation
"""

import numpy as np
import os
import sys

print("="*60)
print("FAST ML TRAINING: CNN + SVM")
print("="*60)

# Step 1: Load data
print("\nStep 1: Loading and preprocessing data...")
try:
    from data_preprocessing import load_and_preprocess_data
    data_path = r"C:\Users\USER\Downloads\finalminiproject-main\finalminiproject-main\10253-20260326T214604Z-1-001\10253"
   
    if not os.path.exists(data_path):
        print(f"Error: Dataset path not found: {data_path}")
        sys.exit(1)
    
    print("     Loading images...")
    X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data(data_path)
    print(f"[OK] Data loaded.")
    print(f"     Training: {X_train.shape}, Test: {X_test.shape}")
    print(f"     Classes: {label_encoder.classes_}")
except Exception as e:
    print(f"Error during data loading: {e}")
    sys.exit(1)

# Step 2: Train CNN
print("\nStep 2: Training CNN model (10 epochs)...")
try:
    from cnn_model import train_cnn_model, evaluate_cnn_model, save_cnn_model
    print("     This will take 2-5 minutes...")
    cnn_model, history = train_cnn_model(X_train, y_train, X_test, y_test, epochs=10)
    cnn_acc, cnn_report = evaluate_cnn_model(cnn_model, X_test, y_test)
    save_cnn_model(cnn_model, 'models/cnn_model.h5')
    print(f"[OK] CNN trained. Accuracy: {cnn_acc:.4f}")
except Exception as e:
    print(f"Error during CNN training: {e}")
    cnn_acc = 0

# Step 3: Extract features for SVM
print("\nStep 3: Extracting features for SVM...")
try:
    from cnn_feature_extraction import extract_and_reduce_features
    print("     Applying PCA...")
    train_features, test_features, scaler, pca = extract_and_reduce_features(
        X_train, X_test, n_components=50, apply_standardize=True
    )
    print(f"[OK] Features extracted. Shape: {train_features.shape}")
except Exception as e:
    print(f"Error during feature extraction: {e}")
    train_features = X_train.reshape(X_train.shape[0], -1)
    test_features = X_test.reshape(X_test.shape[0], -1)

# Step 4: Train SVM
print("\nStep 4: Training SVM classifier...")
try:
    from svm_model import train_svm_classifier, evaluate_model as evaluate_svm, save_model
    print("     This will take 1-3 minutes...")
    svm_model = train_svm_classifier(train_features, y_train, kernel='rbf', C=1.0)
    svm_acc, svm_report = evaluate_svm(svm_model, test_features, y_test, "SVM")
    save_model(svm_model, 'models/svm_model.pkl')
    print(f"[OK] SVM trained. Accuracy: {svm_acc:.4f}")
except Exception as e:
    print(f"Error during SVM training: {e}")
    svm_acc = 0

# Summary
print("\n" + "="*60)
print("TRAINING RESULTS")
print("="*60)
print(f"CNN Accuracy: {cnn_acc:.4f}")
print(f"SVM Accuracy: {svm_acc:.4f}")
print("="*60)
print("\nNext step: Train Quantum models separately")
print("  - Quantum SVM (QSVM): Great for feature classification")
print("  - Quantum Variational Classifier (QVC): Quantum ML approach")
print("\nModels saved in 'models/' directory")
