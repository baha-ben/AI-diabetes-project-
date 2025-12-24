import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

# ====== DATA LOADING =====
# Load the diabetes dataset from CSV file
# Dataset: Pima Indians Diabetes Database
data = pd.read_csv("dataset\\diabetes.csv") 

# Display first 5 rows to verify data loaded correctly
print("Dataset Preview:")
print(data.head())
print("\nDataset Shape:", data.shape)
print("\nColumn Names:", data.columns.tolist())

# X: All columns except 'Outcome' (8 features)
X = data.drop("Outcome", axis=1)


## y: 'Outcome' column (0 = Not Diabetic, 1 = Diabetic)
y = data["Outcome"]

# ===== TRAIN-TEST SPLIT =====
# Split dataset into training and testing sets
# 80% for training, 20% for testing
# random_state=42 ensures reproducible results
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% of data for testing
    random_state=42     # For reproducibility
)

print("\nTraining set size:", X_train.shape[0])
print("Testing set size:", X_test.shape[0])

# ===== MODEL TRAINING =====
# Create Random Forest Classifier
# Random Forest is an ensemble method that combines multiple decision trees
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()


# Train the model on training data
model.fit(X_train, y_train)
print("Model training completed!")

from sklearn.metrics import accuracy_score
# Make predictions on test set
y_pred = model.predict(X_test)

# Calculate accuracy: percentage of correct predictions
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")


#Matrix 
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_pred))



# ==== SAVE MODEL =====
# Save the trained model to a file using joblib
# This model will be loaded by the main application
model_path = "models\\diabetes_model.pkl"
joblib.dump(model, model_path)
print(f"\nModel saved successfully to: {model_path}")
print("The model is ready to be used in the application!")




