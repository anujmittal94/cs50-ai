import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import random
import matplotlib.pyplot as plt

IMG_WIDTH = 30
IMG_HEIGHT = 30
data_dir = "gtsrb"

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python tester.py model images")

    model_loc = sys.argv[1]
    test_images = sys.argv[2]

    category_images = dict()
    with os.scandir(data_dir) as categories:
        for category in categories:
            image_loc = random.choice(os.listdir(category.path))
            image_array = cv2.resize(cv2.imread(os.path.join(category.path, image_loc)), (IMG_WIDTH, IMG_HEIGHT))
            category_images[category.name] = image_array

    model = tf.keras.models.load_model(model_loc)


    with os.scandir(test_images) as images:
        for image in images:
            image_array = np.array([cv2.resize(cv2.imread(image.path), (IMG_WIDTH, IMG_HEIGHT))])
            fig, axs = plt.subplots(1, 2, sharey=True)
            axs[0].imshow(image_array[0][...,::-1])
            axs[0].set_title("Image")
            category = str(model.predict_classes(image_array)[0])
            axs[1].imshow(category_images[category][...,::-1])
            axs[1].set_title("Category " + category)
            plt.show()

if __name__ == "__main__":
    main()
