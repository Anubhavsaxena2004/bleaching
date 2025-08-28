# Full Python script for predicting coral bleaching events.
# Revised version with improved target variable creation.

# --- Core Libraries ---
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.impute import SimpleImputer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
try:
    df = pd.read_csv('global_bleaching_environmental.csv', encoding='ISO-8859-1', low_memory=False, na_values=['nd'])
    print("Dataset loaded successfully!")
    print("Shape of the dataset:", df.shape)
except FileNotFoundError:
    print("Error: File not found.")
    exit()
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

# Data Preprocessing
print("\n--- Starting Data Preprocessing ---")

# Select relevant columns including both Bleaching_Level and Percent_Bleaching
relevant_cols = [
    'SSTA_DHW',
    'TSA_DHW',
    'Temperature_Maximum',
    'Turbidity',
    'Depth_m',
    'Bleaching_Level',
    'Percent_Bleaching'
]
df_clean = df[relevant_cols].copy()

# Create target variable using both columns
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

print(f"Shape after creating target variable: {df_clean.shape}")
print("Value counts for the target variable 'bleaching_event':")
print(df_clean['bleaching_event'].value_counts())

# Separate features and target
X = df_clean.drop(['bleaching_event', 'Bleaching_Level', 'Percent_Bleaching'], axis=1)
y = df_clean['bleaching_event']

# Handle missing values in features
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)
X = pd.DataFrame(X_imputed, columns=X.columns)

print("Final shape of features (X):", X.shape)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\n--- Class Distribution After Split ---")
print("Training set distribution:")
print(y_train.value_counts())
print("Testing set distribution:")
print(y_test.value_counts())

# Train and evaluate model
print("\n--- Starting Model Training and Evaluation ---")
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['No Bleaching (0)', 'Bleaching (1)']))

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['No Bleaching', 'Bleaching'], 
            yticklabels=['No Bleaching', 'Bleaching'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Feature importance
importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)

print("\nMost Important Features:")
print(feature_importance_df)

plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feature_importance_df)
plt.title('Feature Importance')
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.tight_layout()
plt.show()

print("\n--- Project Complete ---")

import joblib

# This is the 'model' variable you already trained
# joblib.dump saves your model into a file
joblib.dump(model, 'coral_bleaching_model.joblib')

print("Model saved successfully as coral_bleaching_model.joblib")