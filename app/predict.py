import torch
import torch.nn as nn
import numpy as np
import joblib



scaler = joblib.load("model/scaler.pkl")


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



model = DiabetesANN()

model.load_state_dict(
    torch.load("model/diabetes_model.pth")
)

model.eval()


print("\n===== DIABETES PREDICTION SYSTEM =====\n")

pregnancies = float(input("Enter Pregnancies: "))

glucose = float(input("Enter Glucose Level: "))

blood_pressure = float(input("Enter Blood Pressure: "))

skin_thickness = float(input("Enter Skin Thickness: "))

insulin = float(input("Enter Insulin Level: "))

bmi = float(input("Enter BMI: "))

diabetes_pedigree = float(
    input("Enter Diabetes Pedigree Function: ")
)

age = float(input("Enter Age: "))



input_data = np.array([
    [
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        diabetes_pedigree,
        age
    ]
])



input_scaled = scaler.transform(input_data)

input_tensor = torch.tensor(
    input_scaled,
    dtype=torch.float32
)



with torch.no_grad():

    output = model(input_tensor)

    probability = torch.sigmoid(output).item()



print("\n===== RESULT =====")

if probability >= 0.5:

    print("Prediction: DIABETIC")

    print(f"Confidence: {probability:.4f}")

else:

    print("Prediction: NON-DIABETIC")

    print(f"Confidence: {1 - probability:.4f}")