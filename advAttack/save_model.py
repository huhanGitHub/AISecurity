"""
Written by Yujin Huang(Jinx)
Started 20/03/2021 2:31 am
Last Editted 

Description of the purpose of the code
"""
import tensorflow as tf
import numpy as np

model = tf.keras.applications.MobileNetV2()

# tf.saved_model.save(model, 'mobilenetv2_1')
model.save('mv2')

# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model('mv2') # path to the SavedModel directory
tflite_model = converter.convert()

# Save the model.
with open('mv2.tflite', 'wb') as f:
  f.write(tflite_model)

