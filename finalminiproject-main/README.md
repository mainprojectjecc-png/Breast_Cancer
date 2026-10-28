# ML Pipeline: CNN, SVM, QSVM, and QVC

A comprehensive machine learning project implementing deep learning and quantum machine learning models for image classification.

## Project Structure

```
finalminiproject-main/
├── data_preprocessing.py          # Data loading, normalization, augmentation
├── cnn_feature_extraction.py      # Feature extraction and dimensionality reduction
├── cnn_model.py                   # Convolutional Neural Network implementation
├── svm_model.py                   # Classical Support Vector Machine
├── qsvm_model.py                  # Quantum Support Vector Machine
├── qvc_model.py                   # Quantum Variational Classifier
├── model_evaluation.py            # Model evaluation and visualization
├── main.py                        # Main pipeline orchestrator
├── requirements.txt               # Project dependencies
├── models/                        # Directory for saving trained models
└── README.md                      # This file
```

## Installed Libraries

- **Core ML**: NumPy, Pandas, Scikit-learn
- **Deep Learning**: TensorFlow, Keras
- **Quantum ML**: Qiskit, Qiskit-Aer, Qiskit-Machine-Learning
- **Visualization**: Matplotlib, Seaborn
- **Image Processing**: OpenCV
- **Python Version**: 3.11.9

## Setup Instructions

### 1. Create Virtual Environment (Already Done)
The virtual environment is already set up with Python 3.11 in `.venv/`

### 2. Install Dependencies
```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Module Descriptions

### 1. `data_preprocessing.py`
Handles all data loading and preprocessing tasks:
- Load images from directory structure
- Resize and normalize images
- Encode labels
- Split train/test data
- Data augmentation (rotation, flip, zoom, etc.)

**Usage:**
```python
from data_preprocessing import load_and_preprocess_data

X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data("path/to/dataset")
```

### 2. `cnn_feature_extraction.py`
Feature extraction and dimensionality reduction:
- Extract features from CNN intermediate layers
- Apply PCA for dimensionality reduction
- Standardize features
- Visualize variance explained

**Usage:**
```python
from cnn_feature_extraction import extract_and_reduce_features

train_features, test_features, scaler, pca = extract_and_reduce_features(X_train, X_test, n_components=50)
```

### 3. `cnn_model.py`
CNN implementation for image classification:
- Build CNN architecture (Conv2D → MaxPooling → Dense)
- Train with early stopping and checkpoints
- Extract features from intermediate layers
- Evaluate and visualize training history

**Usage:**
```python
from cnn_model import train_cnn_model, evaluate_cnn_model

cnn_model, history = train_cnn_model(X_train, y_train, X_test, y_test, epochs=50)
accuracy, report = evaluate_cnn_model(cnn_model, X_test, y_test)
```

### 4. `svm_model.py`
Classical Support Vector Machine:
- Train SVM with various kernels (rbf, linear, poly)
- Hyperparameter tuning using GridSearchCV
- Model evaluation with classification metrics
- Save/load trained models

**Usage:**
```python
from svm_model import train_svm_classifier, evaluate_model

svm_model = train_svm_classifier(X_train, y_train)
accuracy, report = evaluate_model(svm_model, X_test, y_test, "SVM")
```

### 5. `qsvm_model.py`
Quantum Support Vector Machine using Qiskit:
- Prepare data for quantum circuits (scale to [0,1])
- Create quantum kernels using fidelity
- Train QSVC with quantum feature maps
- Support for feature reduction

**Usage:**
```python
from qsvm_model import prepare_data_for_qsvm, train_qsvm_classifier

X_train_q, X_test_q, y_train_q, y_test_q, scaler = prepare_data_for_qsvm(X_train, X_test, y_train, y_test)
qsvm_model, kernel = train_qsvm_classifier(X_train_q, y_train_q)
```

### 6. `qvc_model.py`
Quantum Variational Classifier using Qiskit:
- Design quantum circuits with feature maps and ansatz
- Train using COBYLA optimizer
- Variational quantum algorithm for classification
- Support feature reduction for quantum hardware

**Usage:**
```python
from qvc_model import prepare_data_for_qvc, train_qvc_classifier

