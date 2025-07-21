import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

# STEP 1: Load CSV file
df = pd.read_csv("nifty50.csv")  # Must contain a 'Close' column
if "Close" not in df.columns:
    raise ValueError("CSV must contain a 'Close' column.")

# STEP 2: Preprocess data
data = df[["Close"]]
data.dropna(inplace=True)

dataset = data.values
training_data_len = int(len(dataset) * 0.8)

# Scale data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# STEP 3: Create training dataset
train_data = scaled_data[0:training_data_len, :]
x_train, y_train = [], []

for i in range(60, len(train_data)):
    x_train.append(train_data[i - 60 : i, 0])
    y_train.append(train_data[i, 0])

x_train = np.array(x_train)
y_train = np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# STEP 4: Build LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(x_train, y_train, batch_size=1, epochs=1)

# STEP 5: Test the model
test_data = scaled_data[training_data_len - 60 :, :]
x_test = []
y_test = dataset[training_data_len:, :]

for i in range(60, len(test_data)):
    x_test.append(test_data[i - 60 : i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# STEP 6: Plot the results
train = data[:training_data_len]
valid = data[training_data_len:]
valid["Predictions"] = predictions

print("\n\n🔮 Predicted Closing Price for Next Day")
print(f"Predicted Price: ₹{valid['Predictions'].values[-1]:.2f}")

plt.figure(figsize=(14, 6))
plt.title("NIFTY 50 Stock Price Prediction")
plt.xlabel("Days")
plt.ylabel("Close Price INR")
plt.plot(train["Close"])
plt.plot(valid[["Close", "Predictions"]])
plt.legend(["Train", "Actual", "Predicted"])
plt.show()
