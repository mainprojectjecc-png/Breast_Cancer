#!/usr/bin/env python3
"""
Test script to verify Flask API is working
"""
import requests
import os
from pathlib import Path

BASE_URL = 'http://localhost:5000'

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"Health Check: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_models_info():
    """Test the models info endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/models/info')
        print(f"Models Info: {response.json()}")
        return True
    except Exception as e:
        print(f"Models info failed: {e}")
        return False

def test_predict_with_sample():
    """Test prediction with a sample image"""
    try:
        # Use a sample image from the sample_dataset
        sample_image_path = Path('sample_dataset/class_0/class_0_000.jpg')
        
        if not sample_image_path.exists():
            print(f"Sample image not found: {sample_image_path}")
            return False
        
        with open(sample_image_path, 'rb') as f:
            files = {'image': f}
            data = {'model': 'hybrid'}
            response = requests.post(f'{BASE_URL}/predict', files=files, data=data)
        
        result = response.json()
        print(f"\nPrediction Result:")
        print(f"Status: {result.get('status')}")
        if 'models' in result:
            for model, prediction in result['models'].items():
                if 'error' not in prediction:
                    print(f"  {model}: {prediction['class_name']} (confidence: {prediction['confidence']:.2%})")
                else:
                    print(f"  {model}: Error - {prediction['error']}")
        
        return result.get('status') == 'success'
    except Exception as e:
        print(f"Prediction test failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Testing Flask API")
    print("=" * 60)
    
    print("\n1. Testing /health endpoint...")
    test_health_endpoint()
    
    print("\n2. Testing /models/info endpoint...")
    test_models_info()
    
    print("\n3. Testing /predict endpoint with sample image...")
    if test_predict_with_sample():
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed")
    
    print("\n" + "=" * 60)
