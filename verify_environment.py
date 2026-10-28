#!/usr/bin/env python
"""
Verification script to test all module imports and dependencies.
Run this to ensure your environment is properly configured.
"""

import sys

def test_imports():
    """Test all required imports."""
    
    print("="*60)
    print("TESTING ML PIPELINE ENVIRONMENT")
    print("="*60)
    
    test_results = []
    
    # Test Python version
    print(f"\nPython Version: {sys.version}")
    if sys.version_info >= (3, 11):
        print("✓ Python 3.11+ detected")
        test_results.append(True)
    else:
        print("✗ Python 3.11+ required")
        test_results.append(False)
    
    # Test core libraries
    libraries = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'cv2': 'OpenCV',
        'tensorflow': 'TensorFlow',
        'keras': 'Keras',
        'qiskit': 'Qiskit',
        'joblib': 'Joblib'
    }
    
    print("\nTesting Libraries:")
    print("-" * 60)
    
    for module_name, display_name in libraries.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {display_name:<20} {version}")
            test_results.append(True)
        except ImportError as e:
            print(f"✗ {display_name:<20} FAILED: {e}")
            test_results.append(False)
    
    # Test project modules
    print("\nTesting Project Modules:")
    print("-" * 60)
    
    project_modules = [
        'data_preprocessing',
        'cnn_feature_extraction',
        'cnn_model',
        'svm_model',
        'qsvm_model',
        'qvc_model',
        'model_evaluation'
    ]
    
    for module_name in project_modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name}")
            test_results.append(True)
        except ImportError as e:
            print(f"✗ {module_name} FAILED: {e}")
            test_results.append(False)
        except Exception as e:
            print(f"⚠ {module_name} WARNING: {e}")
    
    # Summary
    print("\n" + "="*60)
    passed = sum(test_results)
    total = len(test_results)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("="*60)
    
    if all(test_results):
        print("\n✓ All imports successful! Environment is ready.")
        print("\nYou can now run:")
        print("  python main.py                    # Full pipeline")
        print("  python verify_environment.py      # This script")
        return True
    else:
        print("\n✗ Some imports failed. Please check your installation.")
        print("\nTo fix missing packages, run:")
        print("  .venv\\Scripts\\python.exe -m pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)