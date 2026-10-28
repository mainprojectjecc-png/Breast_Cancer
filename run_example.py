#!/usr/bin/env python3
"""
Quick example runner - demonstrates how to use individual modules
Changes the dataset path to your actual dataset
"""

from data_preprocessing import load_and_preprocess_data

# IMPORTANT: Change this to your actual dataset path
DATASET_PATH = "path/to/your/dataset"  # <-- MODIFY THIS

print("="*60)
print("ML PIPELINE EXAMPLE RUNNER")
print("="*60)
print(f"\nDataset Path: {DATASET_PATH}")
print("\nTo use this example:")
print("1. Update DATASET_PATH variable with your dataset location")
print("2. Run: python run_example.py")
print("\nExpected dataset structure:")
print("  dataset/")
print("    ├── class1/")
print("    │   ├── image1.jpg")
print("    │   └── image2.jpg")
print("    └── class2/")
print("        ├── image3.jpg")
print("        └── image4.jpg")

import os
if not os.path.exists(DATASET_PATH):
    print(f"\n⚠️  ERROR: Dataset path not found: {DATASET_PATH}")
    print("Please update the DATASET_PATH variable in this file.")
    exit(1)

print("\n" + "="*60)
print("Starting pipeline...")
print("="*60)

# Step 1: Load data
print("\n[1/2] Loading and preprocessing data...")
X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data(DATASET_PATH)
print(f"✓ Training data shape: {X_train.shape}")
print(f"✓ Test data shape: {X_test.shape}")
print(f"✓ Classes: {label_encoder.classes_}")

print("\nNext steps (see main.py for full pipeline):")
print("  2. Train CNN model")
print("  3. Extract CNN features")
print("  4. Train SVM, QSVM, QVC models")
print("  5. Generate comparison report")

print("\n" + "="*60)
print("✓ Data loading example complete!")
print("="*60)