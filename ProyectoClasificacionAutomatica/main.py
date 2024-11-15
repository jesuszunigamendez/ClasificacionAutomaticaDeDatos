from tkinter import filedialog
import openpyxl
import os
import tkinter as tk
import time


def seleccionarArchivo(nombre,extension):
    """"
        Esta funcion permite ontener un archivo usando el dialogo del sistema
        Argumentos:
            nombre: Nombre de los archovos a seleccionar
            extension: extensiones permitidas
        Retorna:
            String con el archivo seleccionado o None en caso de no seleccionar ninguno
    """
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(title='Seleccionar archivo fuente', filetypes=[(nombre, extension)])
    if file:
        return file
    else:
        return None
    
def obtenerColumna(archivo,tabs=""):
    """"
        Funcion que permite obtener el nombre de la columna a clasificar
        Argumentos:
            archivo: Direccion del archivo a usar
            tabs: variable para controlar dise;o de impresiones
        Retorna:
            Arreglo con el valor de la celda y el nombre
    """
    if archivo:
        wb = openpyxl.load_workbook(archivo)
        hoja = wb.active
        for fila in hoja.iter_rows(values_only=True):
            contador = 1
            for celda in fila:
                print(tabs,contador,". ",celda)
                contador = contador + 1
            while True:
                seleccion = input(tabs)
                try:
                    a = int(seleccion)
                    if a > 0 and a <= contador:
                        contador = 1
                        for celda in fila:
                            if contador == a:
                                return [contador,celda]
                            contador = contador + 1
                    else:
                        a = 1 /0 
                except Exception as e:
                    print(tabs,"Debe seleccionar una opcion valida")

def obtenerDimension(nombre,tabs=""):
    """"
        Funcion que permite obtener un entero para una domensioon
        Argumentos:
            nombre: Nombre de la dimension
            tabs: variable para controlar dise;o de impresiones
        Retorna:
            Int con la dimension
    """
    while True:
        texto = tabs + "Digite el " + nombre + " de las firmas a generar o presione enter para que se genere dinamicamente "
        seleccion = input(texto)
        if seleccion:
            try:
                a = int(seleccion)
                if a > 0:
                    return a
                else:
                    a = 1 / 0
            except Exception as e:
                print(tabs,"Digite un valor numerico positivo")
        else:
            return 0

def obtenerDirectorio():
    """"
        Funcion que permite seleccionar un directorio
        Argumentos:
            nombre: Nombre de la dimension
            tabs: variable para controlar dise;o de impresiones
        Retorna:
            Int con la dimension
    """
    carpeta = filedialog.askdirectory(title="Selecciona una carpeta")
    if carpeta:
        return carpeta
    else:
        return None

