import numpy as np
import pandas as pd
import librosa
import librosa.display
import glob as gb
import matplotlib.pyplot as plt
import gc
import os

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout,BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array


def initiate_cnn_model():
    classifier = Sequential()
    classifier.add(Conv2D(32, 
                        kernel_size = (3, 3), 
                        input_shape = (128, 128, 3), # (height, width, channels) | channels=3  mean its RGB colored
                        activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Conv2D(32, kernel_size = (3, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Dropout(0.5))
    classifier.add(Flatten())

    classifier.add(Dense(units = 128, activation = 'relu'))
    classifier.add(Dense(units = 8, activation = 'softmax'))    # categorical_crossentropy is the standard loss function for multi-class classification
    
    # If only had 2 classes (Normal vs Abnormal), use binary_crossentropy instead
    classifier.compile(optimizer='adam',loss="categorical_crossentropy",metrics=["accuracy"])

    return classifier

class CNN_Model:
    def __init__(self):
        self.cnn_model = initiate_cnn_model()
        self.training_predictions = []

    def train_cnn_model(self):

        ##### TO DO!!! ##########
        ##### RETRIEVE DATA FROM MONGODB (expect json that CAN gives the following dataframe)
        # patient_id (index)    | ID (spectrogram image)    | CLASS (patient_diagnosis)
        # ------------------------------------------------------------------------
        #                       |                           |
        #                       |                           |
        #                       |                           |
        #                       |                           |
        # this will be saved into patient_data_all

        # code adapted from https://github.com/architgajpal/respiratory_disease_classification

        patient_data=pd.read_csv('patient_diagnosis.csv',dtype=str) # might not be a csv file!!!!!
        # ASSUME THAT ALL PNG FILES ARE SAVED IN spectrograms and have patient id in file name
        # e.g. 101_1b1_Al_sc_Meditron.png -> 101 is patient id
        spectograms_dir_loc=np.array(gb.glob("spectrograms1/*.png")) # array of file names
        patient_data_all = pd.DataFrame(columns=['ID','CLASS'])        
        
        
        index = 0
        for image in spectograms_dir_loc[index:]:
            image_name = os.path.basename(image)
            patient_id = image_name.split('_')[0]
            
            # Check that patient_id exists in patient_data
            if patient_id in patient_data['ID'].values:
                patient_condition = patient_data.loc[patient_data['ID'] == patient_id, 'CLASS'].values[0]
                patient_data_all.loc[len(patient_data_all)] = [image_name, patient_condition]


        from sklearn.model_selection import train_test_split
        trainset_df, testset_df = train_test_split(patient_data_all, test_size=0.2)
        

        train_datagen = ImageDataGenerator(rescale = 1./255, # normalise pixel values from [0, 255] to [0,1]
                                        validation_split=0.25) # 25% of data is used to validate
        test_datagen = ImageDataGenerator(rescale = 1./255)

        training_set = train_datagen.flow_from_dataframe(
            dataframe=trainset_df,
            directory="spectrograms1/", # path to root of folder that contains all images TBC!!!!
            x_col="ID",
            y_col="CLASS",
            subset="training", # select the training portion
            batch_size=32, # loads 32 images each time -> good on memory
            seed=42, # randomization seed
            shuffle=True,
            class_mode="categorical",
            target_size=(128,128)) # resize image to 128 x 128

        validation_set = train_datagen.flow_from_dataframe(
            dataframe=trainset_df,
            directory="spectrograms1/", # path to root of folder that contains all images TBC!!!!
            x_col="ID",
            y_col="CLASS",
            subset="validation", # select the validation portion (25% as set above)
            batch_size=32,
            seed=42,
            shuffle=True,
            class_mode="categorical",
            target_size=(128,128))

        test_set = test_datagen.flow_from_dataframe(
            dataframe=testset_df,
            directory="spectrograms1/", # path to root of folder that contains all images TBC!!!!
            x_col="ID",
            y_col="None",
            batch_size=32,
            seed=42,
            shuffle=False,
            class_mode=None,
            target_size=(128,128))

        step_train_size=training_set.n//training_set.batch_size
        step_valid_size=validation_set.n//validation_set.batch_size

        # Model action

        history = self.cnn_model.fit(x=training_set,
                            steps_per_epoch=step_train_size,
                            validation_data=validation_set,
                            validation_steps=step_valid_size,
                            epochs=20)   # training_set already knows which col to use for x_col and y_col

        self.cnn_model.evaluate(validation_set, steps=step_valid_size)

        step_test_size = test_set.n // test_set.batch_size
        predicted_conditions = self.cnn_model.predict(test_set, steps=step_test_size, verbose=1)

        predicted_class_indices=np.argmax(predicted_conditions,axis=1)

        labels = (training_set.class_indices)
        labels = dict((v,k) for k,v in labels.items())
        self.training_predictions = [labels[k] for k in predicted_class_indices]
        print(self.training_predictions[0:10])
        print(testset_df.head(10))

        return history

    # function takes a file path to a single image or a folder
    def predict(self, path):
        import os
        results = {}
        if os.path.isdir(path):
            for fname in os.listdir(path):
                if fname.endswith(".png"):
                    full_path = os.path.join(path, fname)
                    results[fname] = self._predict_single(full_path)
            return results
        else:
            return self._predict_single(path)

    # internal helper to predict a single image
    def _predict_single(self, file_path):
        img = load_img(file_path, target_size=(128, 128))
        arr = np.expand_dims(img_to_array(img), axis=0)
        return self.cnn_model.predict(arr)