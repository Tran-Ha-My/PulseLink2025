from cnn_model import CNN_Model

import paho.mqtt.client as mqtt

BROKER = "localhost"
client = mqtt.Client()
client.connect(BROKER, 1883)  # use 1883 for TCP MQTT

# initiate
model = CNN_Model()

# train and save to history to use the accuracy % value to dipslay to UI 
history = model.train_cnn_model()
accuracy = history.history['val_accuracy'][-1]
print("CNN validation accuracy:", accuracy)


# publish to frontend topic
client.publish("cnn_accuracy", str(accuracy * 100))  # send in %

# predict
prediction = model.predict("/Users/tranhamy/Documents/pulselink/PulseLink2025/backend/spectrograms1")

# Import necessary modules and packages
from cnn_model import CNN_Model
import paho.mqtt.client as mqtt

# MQTT broker settings
BROKER = "localhost"
client = mqtt.Client()
client.connect(BROKER, 1883)  # Use port 1883 for TCP MQTT

# Initialize the CNN model
model = CNN_Model()

# Train the model and retrieve accuracy for UI display
history = model.train_cnn_model()
accuracy = history.history['val_accuracy'][-1]
print("CNN validation accuracy:", accuracy)

# Publish validation accuracy to frontend topic (in percent)
client.publish("cnn_accuracy", str(accuracy * 100))

# Predict using the trained model
prediction = model.predict("pulselink/PulseLink2025/frontend/src/python_scripts/spectrograms1")