# Quick Start Guide - ML Pipeline

## Directory Structure

Your project is now organized as:
```
finalminiproject-main/
├── .venv/                           (Python 3.11 virtual environment)
├── models/                          (Trained model storage)
├── main.py                          (Full pipeline - MAIN SCRIPT)
├── run_example.py                   (Example with dataset loading)
├── run_pipeline.bat                 (Windows batch runner)
├── verify_environment.py            (Test all dependencies)
│
├── Data & Preprocessing
├── data_preprocessing.py            (Load & preprocess images)
├── cnn_feature_extraction.py       (Feature extraction & PCA)
│
├── Models
├── cnn_model.py                    (CNN with TensorFlow)
├── svm_model.py                    (Classical SVM)
├── qsvm_model.py                   (Quantum SVM)
├── qvc_model.py                    (Quantum Variational Classifier)
│
├── Evaluation
├── model_evaluation.py             (Metrics & visualizations)
│
├── Configuration
├── requirements.txt                (Python dependencies)
├── README.md                       (Full documentation)
└── QUICKSTART.md                   (This file)
```

## Setup Status

✅ **Python 3.11.9** - Installed and configured
✅ **Virtual Environment** - Created at `.venv`
✅ **All Dependencies** - Installed (TensorFlow, Qiskit, scikit-learn, etc.)
✅ **Project Files** - All Python modules ready
✅ **Environment Verified** - All imports tested successfully

## How to Run

### Option 1: Run Full Pipeline (RECOMMENDED)
```powershell
cd c:\Users\USER\Downloads\finalminiproject-main
.\run_pipeline.bat
```
Or from PowerShell:
```powershell
.venv\Scripts\python.exe main.py
```

### Option 2: Run Example with Your Dataset
First, update the dataset path in `run_example.py`:
```python
DATASET_PATH = "C:\\path\\to\\your\\dataset"  # <-- Change this
```

Then run:
```powershell
.venv\Scripts\python.exe run_example.py
```

### Option 3: Verify Environment
Check that all libraries are properly installed:
```powershell
.venv\Scripts\python.exe verify_environment.py
```

## Before Running Main Pipeline

### Step 1: Prepare Your Dataset
Your dataset must be organized as:
```
your_dataset/
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

**Supported formats:** JPG, PNG, BMP, TIFF, etc. (OpenCV supported formats)

### Step 2: Update main.py with Your Dataset Path
Open `main.py` and find this line:
```python
data_path = "path/to/your/dataset"  # CHANGE THIS to your actual path
```

Change it to:
```python
data_path = "C:\\Users\\USER\\MyDataset"  # Your dataset path
```

### Step 3: Run the Pipeline
```powershell
.venv\Scripts\python.exe main.py
```

## What the Pipeline Does

1. **Data Preprocessing** - Loads, resizes, normalizes images
2. **CNN Training** - Trains a Convolutional Neural Network
3. **Feature Extraction** - Extracts features from CNN
4. **Model Training** - Trains multiple models:
   - Classical SVM
   - Quantum SVM (QSVM)
   - Quantum Variational Classifier (QVC)
5. **Model Evaluation** - Generates:
   - Confusion matrices for each model
   - ROC curves for multi-class classification
   - Accuracy comparison
   - Detailed classification reports

## Output Files

After running `main.py`, you'll get:
- `models/cnn_model.h5` - Trained CNN
- `models/svm_model.pkl` - Trained SVM
- `models/qsvm_model_qsvm.pkl` - Trained QSVM
- `models/qvc_model_qvc.pkl` - Trained QVC
- `model_comparison_report.txt` - Detailed comparison
- `cnn_training_history.png` - Training curves
- `model_comparison.png` - Accuracy comparison
- `*_confusion_matrix.png` - Confusion matrices for each model
- `*_roc_curves.png` - ROC curves for each model

## Troubleshooting

### Issue: "No such file or directory: main.py"
**Solution:** Make sure you're in the parent directory:
```powershell
cd c:\Users\USER\Downloads\finalminiproject-main
```

### Issue: "Dataset path not found"
**Solution:** Update the `data_path` variable in `main.py` with the full path to your dataset.

### Issue: Out of memory while training
**Solution:** Reduce these in `main.py`:
- `epochs=10` (lower number)
- Image size in `load_and_preprocess_data()` (e.g., 32x32 instead of 64x64)
- Batch size in cnn_model training

### Issue: "TensorFlow/Qiskit import error"
**Solution:** Reinstall packages:
```powershell
.venv\Scripts\python.exe -m pip install --upgrade tensorflow qiskit
```

## Modifying the Pipeline

### Change CNN Architecture
Edit `cnn_model.py` function `build_cnn_model()`:
- Add/remove Conv2D and MaxPooling layers
- Change activation functions
- Modify Dense layer sizes

### Adjust SVM Hyperparameters
Edit `svm_model.py` function `hyperparameter_tuning()`:
```python
param_grid = {
    'C': [0.1, 1, 10, 100],           # Regularization
    'gamma': ['scale', 'auto', 0.001],  # Kernel coefficient
    'kernel': ['rbf', 'linear', 'poly'] # Kernel type
}
```

### Tune Quantum Models
Edit `qsvm_model.py` or `qvc_model.py`:
- `max_features=4` - Number of quantum features
- `max_iter=100` - Number of optimization iterations
- Feature map type (ZZ, RY, etc.)

## Key Files Reference

| File | Purpose |
|------|---------|
| `main.py` | **START HERE** - Full pipeline orchestrator |
| `data_preprocessing.py` | Image loading & preprocessing |
| `cnn_model.py` | CNN implementation |
| `svm_model.py` | Classical SVM |
| `qsvm_model.py` | Quantum SVM |
| `qvc_model.py` | Quantum Variational Classifier |
| `model_evaluation.py` | Evaluation metrics & visualization |
| `cnn_feature_extraction.py` | Feature extraction & PCA |

## Python Environment Info

- **Python Version:** 3.11.9
- **Virtual Environment:** `.venv/`
- **TensorFlow Version:** 2.21.0
- **Qiskit Version:** 2.3.1
- **Scikit-learn Version:** 1.8.0

To view all installed packages:
```powershell
.venv\Scripts\python.exe -m pip list
```

## Next Steps

1. ✅ Environment setup complete
2. ⏳ Prepare your dataset
3. ⏳ Update `data_path` in main.py
4. ⏳ Run: `.venv\Scripts\python.exe main.py`
5. ⏳ Analyze results in output files

## Need Help?

- Check `README.md` for detailed module documentation
- Review `requirements.txt` for available packages
- Run `verify_environment.py` to test all imports
- Check output files for model metrics and visualizations

## Commands Reference

```powershell
# Activate venv
.venv\Scripts\activate

# Run main pipeline
.venv\Scripts\python.exe main.py

# Run with data loading example
.venv\Scripts\python.exe run_example.py

# Verify environment
.venv\Scripts\python.exe verify_environment.py

# Install/update packages
.venv\Scripts\python.exe -m pip install -r requirements.txt

# List installed packages
.venv\Scripts\python.exe -m pip list
```

---

**Setup Date:** March 27, 2026  
**Status:** ✅ READY TO USE