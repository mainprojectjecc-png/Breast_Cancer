import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from sklearn.preprocessing import label_binarize
import joblib

def plot_confusion_matrix(y_true, y_pred, class_names, model_name="Model"):
    """
    Plot confusion matrix for classification results.
    """
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title(f'Confusion Matrix - {model_name}')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.tight_layout()
    plt.savefig(f'{model_name.lower().replace(" ", "_")}_confusion_matrix.png')
    plt.show()

def plot_roc_curves(y_true, y_scores, class_names, model_name="Model"):
    """
    Plot ROC curves for multi-class classification.
    """
    # Binarize the labels
    y_true_bin = label_binarize(y_true, classes=np.arange(len(class_names)))
    n_classes = len(class_names)

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_scores[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Plot all ROC curves
    plt.figure(figsize=(10, 8))

    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label=f'ROC curve of {class_names[i]} (area = {roc_auc[i]:.2f})')

    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Multi-class ROC - {model_name}')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(f'{model_name.lower().replace(" ", "_")}_roc_curves.png')
    plt.show()

def compare_model_accuracies(models_results, model_names):
    """
    Compare accuracies of different models.
    """
    accuracies = [result[0] for result in models_results]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(model_names, accuracies, color=['blue', 'green', 'red', 'purple'])
    plt.title('Model Accuracy Comparison')
    plt.xlabel('Models')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1)

    # Add value labels on bars
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{acc:.4f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('model_comparison.png')
    plt.show()

def save_model_results(results, filename):
    """
    Save model evaluation results to a file.
    """
    with open(filename, 'w') as f:
        for model_name, (accuracy, report) in results.items():
            f.write(f"=== {model_name} ===\n")
            f.write(f"Accuracy: {accuracy:.4f}\n")
            f.write("Classification Report:\n")
            f.write(report)
            f.write("\n\n")

    print(f"Model results saved to {filename}")

def load_model_results(filename):
    """
    Load model evaluation results from a file.
    """
    results = {}
    with open(filename, 'r') as f:
        content = f.read()

    # Simple parsing (you might want to improve this)
    sections = content.split('=== ')[1:]
    for section in sections:
        lines = section.split('\n')
        model_name = lines[0].strip()
        accuracy = float(lines[1].split(': ')[1])
        report_start = lines.index("Classification Report:") + 1
        report = '\n'.join(lines[report_start:-2])  # Remove empty lines at end
        results[model_name] = (accuracy, report)

    print(f"Model results loaded from {filename}")
    return results

def generate_comprehensive_report(all_models, X_test, y_test, class_names):
    """
    Generate a comprehensive report comparing all models.
    """
    print("Generating comprehensive model comparison report...")

    results = {}
    model_names = []

    for model_name, model_info in all_models.items():
        model = model_info['model']
        model_type = model_info['type']

        print(f"\nEvaluating {model_name} ({model_type})...")

        if model_type in ['cnn', 'qvc']:
            # For models that output probabilities
            y_pred_proba = model.predict(X_test)
            if model_type == 'cnn':
                y_pred = np.argmax(y_pred_proba, axis=1)
                y_scores = y_pred_proba
            else:
                y_pred = y_pred_proba
                y_scores = y_pred_proba  # For binary classification, this might need adjustment
        else:
            # For SVM-like models
            y_pred = model.predict(X_test)
            # For ROC curves, we need probability scores
            if hasattr(model, 'predict_proba'):
                y_scores = model.predict_proba(X_test)
            elif hasattr(model, 'decision_function'):
                y_scores = model.decision_function(X_test)
            else:
                # If no probability scores available, skip ROC
                y_scores = None

        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        results[model_name] = (accuracy, report)
        model_names.append(model_name)

        print(f"{model_name} Accuracy: {accuracy:.4f}")

        # Plot confusion matrix
        plot_confusion_matrix(y_test, y_pred, class_names, model_name)

        # Plot ROC curves if scores are available
        if y_scores is not None and len(class_names) <= 10:  # Limit for readability
            plot_roc_curves(y_test, y_scores, class_names, model_name)

    # Compare accuracies
    compare_model_accuracies(list(results.values()), model_names)

    # Save results
    save_model_results(results, 'model_comparison_report.txt')

    return results

if __name__ == "__main__":
    # Example usage
    # from data_preprocessing import load_and_preprocess_data
    # from cnn_model import load_cnn_model
    # from svm_model import load_model as load_svm
    # from qsvm_model import load_qsvm_model
    # from qvc_model import load_qvc_model

    # Load data
    # X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data("path/to/data")
    # class_names = label_encoder.classes_

    # Load trained models
    # all_models = {
    #     'CNN': {'model': load_cnn_model('cnn_model.h5'), 'type': 'cnn'},
    #     'SVM': {'model': load_svm('svm_model.pkl'), 'type': 'svm'},
    #     'QSVM': {'model': load_qsvm_model('qsvm_model')[0], 'type': 'qsvm'},
    #     'QVC': {'model': load_qvc_model('qvc_model')[0], 'type': 'qvc'}
    # }

    # Generate report
    # results = generate_comprehensive_report(all_models, X_test, y_test, class_names)

    print("Model evaluation and visualization module ready.")
    print("Import and use generate_comprehensive_report function to compare all models.")