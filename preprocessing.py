import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
IMAGE_SIZE = 224 #input size to network

def test_input(x):
    x = cv2.imread(x, cv2.IMREAD_COLOR)
    x = cv2.resize(x, (IMAGE_SIZE, IMAGE_SIZE))
    x = x/255.0
    x = np.expand_dims(x, axis=0)
    return x
	
def create_mask(pred_mask):
    pred_mask = np.argmax(pred_mask, axis=-1) 
    pred_mask = np.expand_dims(pred_mask, axis=-1)
    return pred_mask
    
def show_predictions(prediction):
    pred_mask = create_mask(prediction)
    display_sample(pred_mask[0])

def display_sample(display_list):
    plt.figure(figsize=(4, 4))
    plt.imshow(tf.keras.preprocessing.image.array_to_img(display_list))
    plt.axis('off')
    plt.show()