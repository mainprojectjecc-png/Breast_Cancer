"""
Main ML Pipeline Script
Orchestrates data preprocessing, feature extraction, and model training/evaluation
for CNN, SVM, QSVM, and QVC models.
"""

import numpy as np
import os
import sys
from data_preprocessing import load_and_preprocess_data, augment_data
from cnn_model import train_cnn_model, evaluate_cnn_model, save_cnn_model, load_cnn_model
from svm_model import train_svm_classifier, evaluate_model as evaluate_svm, save_model, load_model
from qsvm_model import prepare_data_for_qsvm, train_qsvm_classifier, evaluate_qsvm_model, save_qsvm_model
from qvc_model import prepare_data_for_qvc, train_qvc_classifier, evaluate_qvc_model, save_qvc_model
from model_evaluation import generate_comprehensive_report

def main():
    """
    Main pipeline for training and evaluating all models.
    """
    
    print("="*60)
    print("ML PIPELINE: CNN, SVM, QSVM, and QVC")
    print("="*60)
    
    # Step 1: Load and preprocess data
    print("\nStep 1: Loading and preprocessing data...")
    data_path = "path/to/your/dataset"  # CHANGE THIS to your actual dataset path
    
    if not os.path.exists(data_path):
        print(f"\n[WARNING] Dataset path not found: {data_path}")
        print("Please update the 'data_path' variable with your actual dataset directory.")
        print("\nExample directory structure:")
        print("  dataset/")
        print("    - class1/")
        print("      - image1.jpg")
        print("      - image2.jpg")
        print("    - class2/")
        print("      - image3.jpg")
        print("      - image4.jpg")
        return
    
    X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data(data_path)
    print(f"[OK] Data loaded. Training shape: {X_train.shape}, Test shape: {X_test.shape}")
    
    # Step 2: Train CNN Model
    print("\nStep 2: Training CNN model...")
    cnn_model, history = train_cnn_model(X_train, y_train, X_test, y_test, epochs=10)
    cnn_train_acc, cnn_report = evaluate_cnn_model(cnn_model, X_test, y_test)
    save_cnn_model(cnn_model, 'models/cnn_model.h5')
    print(f"[OK] CNN model trained. Accuracy: {cnn_train_acc:.4f}")
    
    # Extract CNN features for SVM, QSVM, QVC
    print("\nStep 3: Extracting CNN features for other models...")
    from cnn_model import extract_features_from_cnn
    train_features = extract_features_from_cnn(cnn_model, X_train, layer_name='flatten')
    test_features = extract_features_from_cnn(cnn_model, X_test, layer_name='flatten')
    print(f"[OK] Features extracted. Shape: {train_features.shape}")
    
    # Step 4: Train Classical SVM
    print("\nStep 4: Training Classical SVM...")
    svm_model = train_svm_classifier(train_features, y_train, kernel='rbf', C=1.0)
    svm_acc, svm_report = evaluate_svm(svm_model, test_features, y_test, "SVM")
    save_model(svm_model, 'models/svm_model.pkl')
    print(f"[OK] SVM model trained. Accuracy: {svm_acc:.4f}")
    
    # Step 5: Train Quantum SVM
    print("\nStep 5: Preparing data and training Quantum SVM...")
    X_train_qsvm, X_test_qsvm, y_train_qsvm, y_test_qsvm, scaler_qsvm = prepare_data_for_qsvm(
        train_features, test_features, y_train, y_test, max_features=4
    )
    qsvm_model, _ = train_qsvm_classifier(X_train_qsvm, y_train_qsvm)
    qsvm_acc, qsvm_report = evaluate_qsvm_model(qsvm_model, X_test_qsvm, y_test_qsvm)
    save_qsvm_model(qsvm_model, scaler_qsvm, 'models/qsvm_model')
    print(f"[OK] QSVM model trained. Accuracy: {qsvm_acc:.4f}")
    
    # Step 6: Train Quantum Variational Classifier
    print("\nStep 6: Preparing data and training Quantum Variational Classifier...")
    X_train_qvc, X_test_qvc, y_train_qvc, y_test_qvc, scaler_qvc = prepare_data_for_qvc(
        train_features, test_features, y_train, y_test, max_features=4
    )
    num_classes = len(np.unique(y_train_qvc))
    qvc_model, _, _ = train_qvc_classifier(X_train_qvc, y_train_qvc, num_classes, max_iter=50)
    qvc_acc, qvc_report = evaluate_qvc_model(qvc_model, X_test_qvc, y_test_qvc)
    save_qvc_model(qvc_model, scaler_qvc, 'models/qvc_model')
    print(f"[OK] QVC model trained. Accuracy: {qvc_acc:.4f}")
    
    # Step 7: Generate comprehensive report
    print("\nStep 7: Generating comprehensive comparison report...")
    all_models = {
        'CNN': {'model': cnn_model, 'type': 'cnn'},
        'SVM': {'model': svm_model, 'type': 'svm'},
        'QSVM': {'model': qsvm_model, 'type': 'qsvm'},
        'QVC': {'model': qvc_model, 'type': 'qvc'}
    }
    
    results = generate_comprehensive_report(all_models, X_test, y_test, label_encoder.classes_)
    
    # Print summary
    print("\n" + "="*60)
    print("TRAINING SUMMARY")
    print("="*60)
    print(f"CNN Accuracy:      {cnn_train_acc:.4f}")
    print(f"SVM Accuracy:      {svm_acc:.4f}")
    print(f"QSVM Accuracy:     {qsvm_acc:.4f}")
    print(f"QVC Accuracy:      {qvc_acc:.4f}")
    print("="*60)
    print("\n[SUCCESS] All models trained successfully!")
    print("  - Models saved in 'models/' directory")
    print("  - Comparison report saved as 'model_comparison_report.txt'")
    print("  - Visualizations saved (confusion matrices, ROC curves, etc.)")

if __name__ == "__main__":
    main()
