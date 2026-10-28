import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt

def build_cnn_model(input_shape, num_classes):
    """
    Build a Convolutional Neural Network model.
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model

def train_cnn_model(X_train, y_train, X_test, y_test, epochs=50, batch_size=32):
    """
    Train the CNN model.
    """
    input_shape = X_train.shape[1:]
    num_classes = len(np.unique(y_train))

    model = build_cnn_model(input_shape, num_classes)

    # Callbacks
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model_checkpoint = ModelCheckpoint('best_cnn_model.h5', save_best_only=True, monitor='val_accuracy')

    print("Training CNN model...")
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping, model_checkpoint]
    )

    return model, history

def evaluate_cnn_model(model, X_test, y_test):
    """
    Evaluate the trained CNN model.
    """
    print("Evaluating CNN model...")
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)

    accuracy = accuracy_score(y_test, y_pred_classes)
    report = classification_report(y_test, y_pred_classes)

    print(f"CNN Accuracy: {accuracy:.4f}")
    print(f"CNN Classification Report:\n{report}")

    return accuracy, report

def extract_features_from_cnn(model, X_data, layer_name='flatten'):
    """
    Extract features from an intermediate layer of the CNN.
    """
    # Create a model that outputs features from the specified layer
    feature_extractor = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)

    # Extract features
    features = feature_extractor.predict(X_data)

    return features

def plot_training_history(history):
    """
    Plot training and validation accuracy/loss.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()

    # Loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('cnn_training_history.png')
    plt.show()

def save_cnn_model(model, filename):
    """
    Save the trained CNN model.
    """
    model.save(filename)
    print(f"CNN model saved to {filename}")

def load_cnn_model(filename):
    """
    Load a trained CNN model.
    """
    model = tf.keras.models.load_model(filename)
    print(f"CNN model loaded from {filename}")
    return model

if __name__ == "__main__":
    # Example usage
    # from data_preprocessing import load_and_preprocess_data

    # Load and preprocess data
    # X_train, X_test, y_train, y_test, _ = load_and_preprocess_data("path/to/data")

    # Train CNN
    # cnn_model, history = train_cnn_model(X_train, y_train, X_test, y_test)

    # Evaluate
    # evaluate_cnn_model(cnn_model, X_test, y_test)

    # Plot training history
    # plot_training_history(history)

    # Extract features for other models
    # features = extract_features_from_cnn(cnn_model, X_train)

    # Save model
    # save_cnn_model(cnn_model, 'cnn_model.h5')

    print("CNN model training module ready. Import and use train_cnn_model function.")