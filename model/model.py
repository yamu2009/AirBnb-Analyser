import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

def train_model(input_path, model_output_path):
    """
    Trains a Random Forest Regressor on the provided dataset.

    Args:
        input_path (str): Path to the input CSV file.
        model_output_path (str): Path where the trained model will be saved.
    """
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)

    # Features and Target
    X = df.drop('price', axis=1)
    y = df['price']

    # Identify categorical and numerical columns
    categorical_cols = [c for c in X.columns if X[c].dtype == 'object']
    numerical_cols = [c for c in X.columns if X[c].dtype in ['int64', 'float64']]

    print(f"Training on features: {X.columns.tolist()}")
    print(f"Categorical: {categorical_cols}")
    print(f"Numerical: {numerical_cols}")

    # Preprocessing Pipeline
    # We use OneHotEncoder for categorical variables
    # handle_unknown='ignore' is crucial for production if new categories appear
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])

    # Model Pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    print("Training Random Forest Regressor...")
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model Performance:")
    print(f"MAE: ${mae:.2f}")
    print(f"R² Score: {r2:.3f}")

    # Save
    print(f"Saving model to {model_output_path}...")
    joblib.dump(model, model_output_path)
    print("Model saved successfully.")

    # Example Prediction
    example_input = X_test.iloc[0:1]
    prediction = model.predict(example_input)
    print(f"Example Prediction for inputs: \n{example_input.to_dict(orient='records')[0]}")
    print(f"Predicted Price: ${prediction[0]:.2f}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(base_dir, 'data', 'listings_cleaned.csv')
    model_path = os.path.join(base_dir, 'model', 'rf_model.pkl')
    
    train_model(input_csv, model_path)
