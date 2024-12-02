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
        """
            Clase que permite crear un modelo y entenarlo

            Argumentos:
                dataSet: datos que se usaran para entrenar
                destino: donde se guardara el modelo
                tipo: tipo de modelo que creeara la clase

            Retorna
        """
        ##Se inicialozan las varuiables de entrenamiento
        self.dataSet = dataSet
        ##ajustar estos valores
        self.image_size = (128, 128)
        self.img_height, self.img_width = 128, 128
        self.image_size = (128, 128)
        #self.batch_size = 128
        self.batch_size = 64
        self.epochs = 50
        ## esto sirve para el optimizapr
        self.learning_rate = 0.001  # Ajusta este valor según sea necesario
        ##esto es por lo de guardar
        fecha = datetime.now()
        fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
        self.modelName =  destino + "E=" + str(self.epochs) + "_B=" + str(self.batch_size) + "_Lr=" + str(self.learning_rate) + fecha + "_" + tipo
        self.modelName =  destino + "Modelo_" + tipo + "_" + fecha
        self.class_name = self.modelName + ".json"
        self.guardarClases()
        self.crearDataGen()
        self.crearTrainGenerator()
        self.crearValidationGenerator()
        #self.imprimirDatosDeGeneradores()
        if tipo.lower() == "cnn":
            self.crearCNN()
        elif tipo.lower() == "fcn":
            self.crearFCN()
        elif tipo.lower() == "cnntensorflow":
            self.crearTensor()            
        elif tipo.lower() == "cnnalexnet":
            self.crearCNNAlex()
        elif tipo.lower() == "cnnvgg":
            self.crearVGGtinny()                                    
        #self.model.summary()
        self.crearOptimizer()
        self.compilarmodelo()
        self.tiempoinicial = datetime.now()
        self.entrenar()
        self.tiempofinal = datetime.now()
        self.diferencia = self.tiempofinal - self.tiempoinicial
        print(f'Delta Time: {self.diferencia.total_seconds()/60} minutes')
        self.salvarmodelo()
        #self.verDatos()
        
    #def verDatos(self):
    #     acc = self.history.history['accuracy']
    #     val_acc = self.history.history['val_accuracy']
    #     loss = self.history.history['loss']
    #     val_loss = self.history.history['val_loss']
    #     epochs_range = range(self.epochs)
    #     plt.figure(figsize=(12, 6))
    #     plt.subplot(1, 2, 1)
    #     plt.plot(epochs_range, acc, label='Training Accuracy')
    #     plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    #     plt.legend(loc='lower right')
    #     plt.title('Training and Validation Accuracy')
    #     plt.subplot(1, 2, 2)
    #     plt.plot(epochs_range, loss, label='Training Loss')
    #     plt.plot(epochs_range, val_loss, label='Validation Loss')
    #     plt.legend(loc='upper right')
    #     plt.title('Training and Validation Loss')
    #     plt.savefig(self.modelName + ".png")
    #     plt.show()

    def salvarmodelo(self): 
        """
            Funcion que permite guardar el modelo generado y entrenado
        """ 
        self.model.save(self.modelName+".h5" )
        print("Model training complete and saved as 'custom_image_classifier_model.h5'")              

    def entrenar(self):
        """
            Funcion que usa compile del objeto modelo para generar el modelo entrenado
        """        
        self.history = self.model.fit(
            self.trainGeneratoro,
            steps_per_epoch=self.trainGeneratoro.samples // self.batch_size,
            validation_steps=self.validationGenerator.samples // self.batch_size,
            epochs=self.epochs,
            validation_data=self.validationGenerator
        )
        #history = model.fit(
        #    trainGeneratoro,
        #    validation_data=validationGenerator,
        #    epochs=epochs
        #)

    def compilarmodelo(self):
        """
            Funcion que usa compile del objeto modelo para construir el onjeto
        """
        self.model.compile(optimizer=self.optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    def crearOptimizer(self):
        """
            Funcion que usa Adam para crear el objeto optimizer
        """
        self.optimizer = Adam(learning_rate=self.learning_rate)

    def crearCNN(self):
        """
            Funcion que usa Sequential para crear un modelo de tipo CNN
        """
        self.model = Sequential([
            #Conv2D(32, (3, 3), activation='relu', input_shape=(*self.image_size, 3)),
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
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

    def crearTensor(self):
        """
            Funcion que usa Sequential para crear un modelo de tipo CNN basado en los ejemplos de tensorflow
        """
        self.model = Sequential([
            #Conv2D(32, (3, 3), activation='relu', input_shape=(*self.image_size, 3)),
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            Flatten(),
            Dense(64, activation='relu'),
            Dense(len(self.classes))
        ])               

    def crearCNNAlex(self):
        """
        Función que usa Sequential para crear un modelo de tipo CNN basado en AlexNet.
        """
        self.model = Sequential([
            # Primera capa 
            Conv2D(96, (11, 11), strides=(4, 4), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
            MaxPooling2D((3, 3), strides=(2, 2)),

            # Segunda capa 
            Conv2D(256, (5, 5), activation='relu', padding='same'),
            MaxPooling2D((3, 3), strides=(2, 2)),

            # Tercera, cuarta y quinta capas convolucionales
            Conv2D(384, (3, 3), activation='relu', padding='same'),
            Conv2D(384, (3, 3), activation='relu', padding='same'),
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            MaxPooling2D((3, 3), strides=(2, 2)),

            # Aplanado y capas densas completamente conectadas
            Flatten(),
            Dense(4096, activation='relu'),
            Dropout(0.5),
            Dense(4096, activation='relu'),
            Dropout(0.5),
            Dense(len(self.classes), activation='softmax')
        ])

    def crearVGG(self):
        """
        Función que usa Sequential para crear un modelo de tipo CNN basado en VGG
        """
        self.model = Sequential([
            # Bloque 1
            Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(self.img_height, self.img_width, 3)),
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            MaxPooling2D((2, 2), strides=(2, 2)),

            # Bloque 2
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            MaxPooling2D((2, 2), strides=(2, 2)),

            # Bloque 3
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            MaxPooling2D((2, 2), strides=(2, 2)),

            # Bloque 4
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            MaxPooling2D((2, 2), strides=(2, 2)),

            # Bloque 5
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            MaxPooling2D((2, 2), strides=(2, 2)),

            # Clasificación
            Flatten(),
            Dense(4096, activation='relu'),
            Dropout(0.5),
            Dense(4096, activation='relu'),
            Dropout(0.5),
            Dense(len(self.classes), activation='softmax')
        ])

    def crearVGGtinny(self):
        """
        Función que usa Sequential para crear un modelo de tipo CNN basado en VGG
        """

        self.model = Sequential([
            # Bloque 1
            Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(self.img_height, self.img_width, 3)),
            MaxPooling2D((2, 2), strides=(2, 2)),

            # Bloque 2
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            MaxPooling2D((2, 2), strides=(2, 2)),

            # Bloque 3
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            MaxPooling2D((2, 2), strides=(2, 2)),

            # Bloque 4
            #Conv2D(256, (3, 3), activation='relu', padding='same'),
            #MaxPooling2D((2, 2), strides=(2, 2)),


            # Clasificación
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(len(self.classes), activation='softmax')
        ])




    def crearFCN(self):
        """
            Funcion que usa Sequential para crear un modelo de tipo Fcn
        """        
        self.model = Sequential([
            Flatten(input_shape=(self.img_height, self.img_width, 3)),
            Dense(512, activation='relu'),
            Dropout(0.5),  # Para evitar overfitting
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(128, activation='relu'),
            Dense(self.trainGeneratoro.num_classes, activation='softmax')
        ])        


    # def crearCNN(self):
    #     self.model = models.Sequential([
    #         layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
    #         layers.MaxPooling2D((2, 2)),
    #         layers.Conv2D(64, (3, 3), activation='relu'),
    #         layers.MaxPooling2D((2, 2)),
    #         layers.Conv2D(128, (3, 3), activation='relu'),
    #         layers.MaxPooling2D((2, 2)),
    #         layers.Flatten(),
    #         layers.Dense(128, activation='relu'),
    #         layers.Dense(self.trainGeneratoro.num_classes, activation='softmax')  # Número de clases igual al número de carpetas
    #     ])



    # def imprimirDatosDeGeneradores(self):
    #     print("Number of images per class in the training set:")
    #     for self.class_name, class_index in self.trainGeneratoro.class_indices.items():
    #         num_images = np.sum(self.trainGeneratoro.classes == class_index)
    #         print(f"{self.class_name}: {num_images}")

    #     print("\nNumber of images per class in the validation set:")
    #     for self.class_name, class_index in self.validationGenerator.class_indices.items():
    #         num_images = np.sum(self.validationGenerator.classes == class_index)
    #         print(f"{self.class_name}: {num_images}")        

    def crearValidationGenerator(self):   
        """
            Funcion que usa flow_from_directory del objeto datagen para crear el objeto traingenerator
        """
        self.validationGenerator = self.datagen.flow_from_directory(
            self.dataSet,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation'
        )
    def crearTrainGenerator(self):
        """
            Funcion que usa flow_from_directory del objeto datagen para crear el objeto traingenerator
        """
        self.trainGeneratoro = self.datagen.flow_from_directory(
            self.dataSet,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training'
        )      
    
    def crearDataGen(self):
        """
            Funcion que usa ImageDataGenerator para crear el objeto datagen
        """
        self.datagen = ImageDataGenerator(
            rescale=1.0/255.0, 
            validation_split=0.2
        )

    def guardarClases(self):
        """
            Funcion que permite guardar la lista de clases encontradas en el data set como un archivo json
        """
        self.classes = [d for d in os.listdir(self.dataSet) if os.path.isdir(os.path.join(self.dataSet, d))]
        self.classes.sort()
        class_indices = {cls: idx for idx, cls in enumerate(self.classes)}
        # Guardar clases en un archivo JSON
        with open(self.class_name, 'w') as f:
            json.dump(class_indices, f)
