import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, roc_curve, auc

def load_and_preprocess_data(filepath):
    """Loads and preprocesses the data exactly as done during training to ensure valid testing."""
    print("Loading dataset...")
    df = pd.read_csv(filepath, encoding='ISO-8859-1', low_memory=False, na_values=['nd'])
    
    relevant_cols = [
        'SSTA_DHW', 'TSA_DHW', 'Temperature_Maximum', 
        'Turbidity', 'Depth_m', 'Bleaching_Level', 'Percent_Bleaching'
    ]
    df_clean = df[relevant_cols].copy()

    def create_target(row):
        if row['Bleaching_Level'] == 'No Bleaching':
            return 0
        elif pd.notna(row['Bleaching_Level']):
            return 1
        elif row['Percent_Bleaching'] == 0:
            return 0
        elif pd.notna(row['Percent_Bleaching']):
            return 1
        else:
            return np.nan

    df_clean['bleaching_event'] = df_clean.apply(create_target, axis=1)
    df_clean.dropna(subset=['bleaching_event'], inplace=True)

    X = df_clean.drop(['bleaching_event', 'Bleaching_Level', 'Percent_Bleaching'], axis=1)
    y = df_clean['bleaching_event']

    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    X = pd.DataFrame(X_imputed, columns=X.columns)

    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

def generate_curves():
    # 1. Load Data and Split
    X_train, X_test, y_train, y_test = load_and_preprocess_data('global_bleaching_environmental.csv')
    
    # 2. Load the Pre-trained Model
    print("Loading saved model...")
    try:
        model = joblib.load('coral_bleaching_model_balanced.joblib')
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Error: 'coral_bleaching_model_balanced.joblib' not found. Ensure the file is in the directory.")
        return

    # 3. Get Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] # Get probabilities for the positive class (Bleaching)

    # ==========================================
    # FIGURE 5.1: CONFUSION MATRIX
    # ==========================================
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['No Bleaching', 'Bleaching'], 
                yticklabels=['No Bleaching', 'Bleaching'],
                annot_kws={"size": 14})
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('Actual Label', fontsize=12, fontweight='bold')
    plt.title('Figure 5.1: Random Forest Confusion Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300)
    plt.show()

    # ==========================================
    # FIGURE 5.2: ROC-AUC CURVE
    # ==========================================
    plt.figure(figsize=(8, 6))
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'Random Forest ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Guess')
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (FPR)', fontsize=12, fontweight='bold')
    plt.ylabel('True Positive Rate (TPR)', fontsize=12, fontweight='bold')
    plt.title('Figure 5.2: Receiver Operating Characteristic (ROC) Curve', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right", fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('roc_curve.png', dpi=300)
    plt.show()

    # ==========================================
    # FIGURE 5.3: FEATURE IMPORTANCE
    # ==========================================
    plt.figure(figsize=(10, 6))
    importances = model.feature_importances_
    feature_names = X_test.columns
    
    # Sort features by importance
    indices = np.argsort(importances)[::-1]
    sorted_features = [feature_names[i] for i in indices]
    sorted_importances = importances[indices]

    sns.barplot(x=sorted_importances, y=sorted_features, palette='viridis')
    plt.title('Figure 5.3: Feature Importance Analysis', fontsize=14, fontweight='bold')
    plt.xlabel('Gini Importance Score', fontsize=12, fontweight='bold')
    plt.ylabel('Environmental Variables', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    generate_curves()