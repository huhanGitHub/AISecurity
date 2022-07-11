"""
Written by Yujin Huang(Jinx)
Started 22/03/2021 11:11 am
Last Editted 

Description of the purpose of the code
"""

import tensorflow as tf
import csv
import numpy
import sys
import time
import os
from tqdm import tqdm

numpy.set_printoptions(threshold=sys.maxsize)

start_time = time.time()

# the csv file for recording
csv_file = "/Users/hhuu0025/Downloads/adversarialAttack/models/model_info.csv"
f = open(csv_file, "a", newline='')
writer = csv.DictWriter(
    f, fieldnames=["index", "layer", "shape", "data_type"])
writer.writeheader()

row_writer = csv.writer(f)

model = "gender_nn"
model_path = r'/Users/hhuu0025/Downloads/adversarialAttack/models/gender_nn.tflite'
interpreter = tf.lite.Interpreter(model_path)
interpreter.allocate_tensors()
details = interpreter.get_tensor_details()

for detail in tqdm(details):
    row_writer.writerow(
        [detail['index'], detail['name'], detail['shape'], detail['dtype']])

    parameter = interpreter.get_tensor(detail['index'])

    save_dir = r'/Users/hhuu0025/Downloads/adversarialAttack/models/' + model
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    file = open(save_dir + "/" + str(detail['index']) + "_para.txt", "w+")
    file.write(str(parameter))
    file.close()

end_time = time.time()

print("extraction time:", end_time - start_time)
