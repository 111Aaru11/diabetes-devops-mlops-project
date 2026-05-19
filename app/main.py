from flask import Flask, render_template, request, jsonify

import torch
import torch.nn as nn

import numpy as np
import os
import joblib
import time

# ===================================
# PROMETHEUS IMPORTS
# ===================================

from prometheus_client import Counter
from prometheus_client import Histogram
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST


# ===================================
# CREATE FLASK APP
# ===================================

app = Flask(__name__)


# ===================================
# PROMETHEUS METRICS
# ===================================

# Total prediction requests

PREDICTION_COUNTER = Counter(
    "prediction_requests_total",
    "Total number of prediction requests"
)

# Diabetic predictions

DIABETIC_COUNTER = Counter(
    "diabetic_predictions_total",
    "Total diabetic predictions"
)

# Non-diabetic predictions

NON_DIABETIC_COUNTER = Counter(
    "non_diabetic_predictions_total",
    "Total non-diabetic predictions"
)

# Prediction response time

REQUEST_TIME = Histogram(
    "prediction_request_duration_seconds",
    "Time spent processing prediction requests"
)


# ===================================
# FIXED PATHS FOR DOCKER
# ===================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "model",
    "diabetes_model.pth"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "..",
    "model",
    "scaler.pkl"
)

print("Current Working Directory:", os.getcwd())
print("MODEL_PATH:", MODEL_PATH)
print("SCALER_PATH:", SCALER_PATH)


# ===================================
# LOAD SCALER
# ===================================

scaler = joblib.load(SCALER_PATH)


# ===================================
# DEFINE ANN MODEL
# ===================================

class DiabetesANN(nn.Module):

    def __init__(self):

        super(DiabetesANN, self).__init__()

        self.network = nn.Sequential(

            nn.Linear(8, 32),
            nn.ReLU(),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 8),
            nn.ReLU(),

            nn.Linear(8, 1)

        )

    def forward(self, x):

        return self.network(x)


# ===================================
# LOAD TRAINED MODEL
# ===================================

model = DiabetesANN()

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=torch.device("cpu")
    )
)

model.eval()


# ===================================
# HOME PAGE
# ===================================

@app.route("/")

def home():

    return render_template("index.html")


# ===================================
# METRICS ENDPOINT
# ===================================

@app.route("/metrics")

def metrics():

    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


# ===================================
# PREDICTION API
# ===================================

@app.route("/predict", methods=["POST"])

def predict():

    # Start timer

    start_time = time.time()

    try:

        # Count request

        PREDICTION_COUNTER.inc()

        data = request.get_json()

        pregnancies = float(data["pregnancies"])

        glucose = float(data["glucose"])

        blood_pressure = float(data["blood_pressure"])

        skin_thickness = float(data["skin_thickness"])

        insulin = float(data["insulin"])

        bmi = float(data["bmi"])

        pedigree = float(data["pedigree"])

        age = float(data["age"])

        input_data = np.array([[
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            pedigree,
            age
        ]])

        # ===================================
        # SCALE INPUT DATA
        # ===================================

        input_scaled = scaler.transform(input_data)

        input_tensor = torch.tensor(
            input_scaled,
            dtype=torch.float32
        )

        # ===================================
        # MODEL PREDICTION
        # ===================================

        with torch.no_grad():

            output = model(input_tensor)

            probability = torch.sigmoid(output).item()

        # ===================================
        # RESULT LOGIC
        # ===================================

        if probability >= 0.5:

            prediction = "DIABETIC"

            confidence = probability

            # Increment diabetic counter

            DIABETIC_COUNTER.inc()

        else:

            prediction = "NON-DIABETIC"

            confidence = 1 - probability

            # Increment non-diabetic counter

            NON_DIABETIC_COUNTER.inc()

        # ===================================
        # TRACK RESPONSE TIME
        # ===================================

        REQUEST_TIME.observe(
            time.time() - start_time
        )

        # ===================================
        # RETURN RESPONSE
        # ===================================

        return jsonify({

            "prediction": prediction,

            "confidence": f"{confidence:.4f}"

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        })


# ===================================
# RUN FLASK APP
# ===================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

    
# from flask import Flask, render_template, request, jsonify

# import torch
# import torch.nn as nn

# import numpy as np
# import os
# import joblib


# # ===================================
# # CREATE FLASK APP
# # ===================================

# app = Flask(__name__)


# # ===================================
# # FIXED PATHS FOR DOCKER
# # ===================================

# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "diabetes_model.pth")
# SCALER_PATH = os.path.join(BASE_DIR, "..", "model", "scaler.pkl")

# print("Current Working Directory:", os.getcwd())
# print("MODEL_PATH:", MODEL_PATH)
# print("SCALER_PATH:", SCALER_PATH)

# # scaler = joblib.load(SCALER_PATH)

# #webhook test
# # ===================================
# # LOAD SCALER
# # ===================================

# scaler = joblib.load(SCALER_PATH)


# # ===================================
# # DEFINE ANN MODEL
# # ===================================

# class DiabetesANN(nn.Module):

#     def __init__(self):

#         super(DiabetesANN, self).__init__()

#         self.network = nn.Sequential(

#             nn.Linear(8, 32),
#             nn.ReLU(),

#             nn.Linear(32, 16),
#             nn.ReLU(),

#             nn.Linear(16, 8),
#             nn.ReLU(),

#             nn.Linear(8, 1)

#         )

#     def forward(self, x):

#         return self.network(x)


# # ===================================
# # LOAD TRAINED MODEL
# # ===================================

# model = DiabetesANN()

# model.load_state_dict(
#     torch.load(
#         MODEL_PATH,
#         map_location=torch.device("cpu")
#     )
# )

# model.eval()


# # ===================================
# # HOME PAGE
# # ===================================

# @app.route("/")

# def home():

#     return render_template("index.html")


# # ===================================
# # PREDICTION API
# # ===================================

# @app.route("/predict", methods=["POST"])

# def predict():

#     try:

#         data = request.get_json()

#         pregnancies = float(data["pregnancies"])

#         glucose = float(data["glucose"])

#         blood_pressure = float(data["blood_pressure"])

#         skin_thickness = float(data["skin_thickness"])

#         insulin = float(data["insulin"])

#         bmi = float(data["bmi"])

#         pedigree = float(data["pedigree"])

#         age = float(data["age"])

#         input_data = np.array([[
#             pregnancies,
#             glucose,
#             blood_pressure,
#             skin_thickness,
#             insulin,
#             bmi,
#             pedigree,
#             age
#         ]])

#         # SCALE DATA

#         input_scaled = scaler.transform(input_data)

#         input_tensor = torch.tensor(
#             input_scaled,
#             dtype=torch.float32
#         )

#         # MODEL PREDICTION

#         with torch.no_grad():

#             output = model(input_tensor)

#             probability = torch.sigmoid(output).item()

#         if probability >= 0.5:

#             prediction = "DIABETIC"

#             confidence = probability

#         else:

#             prediction = "NON-DIABETIC"

#             confidence = 1 - probability

#         return jsonify({

#             "prediction": prediction,

#             "confidence": f"{confidence:.4f}"

#         })

#     except Exception as e:

#         return jsonify({

#             "error": str(e)

#         })


# # ===================================
# # RUN FLASK APP
# # ===================================

# if __name__ == "__main__":

#     app.run(
#         host="0.0.0.0",
#         port=5000,
#         debug=True
#     )


