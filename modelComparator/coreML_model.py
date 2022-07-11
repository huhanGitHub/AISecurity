import tensorflow as tf
import coremltools as ct

tf_keras_model = tf.keras.Sequential(
    [
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax),
    ]
)

# Pass in `tf.keras.Model` to the Unified Conversion API
mlmodel = ct.convert(tf_keras_model, convert_to="mlprogram")

# or save the keras model in SavedModel directory format and then convert
tf_keras_model.save('tf_keras_model')
mlmodel = ct.convert('tf_keras_model', convert_to="mlprogram")

# or load the model from a SavedModel and then convert
tf_keras_model = tf.keras.models.load_model('tf_keras_model')
mlmodel = ct.convert(tf_keras_model, convert_to="mlprogram")

# or save the keras model in HDF5 format and then convert
tf_keras_model.save('tf_keras_model.h5')
mlmodel = ct.convert('tf_keras_model.h5', convert_to="mlprogram")
mlmodel.save('tf_keras_model.mlpackage')