from flask import Flask, request, render_template, jsonify
import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

app = Flask(__name__)

# File upload path
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to analyze image and extract coastal features
def analyze_image(image_path):
    image = Image.open(image_path)
    img_array = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 100, 200)
    
    # Coastline length estimation
    coastline_length = np.count_nonzero(edges)
    
    # Simulated values (you can integrate ML models)
    sea_level_rise = round(np.random.uniform(0.3, 1.5), 2)  # Placeholder
    erosion_area = round(np.random.uniform(10, 50), 2)  # Placeholder
    vegetation_loss = round(np.random.uniform(5, 20), 2)  # Placeholder

    return {
        "coastline_length": coastline_length,
        "sea_level_rise": sea_level_rise,
        "erosion_area": erosion_area,
        "vegetation_loss": vegetation_loss
    }

# Function to process CSV data
def analyze_csv(filepath):
    df = pd.read_csv(filepath)
    
    # Ensure required columns exist
    required_cols = ["Year", "Country", "Coastal length", "Sea level", "Land Impact"]
    if not all(col in df.columns for col in required_cols):
        return None

    df["Erosion Rate"] = df["Land Impact"] / df["Coastal length"]
    avg_erosion = df["Erosion Rate"].mean()
    avg_sea_level_rise = df["Sea level"].mean()

    return {
        "avg_erosion": round(avg_erosion, 2),
        "avg_sea_level_rise": round(avg_sea_level_rise, 2)
    }

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            if file.filename.endswith(".csv"):
                data = analyze_csv(filepath)
                return render_template("result.html", csv_data=data, img_data=None)

            elif file.filename.endswith((".jpg", ".png", ".jpeg")):
                data = analyze_image(filepath)
                return render_template("result.html", csv_data=None, img_data=data)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
