import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)



df = pd.read_csv("dataset/diabetes.csv")

print(df.head())



X = df.drop("Outcome", axis=1).values
y = df["Outcome"].values



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, "model/scaler.pkl")



X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)

y_train = torch.FloatTensor(y_train).reshape(-1, 1)
y_test = torch.FloatTensor(y_test).reshape(-1, 1)



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

# Create model
model = DiabetesANN()

print(model)



criterion = nn.BCEWithLogitsLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.0005
)


epochs = 300

losses = []

for epoch in range(epochs):

    # Forward pass
    outputs = model(X_train)

    loss = criterion(outputs, y_train)

    # Backward pass
    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    losses.append(loss.item())

    if (epoch + 1) % 20 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")



with torch.no_grad():

    predictions = torch.sigmoid(model(X_test))

    predicted = (predictions >= 0.5).float()

# Accuracy

accuracy = accuracy_score(
    y_test,
    predicted
)

print("\nAccuracy:", accuracy)



cm = confusion_matrix(
    y_test,
    predicted
)

print("\nConfusion Matrix:")
print(cm)

# Heatmap

plt.figure(figsize=(6, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
plt.savefig("confusion_matrix.png")
plt.close()

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predicted
    )
)



plt.figure(figsize=(8, 5))

plt.plot(losses)

plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.ylabel("Loss")
plt.show()

plt.savefig("loss_graph.png")
plt.close()


torch.save(
    model.state_dict(),
    "model/diabetes_model.pth"
)

print("\nModel saved successfully!")

print("Scaler saved successfully!")
# import pandas as pd
# import numpy as np
# import torch
# import torch.nn as nn
# import torch.optim as optim

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import (
#     accuracy_score,
#     confusion_matrix,
#     classification_report
# )

# import seaborn as sns
# import matplotlib.pyplot as plt
# import joblib



# df = pd.read_csv("dataset/diabetes.csv")

# print(df.head())



# X = df.drop("Outcome", axis=1).values
# y = df["Outcome"].values



# X_train, X_test, y_train, y_test = train_test_split(
#     X,
#     y,
#     test_size=0.2,
#     random_state=42
# )



# scaler = StandardScaler()

# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

# # Save scaler
# joblib.dump(scaler, "model/scaler.pkl")



# X_train = torch.FloatTensor(X_train)
# X_test = torch.FloatTensor(X_test)

# y_train = torch.FloatTensor(y_train).reshape(-1, 1)
# y_test = torch.FloatTensor(y_test).reshape(-1, 1)



# class DiabetesANN(nn.Module):

#     def __init__(self):
#         super(DiabetesANN, self).__init__()

#         self.network = nn.Sequential(
#             nn.Linear(8, 16),
#             nn.ReLU(),

#             nn.Linear(16, 8),
#             nn.ReLU(),

#             nn.Linear(8, 1),
#             nn.Sigmoid()
#         )

#     def forward(self, x):
#         return self.network(x)

# model = DiabetesANN()

# print(model)

# criterion = nn.BCELoss()

# optimizer = optim.Adam(
#     model.parameters(),
#     lr=0.0005
# )



# epochs = 200

# losses = []

# for epoch in range(epochs):

#     # Forward pass
#     outputs = model(X_train)

#     loss = criterion(outputs, y_train)

#     # Backward pass
#     optimizer.zero_grad()

#     loss.backward()

#     optimizer.step()

#     losses.append(loss.item())

#     if (epoch + 1) % 10 == 0:
#         print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")



# with torch.no_grad():

#     predictions = model(X_test)

#     predicted = (predictions >= 0.5).float()

# accuracy = accuracy_score(
#     y_test,
#     predicted
# )

# print("\nAccuracy:", accuracy)


# cm = confusion_matrix(
#     y_test,
#     predicted
# )

# print("\nConfusion Matrix:")
# print(cm)

# # Heatmap

# plt.figure(figsize=(6, 5))

# sns.heatmap(
#     cm,
#     annot=True,
#     fmt="d",
#     cmap="Blues"
# )

# plt.title("Confusion Matrix")
# plt.xlabel("Predicted")
# plt.ylabel("Actual")

# plt.show()




# print("\nClassification Report:\n")

# print(
#     classification_report(
#         y_test,
#         predicted
#     )
# )


# plt.figure(figsize=(8, 5))

# plt.plot(losses)

# plt.title("Training Loss")
# plt.xlabel("Epoch")
# plt.ylabel("Loss")

# plt.show()



# torch.save(
#     model.state_dict(),
#     "model/diabetes_model.pth"
# )

# print("\nModel saved successfully!")

# print("Scaler saved successfully!")












# # import pandas as pd
# # import numpy as np
# # import torch
# # import torch.nn as nn
# # import torch.optim as optim

# # from sklearn.model_selection import train_test_split
# # from sklearn.preprocessing import StandardScaler
# # from sklearn.metrics import accuracy_score

# # import joblib

# # data = pd.read_csv("../dataset/diabetes.csv")

# # print("Dataset Loaded Successfully")
# # print(data.head())



# # X = data.drop("Outcome", axis=1)
# # y = data["Outcome"]




# # scaler = StandardScaler()

# # X_scaled = scaler.fit_transform(X)

# # joblib.dump(scaler, "scaler.pkl")

# # print("Scaler Saved")




# # X_train, X_test, y_train, y_test = train_test_split(
# #     X_scaled,
# #     y,
# #     test_size=0.2,
# #     random_state=42
# # )




# # X_train = torch.tensor(X_train, dtype=torch.float32)
# # X_test = torch.tensor(X_test, dtype=torch.float32)

# # y_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
# # y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)




# # class DiabetesANN(nn.Module):

# #     def __init__(self):
# #         super(DiabetesANN, self).__init__()

# #         self.fc1 = nn.Linear(8, 16)
# #         self.relu1 = nn.ReLU()

# #         self.fc2 = nn.Linear(16, 8)
# #         self.relu2 = nn.ReLU()

# #         self.fc3 = nn.Linear(8, 1)

# #         self.sigmoid = nn.Sigmoid()

# #     def forward(self, x):

# #         x = self.fc1(x)
# #         x = self.relu1(x)

# #         x = self.fc2(x)
# #         x = self.relu2(x)

# #         x = self.fc3(x)

# #         x = self.sigmoid(x)

# #         return x


# # model = DiabetesANN()

# # print(model)



# # criterion = nn.BCELoss()

# # optimizer = optim.Adam(model.parameters(), lr=0.001)



# # epochs = 200

# # for epoch in range(epochs):

# #     outputs = model(X_train)

# #     loss = criterion(outputs, y_train)

# #     optimizer.zero_grad()

# #     loss.backward()

# #     optimizer.step()

# #     if (epoch + 1) % 10 == 0:
# #         print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")




# # with torch.no_grad():

# #     predictions = model(X_test)

# #     predicted = (predictions > 0.5).float()

# #     accuracy = accuracy_score(y_test, predicted)

# #     print(f"\nModel Accuracy: {accuracy * 100:.2f}%")



# # torch.save(model.state_dict(), "diabetes_model.pth")

# # print("Model Saved Successfully")