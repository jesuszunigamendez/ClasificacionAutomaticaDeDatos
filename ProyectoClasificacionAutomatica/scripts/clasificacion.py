import tkinter as tk
from tkinter import filedialog
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
import cv2
import os
from openpyxl import load_workbook
import platform
import re


class Clasificar:
    def __init__(self,*,rutaModelo,rutaArchivo,rutaDataSetClasificar,rutaResultado,ancho,alto):
        self.rutaModelo = rutaModelo
        self.model = tf.keras.models.load_model(self.rutaModelo)
        self.rutaArchivo = rutaArchivo
        self.rutaDataSetClasificar = rutaDataSetClasificar
        self.archivosClasificar = [f for f in os.listdir(self.rutaDataSetClasificar) if f.endswith('.png')]
        self.rutaResultado = rutaResultado
        self.rutaClases = self.obtenerRutaClases()
        self.indices = self.obtenerIndices()
        self.arrayClasificar = []
        self.clasificar()
        rutaGuardada = self.guardarExcel()
        self.abrirExcel(rutaGuardada)

    def abrirExcel(self,ruta):
        # Abrir el archivo en el sistema operativo
        if platform.system() == "Windows":
            os.startfile(ruta)  # En Windows
        elif platform.system() == "Darwin":
            os.system(f"open {ruta}")  # En macOS
        else:
            os.system(f"xdg-open {ruta}")  # En Linux

    def guardarExcel(self):
        # Obtener el nombre del archivo original sin la ruta completa
        nombreArchivo = os.path.basename(self.rutaArchivo)
        # Crear el nuevo nombre con el prefijo
        nombreGuardar = f"Resultados_Para_{nombreArchivo}"
        # Combinar la nueva ruta y el nuevo nombre
        rutaGuardado = os.path.join(self.rutaResultado, nombreGuardar)

        # Cargar el archivo Excel
        workbook = load_workbook(self.rutaArchivo)

        # Seleccionar la hoja activa (o especificar la hoja por nombre)
        hoja = workbook.active

        # Obtener el número actual de columnas
        num_columnas = hoja.max_column

        # Agregar encabezados en la primera fila de las nuevas columnas
        hoja.cell(row=1, column=num_columnas + 1, value="Resultado")
        hoja.cell(row=1, column=num_columnas + 2, value="Certeza %")

        # Recorrer las filas desde la segunda para agregar los datos
        contadorFila = 1
        for fila in hoja.iter_rows(min_row=2, max_col=num_columnas + 2):  # max_col para recorrer las nuevas columnas
            contadorFila = contadorFila + 1
            for arreglo in self.arrayClasificar:
                if contadorFila == int(arreglo[0]):
                    resultado = arreglo[1]
                    confianza = round((float(arreglo[2]) * 100) , 2)
                    break
            # Penúltima columna (nueva columna añadida)
            fila[num_columnas].value = str(resultado)
    
            # Última columna (nueva columna añadida)
            fila[num_columnas + 1].value = str(confianza)

        # Guardar los cambios en la nueva ubicación con el nuevo nombre
        workbook.save(rutaGuardado)

        print(f"Se guardó el archivo modificado como: {rutaGuardado}")
        return rutaGuardado






    # Función para clasificar la imagen
    def classify_image(self,model, img_path, class_indices):
        # Obtén la forma de entrada del modelo
        input_shape = model.input_shape[1:3]  # Esto es (img_shape, img_shape)
        img = self.load_and_prep_image(img_path, input_shape[0])
        prediction = model.predict(img)
        if class_indices:
            class_names = list(class_indices.keys())
            predicted_class = class_names[np.argmax(prediction)]
            confidence = np.max(prediction)
            return predicted_class, confidence
        else:
            return None, None
        
    # Función para cargar y preprocesar la imagen
    def load_and_prep_image(self, filename, img_shape):
        img = image.load_img(filename, target_size=(img_shape, img_shape))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        return img        
        
    def clasificar(self):
        for imagen in self.archivosClasificar:
            buscar = re.search(r"_(\d+)\.png$", imagen)
            if buscar:
                numero = buscar.group(1)  # Obtener el número como texto
                rutaImagen = self.rutaDataSetClasificar + "/" + imagen
                prediccion, confianza = self.classify_image(self.model, rutaImagen, self.indices)
                if prediccion is not None and confianza is not None:
                    self.arrayClasificar.append([numero,prediccion,confianza])
                else:
                    self.arrayClasificar.append([numero,"Fail","0"])
            else:
                print("Error al procesar la firma " + imagen)
            

        
    def clasificarMetdo2(self,ruta_imagen,img_height,img_width):
        img = cv2.imread(ruta_imagen)
        img = cv2.resize(img, (img_height, img_width))
        img = img / 255.0  # Normalizar como en el entrenamiento
        img = np.expand_dims(img, axis=0)  # Añadir dimensión para batch
        # Realizar predicción
        prediccion = self.model.predict(img)
        clase_predicha = np.argmax(prediccion)  # Índice de la categoría más probable
        etiqueta_predicha = self.train_generator.class_indices.keys()  # Obtener nombres de categorías
        ########################################################
        return list(etiqueta_predicha)[clase_predicha]        
    

    def obtenerIndices(self):
        indices = None
        try:
            with open(self.rutaClases, 'r') as f:
                indices = json.load(f)
                return indices
        except FileNotFoundError:
            return None
        
    def obtenerRutaClases(self):
        partes = self.rutaModelo.split("/")
        ruta = ""
        for parte in partes:
            if parte.endswith(".h5"):
                nombre = parte[:-2]
                ruta = ruta + nombre + "json"
            else:
                ruta = ruta + parte + "/"
        return ruta


