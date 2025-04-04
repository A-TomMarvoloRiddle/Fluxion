import matplotlib.pyplot as plt
import csv
from datetime import datetime
import numpy as np
from sklearn import kernel_approximation
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
#from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.layers import LSTM, Dense, Input
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Step 1: Fetch data and preprocess it
ip = []  # input
op = []  # output

with open("RNN_dataset_test_and_split.csv", 'r') as file:
    csvf = csv.reader(file)
    next(csvf)  # Skip header if present
    for lines in csvf:
        ip.append(lines[0:2])  # Assuming first column is day, second is time
        op.append(lines[-1])  # Assuming last column is the target (green time)

# Initialize lists for date, month, year, hour, minute, and day
numeric_day = []  # Numeric day of the month
weekday_name = []  # Name of the day
hour = []
minute = []

# Step 2: Extract date and time components
for entry in ip:
    # Parse date and time
    date_time_str = f"{entry[0]} {entry[1]}"  # Combine date and time
    try:
        date_time_obj = datetime.strptime(date_time_str, '%A %H:%M')
    except ValueError:
        print("Value Error")
        date_time_obj = datetime.strptime(date_time_str, '%A %H:%M')

    # Append extracted features to respective lists
    numeric_day.append(date_time_obj.day)  # Numeric day
    weekday_name.append(date_time_obj.strftime('%A'))  # Name of the day
    hour.append(date_time_obj.hour)
    minute.append(date_time_obj.minute)

# Map weekday names to numeric values
weekday_mapping = {
    'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
    'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7
}
numeric_weekday = [weekday_mapping[day] for day in weekday_name]
#what is the use of using numeric_weekday in place of weekday_name

# Step 3: Prepare dataset
input_features = np.array([numeric_weekday, hour, minute], dtype=np.float32).T
output_target = np.array(op, dtype=np.float32).reshape(-1, 1)

# Correctly scale the input features and output target
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

input_features = scaler_x.fit_transform(input_features)
output_target = scaler_y.fit_transform(output_target)

# Training and testing dataset
X = input_features.reshape(input_features.shape[0], 1, input_features.shape[1])
y = output_target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model
input_shape = (X_train.shape[1], X_train.shape[2])
# Step 4: Build the LSTM model
model = Sequential([
    Input(shape=input_shape), #input layer
    LSTM(1, return_sequences=True,dropout=0.2), # LSTM layer with 1 unit
    LSTM(4, return_sequences=True,dropout=0.2), # LSTM layer with 4 units
    LSTM(8, return_sequences=True,dropout=0.2), # LSTM layer with 8 units
    LSTM(16, return_sequences=True,dropout=0.2), # LSTM layer with 16 units
    LSTM(32, return_sequences=True,dropout=0.2), # LSTM layer with 32 units
    LSTM(64, return_sequences=True,dropout=0.2), # LSTM layer with 64 units
    LSTM(128, return_sequences=True,dropout=0.2), # LSTM layer with 128 units
    LSTM(256, return_sequences=True,dropout=0.2), # LSTM layer with 256 units
    LSTM(512, return_sequences=True,dropout=0.2), # LSTM layer with 512 units kernel_regularizer=l2(0.01)
    Dense(1) #output layer
])

# Step 5: Build and train the model
model.compile(optimizer='adam', loss='mse')

reduce_lr = ReduceLROnPlateau(monitor='val_loss', 
                               factor=0.2,  # Reduce learning rate by 80%
                               patience=10,  # Wait 5 epochs before reducing
                               min_lr=0.00001)


early_stopping = EarlyStopping(
    monitor='val_loss',  # Monitor validation loss
    patience=10,         # Number of epochs with no improvement
    restore_best_weights=True  # Restore model weights from the epoch with best value of the monitored quantity
)
history=model.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_test, y_test), verbose=1)
#callbacks=[early_stopping,reduce_lr]
# Step 6: Evaluate the model
#loss = model.evaluate(X_test, y_test, verbose=0)
#print(f"Test Loss: {loss}")
predictions = model.predict(X_test)
#print(X_test)
predictions = scaler_y.inverse_transform(predictions.reshape(-1, 1))
#print(predictions)
# Step 7: Make predictions
# Predict for a new input
new_day = "Monday"
new_time = "14:05"

# Parse new input
try:
    new_dt_obj = datetime.strptime(f"{new_day} {new_time}", '%A %H:%M')
except ValueError:
    new_dt_obj = datetime.strptime(f"{new_day} {new_time}", '%A %H:%M')

numeric_day = new_dt_obj.day  # Numeric day of the month
numeric_weekday = weekday_mapping[new_dt_obj.strftime('%A')]  # Map weekday name to number

# Create new input feature
new_input = [[numeric_weekday, new_dt_obj.hour, new_dt_obj.minute]]
new_input_scaled = scaler_x.transform(new_input)
new_input_reshaped = new_input_scaled.reshape(1, 1, 3)

# Extract loss values
train_loss = history.history['loss']
val_loss = history.history['val_loss']
plt.figure(figsize=(10, 6))
plt.plot(train_loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Loss Curves')
plt.legend()
plt.grid(True)
plt.show()

# Predict the green time
predicted_green_time = model.predict(new_input_reshaped)
predicted_green_time=predicted_green_time.reshape(-1,1)
predicted_green_time = scaler_y.inverse_transform(predicted_green_time)
print(f"Predicted Green Time for {new_day} {new_time}: {predicted_green_time[0][0]}")
model.save('model1.h5')