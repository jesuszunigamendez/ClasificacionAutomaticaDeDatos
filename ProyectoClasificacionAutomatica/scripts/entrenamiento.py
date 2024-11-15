import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

import tensorflow as tf
from tensorflow.keras import layers, models



class Modelos:
    def __init__(self,*,dataSet,destino,tipo):
        ##Se inicialozan las varuiables de entrenamiento
        self.dataSet = dataSet
        ##ajustar estos valores
        self.image_size = (128, 128)
        self.img_height, self.img_width = 128, 128
        self.batch_size = 128
        self.epochs = 50
        ## esto sirve para el optimizapr
        self.learning_rate = 0.001  # Ajusta este valor según sea necesario
        ##esto es por lo de guardar
        fecha = datetime.now()
        fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
        self.modelName =  destino + "E=" + str(self.epochs) + "_B=" + str(self.batch_size) + "_Lr=" + str(self.learning_rate) + fecha + "_" + tipo
        self.class_name = self.modelName + ".json"
        self.guardarClases()
        self.crearDataGen()
        self.crearTrainGenerator()
        self.crearValidationGenerator()
        self.imprimirDatosDeGeneradores()
        if tipo.lower() == "original":
            self.crearCNNOriginal()
        elif tipo.lower() == "cnn":
            self.crearCNN()
        elif tipo.lower() == "dnn":
            self.crearDNN()
        self.crearOptimizer()
        self.compilarmodelo()
        self.tiempoinicial = datetime.now()
        self.entrenar()
        self.tiempofinal = datetime.now()
        self.diferencia = self.tiempofinal - self.tiempoinicial
        print(f'Delta Time: {self.diferencia.total_seconds()/60} minutes')
        self.salvarmodelo()
        self.verDatos()

    def verDatos(self):
        acc = self.history.history['accuracy']
        val_acc = self.history.history['val_accuracy']
        loss = self.history.history['loss']
        val_loss = self.history.history['val_loss']
        epochs_range = range(self.epochs)
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label='Training Accuracy')
        plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.title('Training and Validation Accuracy')
        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label='Training Loss')
        plt.plot(epochs_range, val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.title('Training and Validation Loss')
        plt.savefig(self.modelName + ".png")
        plt.show()

    def salvarmodelo(self):  
        self.model.save(self.modelName+".h5" )
        print("Model training complete and saved as 'custom_image_classifier_model.h5'")              

    def entrenar(self):
        self.history = self.model.fit(
            self.train_generator,
            steps_per_epoch=self.train_generator.samples // self.batch_size,
            validation_steps=self.validation_generator.samples // self.batch_size,
            epochs=self.epochs,
            validation_data=self.validation_generator
        )
        #history = model.fit(
        #    train_generator,
        #    validation_data=validation_generator,
        #    epochs=epochs
        #)

    def compilarmodelo(self):
        self.model.compile(optimizer=self.optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    def crearOptimizer(self):
        self.optimizer = Adam(learning_rate=self.learning_rate)

    def crearCNNOriginal(self):
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(*self.image_size, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(len(self.classes), activation='softmax')
        ])        
    def crearCNN(self):
        self.model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(self.train_generator.num_classes, activation='softmax')  # Número de clases igual al número de carpetas
        ])        
    def crearDNN(self):
        self.model = models.Sequential([
            layers.Flatten(input_shape=(self.img_height, self.img_width, 3)),  # Aplanar la imagen
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),  # Para evitar overfitting
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.Dense(self.train_generator.num_classes, activation='softmax')
        ])        
    def imprimirDatosDeGeneradores(self):
        print("Number of images per class in the training set:")
        for self.class_name, class_index in self.train_generator.class_indices.items():
            num_images = np.sum(self.train_generator.classes == class_index)
            print(f"{self.class_name}: {num_images}")

        print("\nNumber of images per class in the validation set:")
        for self.class_name, class_index in self.validation_generator.class_indices.items():
            num_images = np.sum(self.validation_generator.classes == class_index)
            print(f"{self.class_name}: {num_images}")        

    def crearValidationGenerator(self):      
        self.validation_generator = self.datagen.flow_from_directory(
            self.dataSet,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation'
        )
    def crearTrainGenerator(self):
        self.train_generator = self.datagen.flow_from_directory(
            self.dataSet,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training'
        )      
    
    def crearDataGen(self):
        self.datagen = ImageDataGenerator(
            rescale=1.0/255.0, 
            validation_split=0.2
        )

    def guardarClases(self):
        self.classes = [d for d in os.listdir(self.dataSet) if os.path.isdir(os.path.join(self.dataSet, d))]
        self.classes.sort()
        class_indices = {cls: idx for idx, cls in enumerate(self.classes)}
        # Guardar clases en un archivo JSON
        with open(self.class_name, 'w') as f:
            json.dump(class_indices, f)
