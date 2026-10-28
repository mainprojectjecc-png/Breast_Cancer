import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import cv2
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_and_preprocess_data(data_path, image_size=(64, 64)):
    """
    Load and preprocess image data for classification.
    Assumes data is organized in folders by class.
    """
    images = []
    labels = []

    for class_name in os.listdir(data_path):
        class_path = os.path.join(data_path, class_name)
        if os.path.isdir(class_path):
            for image_name in os.listdir(class_path):
                image_path = os.path.join(class_path, image_name)
                try:
                    image = cv2.imread(image_path)
                    image = cv2.resize(image, image_size)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    images.append(image)
                    labels.append(class_name)
                except Exception as e:
                    print(f"Error loading {image_path}: {e}")

    # Convert to numpy arrays
    X = np.array(images)
    y = np.array(labels)

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Normalize pixel values
    X = X.astype('float32') / 255.0

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, label_encoder

def augment_data(X_train, y_train, augmentation_factor=2):
    """
    Augment training data using ImageDataGenerator.
    """
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2
    )

    augmented_images = []
    augmented_labels = []

    for i in range(len(X_train)):
        image = X_train[i]
        label = y_train[i]

        # Original image
        augmented_images.append(image)
        augmented_labels.append(label)

        # Augmented images
        image = np.expand_dims(image, axis=0)
        for batch in datagen.flow(image, batch_size=1):
            augmented_images.append(batch[0])
            augmented_labels.append(label)
            if len(augmented_images) >= len(X_train) * augmentation_factor:
                break

    return np.array(augmented_images), np.array(augmented_labels)

if __name__ == "__main__":
    # Example usage
    data_path = "path/to/your/dataset"  # Replace with actual path
    X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data(data_path)
    print(f"Training data shape: {X_train.shape}")
    print(f"Test data shape: {X_test.shape}")
    print(f"Number of classes: {len(label_encoder.classes_)}")