X_train_q, X_test_q, y_train_q, y_test_q, scaler = prepare_data_for_qvc(X_train, X_test, y_train, y_test)
qvc_model, feature_map, ansatz = train_qvc_classifier(X_train_q, y_train_q, num_classes=2)
```

### 7. `model_evaluation.py`
Comprehensive model evaluation and visualization:
- Confusion matrices
- ROC curves for multi-class classification
- Model accuracy comparison
- Generate detailed comparison reports
- Save evaluation results

**Usage:**
```python
from model_evaluation import generate_comprehensive_report

results = generate_comprehensive_report(all_models, X_test, y_test, class_names)
```

## Running the Full Pipeline

### Option 1: Run Main Script
```bash
.venv\Scripts\python.exe main.py
```

This will:
1. Load and preprocess your dataset
2. Train CNN model
3. Extract CNN features
4. Train SVM, QSVM, and QVC models
5. Generate comprehensive comparison report
6. Save all models and visualizations

### Option 2: Step-by-Step Execution
```python
# Load data
from data_preprocessing import load_and_preprocess_data
X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data("path/to/data")

# Train CNN
from cnn_model import train_cnn_model
cnn_model, history = train_cnn_model(X_train, y_train, X_test, y_test)

# Train SVM
from svm_model import train_svm_classifier
svm_model = train_svm_classifier(X_train, y_train)

# Train Quantum Models
from qsvm_model import prepare_data_for_qsvm, train_qsvm_classifier
X_train_q, X_test_q, y_train_q, y_test_q, scaler = prepare_data_for_qsvm(X_train, X_test, y_train, y_test)
qsvm_model, _ = train_qsvm_classifier(X_train_q, y_train_q)

# Evaluate all models
from model_evaluation import generate_comprehensive_report
results = generate_comprehensive_report(all_models, X_test, y_test, label_encoder.classes_)
```

## Dataset Format

Your dataset should be organized as follows:
```
dataset/
├── class1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── class2/
│   ├── image3.jpg
│   ├── image4.jpg
│   └── ...
└── classN/
    └── ...
```

## Output Files

After running the pipeline, you'll get:
- **models/cnn_model.h5** - Trained CNN model
- **models/svm_model.pkl** - Trained SVM model
- **models/qsvm_model_qsvm.pkl** - Trained QSVM model
- **models/qvc_model_qvc.pkl** - Trained QVC model
- **model_comparison_report.txt** - Detailed comparison of all models
- **cnn_training_history.png** - CNN training visualization
- **model_comparison.png** - Accuracy comparison bar chart
- **[model]_confusion_matrix.png** - Confusion matrices for each model
- **[model]_roc_curves.png** - ROC curves for each model

## Key Features

✓ **Data Preprocessing**: Image loading, normalization, augmentation
✓ **Deep Learning**: CNN implementation with TensorFlow
✓ **Feature Extraction**: CNN-based feature extraction with PCA
✓ **Classical ML**: SVM with hyperparameter tuning
✓ **Quantum ML**: QSVM and QVC implementations
✓ **Comprehensive Evaluation**: Metrics, visualizations, comparisons
✓ **Easy to Use**: Modular design for flexibility

## Customization

### Change CNN Architecture
Edit `cnn_model.py` `build_cnn_model()` function to modify layers, activations, etc.

### Adjust Data Preprocessing
Modify `data_preprocessing.py` to change image size, normalization method, or augmentation parameters.

### Tune Model Hyperparameters
- SVM: kernel, C, gamma
- CNNs: epochs, batch_size, learning_rate
- Quantum models: max_iter, ansatz depth

### Feature Reduction
- Modify `n_components` in PCA
- Change `max_features` for quantum models (typically 2-4 for current hardware)

## Requirements

- Python 3.11+
- All packages listed in `requirements.txt`
- Dataset in the correct directory structure

## Troubleshooting

### TensorFlow/Qiskit Import Errors
Make sure you're using Python 3.11 and have activated the virtual environment:
```bash
.venv\Scripts\activate  # On Windows
```

### Out of Memory Errors
- Reduce batch_size in `cnn_model.train_cnn_model()`
- Reduce image size in `data_preprocessing.load_and_preprocess_data()`
- Use fewer samples for training

### Quantum Models Running Slowly
- Reduce `max_iter` parameter
- Use fewer features (2-4 recommended)
- Quantum simulation is slower than classical methods

## References

- TensorFlow: https://tensorflow.org
- Scikit-learn: https://scikit-learn.org
- Qiskit: https://qiskit.org
- OpenCV: https://opencv.org

## Author

ML Pipeline Project - 2026

## License

MIT License