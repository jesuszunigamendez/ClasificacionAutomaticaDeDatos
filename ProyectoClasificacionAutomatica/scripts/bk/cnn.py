import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import numpy as np
import cv2

# Definir ruta del dataset y otros parámetros
data_dir = 'ruta/a/tu/directorio'  # Cambia esto a la ruta donde están tus carpetas de categorías
img_height, img_width = 128, 128  # Tamaño al que redimensionaremos las imágenes
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
model.save('modelo_clasificacion.h5')

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
