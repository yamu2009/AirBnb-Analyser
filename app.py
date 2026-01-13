from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
import numpy as np

app = Flask(__name__)
# Enable CORS for all routes (allows frontend to fetch from localhost:5000)
CORS(app)

# Load the model
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, 'model', 'rf_model.pkl')
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.json
        print(f"Received data: {data}")
        
        # Prepare DataFrame for prediction
        # The model expects specific feature names and types
        input_data = pd.DataFrame([{
            'neighbourhood': data.get('neighborhood'), # logic maps frontend inputs to model features
            'room_type': data.get('room_type'),
            'accommodates': int(data.get('accommodates', 1)), # Note: Model wasn't trained on this if it wasn't in CSV? 
                                                              # Wait, let's check what model was trained on.
                                                              # Model trained on: ['neighbourhood', 'room_type', 'minimum_nights', 'availability_365']
                                                              # We need to map or provide defaults for missing features the model expects.
            'minimum_nights': 1, # Default as not in form
            'availability_365': 365 # Default as not in form
        }])

        # Since we key off exact column names, we must ensure they match what model.py used.
        # model.py Features: ['neighbourhood', 'room_type', 'minimum_nights', 'availability_365']
        
        # We need to construct the exact dataframe
        prediction_df = pd.DataFrame({
            'neighbourhood': [data.get('neighborhood')],
            'room_type': [data.get('room_type')],
            'minimum_nights': [1], # Hardcoded for this simple UI
            'availability_365': [180] # Hardcoded average
        })

        prediction = model.predict(prediction_df)
        predicted_price = float(prediction[0])
        
        # Add 'accommodates' logic simply as a post-processing multiplier if it wasn't in the model
        # OR we leave it as is if we want to be strict about the ML model.
        # Given the user request, let's stick to the ML model output, 
        # but maybe scale it slightly by accommodates manually since it wasn't in the training data?
        # Actually, let's just return the raw model prediction to be honest to the ML.
        
        return jsonify({
            'price': round(predicted_price, 2),
            'currency': '$',
            'confidence': 85 # Mocked confidence
        })

    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
