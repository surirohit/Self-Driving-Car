#!/usr/bin/env python

import os
import cv2
from os import listdir
from os.path import isfile, join
import numpy as np

def main():

    paths = ['forward','left','right','forward-left','forward-right']
    image_array = np.zeros((1, 38400))
    label_array = np.zeros((1, 5), 'float')
    labels = np.zeros((5, 5) , 'float')
    for i in range(5):
        labels[i][i] = 1
    print "Collecting images"
    for i in range(len(paths)):
        path = 'training_images/'+paths[i]+'/'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        print path,'-',len(files),'images'
        for f in files:
            img = cv2.imread(path+f,0)
            temp = img.reshape(1,38400).astype(np.float32)
            image_array = np.vstack((image_array, temp))
            label_array = np.vstack((label_array, labels[i]))

    train = image_array[1:, :]
    train_labels = label_array[1:, :]
    print train.shape
    print train_labels.shape

    e1 = cv2.getTickCount()

    # create MLP
    layer_sizes = np.int32([38400, 32, 5])
    model = cv2.ml.ANN_MLP_create()
    model.setLayerSizes(layer_sizes)

    model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP)
    model.setBackpropMomentumScale(0.0)
    model.setBackpropWeightScale(0.001)
    model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001))
    model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)

    print 'Training MLP ...'
    model.train(np.float32(train), cv2.ml.ROW_SAMPLE, np.float32(train_labels))
    # set end time
    e2 = cv2.getTickCount()
    time = (e2 - e1)/cv2.getTickFrequency()
    print 'Training duration:', time

    # save param
    model.save('mlp_xml/mlp.xml')

    #model = cv2.ml.ANN_MLP_load('mlp_xml/mlp.xml')

    ret, resp = model.predict(train)
    prediction = resp.argmax(-1)
    print 'Prediction:', prediction
    true_labels = train_labels.argmax(-1)
    print 'True labels:', true_labels

    print 'Testing...'
    train_rate = np.mean(prediction == true_labels)
    print 'Train rate: %f:' % (train_rate*100)

    
if __name__ == '__main__':
    main()
