import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import numpy as np
import cv2

# Definir ruta del dataset y otros parámetros
data_dir = 'ruta/a/tu/directorio'  # Cambia esto a la ruta donde están tus carpetas de categorías
img_height, img_width = 128, 128
batch_size = 32
epochs = 10

# Generador de datos de entrenamiento y validación
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2
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

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=epochs
)

# Guardar el modelo entrenado
model.save('modelo_dnn_clasificacion.h5')

# Función para predecir la categoría de una imagen nueva
def predecir_categoria(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    img = cv2.resize(img, (img_height, img_width))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)  # Añadir dimensión para batch

    # Realizar predicción
    prediccion = model.predict(img)
    clase_predicha = np.argmax(prediccion)
    etiqueta_predicha = train_generator.class_indices.keys()
    
    return list(etiqueta_predicha)[clase_predicha]

# Ejemplo de uso
ruta_imagen_nueva = 'ruta/a/tu/imagen.jpg'
categoria = predecir_categoria(ruta_imagen_nueva)
print("La categoría de la imagen es:", categoria)
