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
import cv2



class AmbosModelos:
    def __init__(self,*,dataSet,destino):


# Definir ruta del dataset y otros parámetros
data_dir = 'ruta/a/tu/directorio'  # Cambia esto a la ruta donde están tus carpetas de categorías
img_height, img_width = 128, 128
batch_size = 32
epochs = 10

# Generador de datos de entrenamiento y validación
train_datagen = ImageDataGenerator(
    rescale=1.0/255,        # Normalizar los valores de los píxeles
    validation_split=0.2    # Dividir en 80% entrenamiento y 20% validación
)

train_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)


validation_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

###################################
#################################
# Definir el modelo DNN
model = models.Sequential([
    layers.Flatten(input_shape=(img_height, img_width, 3)),  # Aplanar la imagen
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),  # Para evitar overfitting
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dense(train_generator.num_classes, activation='softmax')
])

# Definir el modelo CNN
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(train_generator.num_classes, activation='softmax')  # Número de clases igual al número de carpetas
])

###################################
#################################


model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=epochs
)


###################################
#################################

# Guardar el modelo entrenado
model.save('modelo_dnn_clasificacion.h5')

# Guardar el modelo entrenado
model.save('modelo_clasificacion.h5')

###################################
#################################

# Función para predecir la categoría de una imagen nueva
def predecir_categoria(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    img = cv2.resize(img, (img_height, img_width))
    img = img / 255.0  # Normalizar como en el entrenamiento
    img = np.expand_dims(img, axis=0)  # Añadir dimensión para batch

    # Realizar predicción
    prediccion = model.predict(img)
    clase_predicha = np.argmax(prediccion)  # Índice de la categoría más probable
    etiqueta_predicha = train_generator.class_indices.keys()  # Obtener nombres de categorías
    
    return list(etiqueta_predicha)[clase_predicha]


# Ejemplo de uso
ruta_imagen_nueva = 'ruta/a/tu/imagen.jpg'  # Cambia esto a la ruta de una imagen de prueba
categoria = predecir_categoria(ruta_imagen_nueva)
print("La categoría de la imagen es:", categoria)















class ModeloCNN:
    def __init__(self,*,dataSet,destino):
        # Tiempo inicial\
        tiempo_inicial = datetime.now()
        self.dataSet = dataSet
        self.image_size = (224, 224)
        self.batch_size = 128
        self.epochs = 50
        self.learning_rate = 0.001  # Ajusta este valor según sea necesario
        self.modelName=  destino + "E=" + str(self.epochs) + "_B=" + str(self.batch_size) + "_Lr=" + str(self.learning_rate)
        self.class_name = destino + 'class_indices.json'
        # Recopilación de clases
        classes = [d for d in os.listdir(self.dataSet) if os.path.isdir(os.path.join(self.dataSet, d))]
        classes.sort()
        class_indices = {cls: idx for idx, cls in enumerate(classes)}
        # Guardar clases en un archivo JSON
        with open(self.class_name, 'w') as f:
            json.dump(class_indices, f)
        # Preprocesamiento de imágenes

        datagen = ImageDataGenerator(
            rescale=1.0/255.0, 
            validation_split=0.2
        )
        
        
        train_generator = datagen.flow_from_directory(
            self.dataSet,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training'
        )

        validation_generator = datagen.flow_from_directory(
            self.dataSet,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation'
        )

        # Imprimir el número de imágenes de cada clase
        print("Number of images per class in the training set:")
        for self.class_name, class_index in train_generator.class_indices.items():
            num_images = np.sum(train_generator.classes == class_index)
            print(f"{self.class_name}: {num_images}")

        print("\nNumber of images per class in the validation set:")
        for self.class_name, class_index in validation_generator.class_indices.items():
            num_images = np.sum(validation_generator.classes == class_index)
            print(f"{self.class_name}: {num_images}")

        # Crear el modelo desde cero
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(*self.image_size, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(len(classes), activation='softmax')
        ])

        # Crear el optimizador con la tasa de aprendizaje ajustada
        optimizer = Adam(learning_rate=self.learning_rate)

        # Compilar el modelo
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

        # Entrenar el modelo y guardar el historial
        history = model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // self.batch_size,
            validation_steps=validation_generator.samples // self.batch_size,
            epochs=self.epochs,
            validation_data=validation_generator
        )

        # Guardar el modelo
        model.save(self.modelName+".h5" )

        print("Model training complete and saved as 'custom_image_classifier_model.h5'")

        # Visualizar los resultados del entrenamiento
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

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
        # Tiempo final
        tiempo_final = datetime.now()

        # Calcular la diferencia
        diferencia = tiempo_final - tiempo_inicial

        # Imprimir la diferencia en segundos
        print(f'Delta Time: {diferencia.total_seconds()/60} minutes')

        plt.show()
