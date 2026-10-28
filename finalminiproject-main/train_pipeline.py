"""
Simplified ML Training Pipeline
Trains CNN, SVM, QSVM, and QVC models with proper error handling
"""

import numpy as np
import os
import sys

print("="*60)
print("ML PIPELINE: CNN, SVM, QSVM, and QVC")
print("="*60)

# Step 1: Load data
print("\nStep 1: Loading and preprocessing data...")
try:
    from data_preprocessing import load_and_preprocess_data
    data_path = r"C:\Users\USER\Downloads\finalminiproject-main\finalminiproject-main\10253-20260326T214604Z-1-001\10253"
    
    if not os.path.exists(data_path):
        print(f"Error: Dataset path not found: {data_path}")
        sys.exit(1)
    
    X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data(data_path)
    print(f"[OK] Data loaded.")
    print(f"     Training shape: {X_train.shape}")
    print(f"     Test shape: {X_test.shape}")
    print(f"     Classes: {label_encoder.classes_}")
except Exception as e:
    print(f"Error during data loading: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 2: Train CNN Model
print("\nStep 2: Training CNN model...")
try:
    from cnn_model import train_cnn_model, evaluate_cnn_model, save_cnn_model
    cnn_model, history = train_cnn_model(X_train, y_train, X_test, y_test, epochs=10)
    cnn_train_acc, cnn_report = evaluate_cnn_model(cnn_model, X_test, y_test)
    save_cnn_model(cnn_model, 'models/cnn_model.h5')
    print(f"[OK] CNN model trained.")
    print(f"     Accuracy: {cnn_train_acc:.4f}")
except Exception as e:
    print(f"Error during CNN training: {e}")
    import traceback
    traceback.print_exc()
    cnn_train_acc = 0
    cnn_report = "Failed"

# Step 3: Extract features using flattened CNN output
print("\nStep 3: Extracting features for classical models...")
try:
    from cnn_feature_extraction import extract_and_reduce_features
    # Use raw image data flattened for feature extraction
    train_features, test_features, scaler, pca = extract_and_reduce_features(
        X_train, X_test, n_components=50, apply_standardize=True
    )
    print(f"[OK] Features extracted and reduced.")
    print(f"     Feature shape: {train_features.shape}")
except Exception as e:
    print(f"Error during feature extraction: {e}")
    import traceback
    traceback.print_exc()
    train_features = X_train.reshape(X_train.shape[0], -1)
    test_features = X_test.reshape(X_test.shape[0], -1)

# Step 4: Train Classical SVM
print("\nStep 4: Training Classical SVM...")
try:
    from svm_model import train_svm_classifier, evaluate_model as evaluate_svm, save_model
    svm_model = train_svm_classifier(train_features, y_train, kernel='rbf', C=1.0)
    svm_acc, svm_report = evaluate_svm(svm_model, test_features, y_test, "SVM")
    save_model(svm_model, 'models/svm_model.pkl')
    print(f"[OK] SVM model trained.")
    print(f"     Accuracy: {svm_acc:.4f}")
except Exception as e:
    print(f"Error during SVM training: {e}")
    import traceback
    traceback.print_exc()
    svm_acc = 0
    svm_report = "Failed"

# Step 5: Train Quantum SVM
print("\nStep 5: Training Quantum SVM...")
try:
    from qsvm_model import prepare_data_for_qsvm, train_qsvm_classifier, evaluate_qsvm_model, save_qsvm_model
    X_train_qsvm, X_test_qsvm, y_train_qsvm, y_test_qsvm, scaler_qsvm = prepare_data_for_qsvm(
        train_features, test_features, y_train, y_test, max_features=4
    )
    qsvm_model, _ = train_qsvm_classifier(X_train_qsvm, y_train_qsvm)
    qsvm_acc, qsvm_report = evaluate_qsvm_model(qsvm_model, X_test_qsvm, y_test_qsvm)
    save_qsvm_model(qsvm_model, scaler_qsvm, 'models/qsvm_model')
    print(f"[OK] QSVM model trained.")
    print(f"     Accuracy: {qsvm_acc:.4f}")
except Exception as e:
    print(f"Error during QSVM training: {e}")
    import traceback
    traceback.print_exc()
    qsvm_acc = 0
    qsvm_report = "Failed"

# Step 6: Train Quantum Variational Classifier
print("\nStep 6: Training Quantum Variational Classifier...")
try:
    from qvc_model import prepare_data_for_qvc, train_qvc_classifier, evaluate_qvc_model, save_qvc_model
    X_train_qvc, X_test_qvc, y_train_qvc, y_test_qvc, scaler_qvc = prepare_data_for_qvc(
        train_features, test_features, y_train, y_test, max_features=4
    )
    qvc_model, _, _ = train_qvc_classifier(X_train_qvc, y_train_qvc, max_iter=50)
    qvc_acc, qvc_report = evaluate_qvc_model(qvc_model, X_test_qvc, y_test_qvc)
    save_qvc_model(qvc_model, scaler_qvc, 'models/qvc_model')
    print(f"[OK] QVC model trained.")
    print(f"     Accuracy: {qvc_acc:.4f}")
except Exception as e:
    print(f"Error during QVC training: {e}")
    import traceback
    traceback.print_exc()
    qvc_acc = 0
    qvc_report = "Failed"

# Step 7: Summary
print("\n" + "="*60)
print("TRAINING SUMMARY")
print("="*60)
print(f"CNN  Accuracy: {cnn_train_acc:.4f}")
print(f"SVM  Accuracy: {svm_acc:.4f}")
print(f"QSVM Accuracy: {qsvm_acc:.4f}")
print(f"QVC  Accuracy: {qvc_acc:.4f}")
print("="*60)
print("\n[SUCCESS] All models trained!")
print("  - Models saved in 'models/' directory")
print("  - Check model files for predictions")
