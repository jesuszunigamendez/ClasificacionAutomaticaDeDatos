import argparse


# Configurar el analizador de argumentos
parser = argparse.ArgumentParser(description="Argumentos que permiten ejecutar el programa")
# Agregar argumentos
parser.add_argument("--archivoEntrenamiento", type=str, required=True, default="",   help="Nombre del archivo que se va a procesar")
parser.add_argument("--columnaClasificadora", type=str, required=True, default="",   help="Columna que permitira la clasificacion de cada registro")
parser.add_argument("--anchoImagenes",        type=int,                default=0,    help="Ancho de la imagen a generar")  
parser.add_argument("--altoImagenes",         type=int,                default=0,    help="Alto de la imagen a generar")  
parser.add_argument("--listaCategorias",      type=str,                default="",   help="Lista de categorias, se compone de [[Columna1Categoria1,Columna2Categoria1,...],[[Columna1Categoria2,Columna2Categoria2,...],[.........]]")  
arguments = parser.parse_args()

archivoEntrenamiento = arguments.archivoEntrenamiento