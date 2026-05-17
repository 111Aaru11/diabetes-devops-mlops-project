from flask import Flask, render_template, request, jsonify

import torch
import torch.nn as nn

import numpy as np
import os
import joblib


# ===================================
# CREATE FLASK APP
# ===================================

app = Flask(__name__)


# ===================================
# FIXED PATHS FOR DOCKER
# ===================================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "diabetes_model.pth")
SCALER_PATH = os.path.join(BASE_DIR, "..", "model", "scaler.pkl")

print("Current Working Directory:", os.getcwd())
print("MODEL_PATH:", MODEL_PATH)
print("SCALER_PATH:", SCALER_PATH)

# scaler = joblib.load(SCALER_PATH)

#webhook test
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
# PREDICTION API
# ===================================

@app.route("/predict", methods=["POST"])

def predict():

    try:

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

        # SCALE DATA

        input_scaled = scaler.transform(input_data)

        input_tensor = torch.tensor(
            input_scaled,
            dtype=torch.float32
        )

        # MODEL PREDICTION

        with torch.no_grad():

            output = model(input_tensor)

            probability = torch.sigmoid(output).item()

        if probability >= 0.5:

            prediction = "DIABETIC"

            confidence = probability

        else:

            prediction = "NON-DIABETIC"

            confidence = 1 - probability

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
# # LOAD SCALER
# # ===================================

# scaler = joblib.load("model/scaler.pkl")


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
#         "model/diabetes_model.pth",
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





# # from flask import Flask, request, jsonify

# # import torch
# # import torch.nn as nn
# # import numpy as np
# # import joblib

# # # =========================
# # # LOAD FLASK APP
# # # =========================

# # app = Flask(__name__)

# # # =========================
# # # LOAD SCALER
# # # =========================

# # scaler = joblib.load("model/scaler.pkl")

# # # =========================
# # # DEFINE MODEL
# # # =========================

# # class DiabetesANN(nn.Module):

# #     def __init__(self):
# #         super(DiabetesANN, self).__init__()

# #         self.network = nn.Sequential(

# #             nn.Linear(8, 32),
# #             nn.ReLU(),

# #             nn.Linear(32, 16),
# #             nn.ReLU(),

# #             nn.Linear(16, 8),
# #             nn.ReLU(),

# #             nn.Linear(8, 1)

# #         )

# #     def forward(self, x):
# #         return self.network(x)

# # # =========================
# # # LOAD TRAINED MODEL
# # # =========================

# # model = DiabetesANN()

# # model.load_state_dict(
# #     torch.load("model/diabetes_model.pth")
# # )

# # model.eval()

# # # =========================
# # # HOME ROUTE
# # # =========================

# # @app.route("/")

# # def home():

# #     return "Diabetes Prediction API Running Successfully!"

# # # =========================
# # # PREDICTION ROUTE
# # # =========================

# # @app.route("/predict", methods=["POST"])

# # def predict():

# #     try:

# #         data = request.json

# #         input_data = np.array([
# #             [
# #                 data["Pregnancies"],
# #                 data["Glucose"],
# #                 data["BloodPressure"],
# #                 data["SkinThickness"],
# #                 data["Insulin"],
# #                 data["BMI"],
# #                 data["DiabetesPedigreeFunction"],
# #                 data["Age"]
# #             ]
# #         ])

# #         # Scale data

# #         input_scaled = scaler.transform(input_data)

# #         input_tensor = torch.tensor(
# #             input_scaled,
# #             dtype=torch.float32
# #         )

# #         # Prediction

# #         with torch.no_grad():

# #             output = model(input_tensor)

# #             probability = torch.sigmoid(output).item()

# #         prediction = (
# #             "DIABETIC"
# #             if probability >= 0.5
# #             else "NON-DIABETIC"
# #         )

# #         return jsonify({

# #             "prediction": prediction,

# #             "confidence": round(probability, 4)

# #         })

# #     except Exception as e:

# #         return jsonify({

# #             "error": str(e)

# #         })

# # # =========================
# # # RUN APP
# # # =========================

# # if __name__ == "__main__":

# #     app.run(
# #         host="0.0.0.0",
# #         port=5000,
# #         debug=True
# #     )