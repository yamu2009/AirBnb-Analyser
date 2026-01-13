# Airbnb Price Analyser

A styled PropTech single-page application (SPA) to predict Airbnb listing prices based on neighbourhood, room type, and other features.

## Project Structure

- **`/frontend`**: Contains the functionality for the user interface.
    - `index.html`: The main dashboard structure.
    - `style.css`: Modern styling with Airbnb-inspired aesthetics.
    - `script.js`: Sends usage data to the Flask API.
- **`/model`**: Contains the Machine Learning logic.
    - `clean_data.py`: Preprocesses the raw CSV data.
    - `model.py`: Trains a Random Forest Regressor and saves it as `rf_model.pkl`.
    - `rf_model.pkl`: The trained model file.
- **`app.py`**: A Flask API server that loads the model and serves predictions.
- **`/data`**: Stores the dataset.

## How to Run

### 1. Prerequisites
Ensure you have Python 3 installed.
Install dependencies:
```bash
pip install pandas numpy scikit-learn joblib flask flask-cors
```

### 2. Prepare the Model
If you haven't already, clean the data and train the model:
```bash
python3 model/clean_data.py
python3 model/model.py
```

### 3. Start the API Server
Run the Flask application:
```bash
python3 app.py
```
*The server will start at `http://127.0.0.1:5000`*

### 4. Launch the Frontend
Simply open `frontend/index.html` in your web browser. 
It will automatically connect to the local Flask server.

## API Specification

**POST /predict**

**Request Body:**
```json
{
    "neighborhood": "Downtown",
    "room_type": "Entire home/apt",
    "accommodates": 4
}
```

**Response:**
```json
{
    "price": 145.50,
    "currency": "$",
    "confidence": 85
}
```

## Model Details
- **Algorithm**: Random Forest Regressor
- **Features Used**: Neighbourhood, Room Type, Minimum Nights (Default: 1), Availability (Default: 180).
