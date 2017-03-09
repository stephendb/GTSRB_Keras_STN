import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
from sklearn.utils import shuffle
from floyd import dot

IMG_SIZE = 299
TRAIN_DIR = dot + "/input/GTSRB/Final_Training/"
TEST_DIR = dot + "/input/GTSRB/Final_Test/"

def preprocess_img(img):

    # # Histogram normalization in v channel
    # hsv = color.rgb2hsv(img)
    # hsv[:, :, 2] = exposure.equalize_hist(hsv[:, :, 2])
    # img = color.hsv2rgb(hsv)

    # central square crop
    min_side = min(img.shape[:-1])
    centre = img.shape[0]//2, img.shape[1]//2
    img = img[centre[0]-min_side//2:centre[0]+min_side//2,
              centre[1]-min_side//2:centre[1]+min_side//2,
              :]

    # rescale to standard size
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_CUBIC)
    return img

# def get_arrays(image_paths):
#     imgs = []
#     NUM_CLASSES = 43
#     for img_path in image_paths:
#         img = preprocess_img(cv2.imread(img_path))
#         imgs.append(img)
#     X = np.array(imgs, dtype='float32')
#     return X

def train_data(IMG_DIR=TRAIN_DIR):
    image_paths = []
    labels = []
    for root, dirs, files in os.walk(IMG_DIR):
        for f in files:
            if f.endswith(".ppm"):
                labels.append(int(root.split("/")[-1]))
                image_paths.append(os.path.join(root, f))

    print("{} image names.".format(len(image_paths)))
    print("{0} images labels with {1} unique labels".format(len(labels), len(set(labels))))
    paths, labels = shuffle(image_paths, labels)
    return paths, labels

def test_data(TEST_DIR=TEST_DIR):
    test = pd.read_csv(TEST_DIR + 'Images/GT-final_test.csv',sep=';')

    image_paths = []
    labels = []
    print("{} image names.".format(len(test['Filename'])))
    print("{0} images labels with {1} unique labels".format(len(test['ClassId']), len(set(test['ClassId']))))
    for file_name, class_id  in zip(list(test['Filename']), list(test['ClassId'])):
        image_paths.append(os.path.join(TEST_DIR + 'Images/',file_name))
        labels.append(class_id)

    image_paths, labels = shuffle(image_paths, labels)
    return image_paths, labels


def main():
    pass

    # train = train_data(TRAIN_DIR)
    # test = test_data(TEST_DIR)

    # with open(dot + "/output/train_incpt.pkl", "wb") as f_output:
    #     pickle.dump(train, f_output)
    #     print("Train output complete")
    # with open(dot + "/output/test_incpt.pkl", "wb") as f_output:
    #     pickle.dump(test, f_output)
    #     print("Test output complete")

    # f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    # ax1.imshow(train['features'][0])
    # ax1.set_title('Train' + train['labels'][0])
    # ax2.imshow(test['features'][0])
    # ax2.set_title('Test' + test['labels'][0])
    # plt.show()

if __name__ == "__main__":
    main()