# # Función para predecir la categoría de una imagen nueva
# def predecir_categoria(ruta_imagen):
#     img = cv2.imread(ruta_imagen)
#     img = cv2.resize(img, (img_height, img_width))
#     img = img / 255.0  # Normalizar como en el entrenamiento
#     img = np.expand_dims(img, axis=0)  # Añadir dimensión para batch

#     # Realizar predicción
#     prediccion = model.predict(img)
#     clase_predicha = np.argmax(prediccion)  # Índice de la categoría más probable
#     etiqueta_predicha = train_generator.class_indices.keys()  # Obtener nombres de categorías
    
#     return list(etiqueta_predicha)[clase_predicha]


# # Ejemplo de uso
# ruta_imagen_nueva = 'ruta/a/tu/imagen.jpg'  # Cambia esto a la ruta de una imagen de prueba
# categoria = predecir_categoria(ruta_imagen_nueva)
# print("La categoría de la imagen es:", categoria)



# Función para cargar el modelo
# def load_model():
#     root = tk.Tk()
#     root.withdraw()
#     file_path = filedialog.askopenfilename(title='Seleccionar archivo del modelo', filetypes=[('Modelo HDF5', '*.h5')])
#     print(file_path)
#     if file_path:
#         model = tf.keras.models.load_model(file_path)
#         print(model)
#         return model, file_path
#     else:
#         return None, None 







# print("aqui")
# # Cargar el modelo
# model, model_path = load_model()

# Verificar si se cargó correctamente el modelo
# if model is None:
#     print('No se seleccionó ningún modelo. Por favor, selecciona un archivo de modelo HDF5 (.h5).')
# else:
    # Intentar cargar los índices de las clases desde un archivo JSON asociado al modelo
    #    class_indices = None
    # partes = model_path.split("/")
    # ruta = ""
    # for parte in partes:
    #     if parte.endswith(".h5"):
    #         ruta = ruta + "class_indices.json"
    #     else:
    #         ruta = ruta + parte + "/"
    # print(model_path)
    # print(ruta)            
    # json_path = ruta
    # try:
    #     with open(json_path, 'r') as f:
    #         class_indices = json.load(f)
    #         print('Índices de las clases cargados desde JSON.')
    # except FileNotFoundError:
    #     print('No se encontró el archivo de índices de las clases JSON asociado al modelo.')

    # Clasificar una nueva imagen seleccionada por el usuario
    # while True:
    #     root = tk.Tk()
    #     root.withdraw()
    #     img_path = filedialog.askopenfilename(title='Seleccionar imagen para clasificar')
    #     print(img_path)
    #     if img_path:
    #         predicted_class, confidence = classify_image(model, img_path, class_indices)
    #         if predicted_class is not None and confidence is not None:
    #             print(f'La imagen fue clasificada como: {predicted_class} con una confianza de: {confidence:.2f}')
    #         else:
    #             print('No se pudo realizar la clasificación debido a un problema con class_indices.')
    #     else:
    #         print('No se seleccionó ninguna imagen para clasificar.')
    #         break
