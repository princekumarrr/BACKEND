from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(_name_)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Restrict CORS to your frontend

# Define an upload folder path
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    # Check file type
    if not file.filename.endswith('.csv'):
        return 'Invalid file type. Only CSV files are allowed.', 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return f"Error reading CSV file: {e}", 500

    matching_indices = []
    for i in range(0, len(df) - 3):
        if df.iloc[i, 0] == df.iloc[i + 1, 0] == df.iloc[i + 2, 0] == df.iloc[i + 3, 0]:
            matching_indices.append(i)

    chart_data = [{"index": i, "value": v} for i, v in enumerate(df.iloc[:, 0])]

    # Optional: Clean up the file after processing
    os.remove(file_path)

    return jsonify({
        'chartData': chart_data,
        'matchingIndices': matching_indices
    })