if __name__ == "__main__":
    tabMenu = "     "
    while True:
        #if os.name == 'posix':
        #    os.system('clear')
        #elif os.name == 'nt':
        #    os.system('cls')
        tabMenu = " "            
        print()
        print("Seleccione una opcion")
        print(tabMenu,"1 . Generar Firmas")
        print(tabMenu,"2 . Entrenar modelo")
        print(tabMenu,"3 . Clasificar Datos")
        print(tabMenu,"0 . Salir")
        print()
        seleccion = input()
        try:
            a = int(seleccion)
            if a < 0 and a >3:
                a = 1 / 0
            else:
                menu1 = a
            if menu1 == 1:
                tabMenu = "         "            
                #variables necesarias para instanciar el objeto
                flagMenuPrincipal = False
                while True:
                    print(tabMenu,"Utilice el dialogo del sistema para seleccionar el archivo fuente")
                    archivoOrigen = seleccionarArchivo("Excel","*.xlsx")
                    if not archivoOrigen:
                        print(tabMenu,"Debe seleccionar un archivo para continuar o si desea volver al menu ingrese 0 (presione enter)")
                        a = input()
                        if a == "0":
                            flagMenuPrincipal = True
                            break
                    else:
                        break
                if not flagMenuPrincipal:            
                    print(tabMenu,"Seleccione la celda con la que se clasificaran las firmas.")
                    columnaClasificadora = obtenerColumna(archivoOrigen,tabs=tabMenu)
                    anchoImagen = obtenerDimension("Ancho",tabs=tabMenu)
                    altoImagen = obtenerDimension("Alto",tabs=tabMenu)
                    while True:
                        print(tabMenu,"Utilice el dialogo del sistema para seleccionar la carpeta donde se guardaran las firmas")
                        carpetaDestino = obtenerDirectorio()
                        if not carpetaDestino:
                            print(tabMenu,"Debe seleccionar una carpeta para continuar o si desea volver al menu ingrese 0 (presione enter)")
                            a = input()
                            if a == "0":
                                flagMenuPrincipal = True
                                break
                        else:
                            break                
                

                if not flagMenuPrincipal:
                    from scripts import generarFirmasGraficas
                                        

                    print("Las firmas se generan con los siguienbtes datos: ")
                    print("Archivo fuente: ",archivoOrigen)
                    print("Celda clasificadora:", columnaClasificadora[1])
                    if anchoImagen == 0:
                        print("Ancho de las firmas: Dinamico")
                    else:
                        print("Ancho de las firmas ",anchoImagen)
                    if altoImagen == 0:
                        print("Alto de las firmas: Dinamico")
                    else:
                        print("Alto de las firmas ",altoImagen)                 
                    carpetaDestino = carpetaDestino + "/"   
                    print("Carpeta destino",carpetaDestino)
                    print()
                    seleccion = input("Presione enter para generar las firmas o digite 0 para salir sin generar")
                    if seleccion != "0":
                        firmas = generarFirmasGraficas.codificarExcel(origen=archivoOrigen,destino=carpetaDestino,columnaClasificadora=columnaClasificadora[0],ancho=anchoImagen,alto=altoImagen)
            elif menu1 == 2:
                tabMenu = "         "            
                flagMenuPrincipal = False
                while True:
                    print(tabMenu,"Utilice el dialogo del sistema para seleccionar la carpeta donde se encuentra el set de datos")
                    origen = obtenerDirectorio()
                    if not origen:
                        print(tabMenu,"Debe seleccionar una carpeta para continuar o si desea volver al menu ingrese 0 (presione enter)")
                        a = input()
                        if a == "0":
                            flagMenuPrincipal = True
                            break
                    else:
                        break
                while flagMenuPrincipal == False:
                    print(tabMenu,"Utilice el dialogo del sistema para seleccionar la carpeta donde se guardara el modelo")
                    destino = obtenerDirectorio()
                    if not destino:
                        print(tabMenu,"Debe seleccionar una carpeta para continuar o si desea volver al menu ingrese 0 (presione enter)")
                        a = input()
                        if a == "0":
                            flagMenuPrincipal = True
                            break
                    else:
                        break  
                if flagMenuPrincipal == False:
                    origen = origen + "/"
                    destino = destino + "/"
                    tipo = ""
                    print(origen)
                    print(destino)
                    while True:
                        try:
                            print(tabMenu,"Seleccione el tipo de modelo a entrenar")
                            print(tabMenu,"1. original")
                            print(tabMenu,"2. cnn")
                            print(tabMenu,"3. dnn")                            
                            print
                            seleccion = input()
                            a = int(seleccion)
                            if a == 1:
                                tipo = "original"
                                break
                            elif a == 2:
                                tipo = "cnn"
                                break
                            elif a == 3:
                                tipo = "dnn"
                                break
                            else:
                                a = 1/0
                        except Exception as e:
                            print("Seleccione una opcion correcta")
                    from scripts import entrenamiento
                    entrenamiento.Modelos(dataSet=origen,destino=destino,tipo=tipo)
                    print("terminado")
            elif menu1 == 3:
                tabMenu = "         "            
                flagMenuPrincipal = False
                while True:
                    print(tabMenu,"Utilice el dialogo del sistema para seleccionar el modelo a utilizar")
                    rutaModelo = seleccionarArchivo("Modelo HDF5","*.h5")
                    if not rutaModelo:
                        print(tabMenu,"Debe seleccionar un archivo para continuar o si desea volver al menu ingrese 0 (presione enter)")
                        a = input()
                        if a == "0":
                            flagMenuPrincipal = True
                            break
                    else:
                        break

                while flagMenuPrincipal == False:
                    print(tabMenu,"Utilice el dialogo del sistema para seleccionar el archivo a clasificar")
                    archivoClasificar = seleccionarArchivo("Excel","*.xlsx")
                    if not archivoClasificar:
                        print(tabMenu,"Debe seleccionar un archivo para continuar o si desea volver al menu ingrese 0 (presione enter)")
                        a = input()
                        if a == "0":
                            flagMenuPrincipal = True
                            break
                    else:
                        break
                while flagMenuPrincipal == False:
                    print(tabMenu,"Utilice el dialogo del sistema para seleccionar la carpeta donde se guardaran los resultados")
                    destino = obtenerDirectorio()
                    if not destino:
                        print(tabMenu,"Debe seleccionar una carpeta para continuar o si desea volver al menu ingrese 0 (presione enter)")
                        a = input()
                        if a == "0":
                            flagMenuPrincipal = True
                            break
                    else:
                        break   
                if not flagMenuPrincipal:            
                    anchoImagen = obtenerDimension("Ancho",tabs=tabMenu)
                    altoImagen = obtenerDimension("Alto",tabs=tabMenu)                                          
                if not flagMenuPrincipal:
                    from scripts import clasificacion
                    from scripts import generarFirmasGraficas
                    destino = destino + "/"
                    firmas = generarFirmasGraficas.codificarExcel(origen=archivoClasificar,destino=destino,columnaClasificadora="",ancho=anchoImagen,alto=altoImagen, modo="clasificar")
                    rutaDataSet = destino + "FirmasTemporales"
                    clasificar = clasificacion.Clasificar(rutaModelo=rutaModelo,rutaArchivo=archivoClasificar,rutaDataSetClasificar=rutaDataSet,rutaResultado=destino,ancho=anchoImagen,alto=altoImagen)
            elif menu1 == 0:
                break                    
        except Exception as e:
            print(e)
            print("Seleccione una opcion correcta")
        


    