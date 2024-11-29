from tkinter import filedialog
import openpyxl
import os
import tkinter as tk
import time
import sys
from datetime import datetime


def seleccionarArchivo(nombre,extension):
    """"
        Esta funcion permite ontener un archivo usando el dialogo del sistema
        Argumentos:
            nombre: Nombre de los archovos a seleccionar
            extension: extensiones permitidas
        Retorna:
            String con el archivo seleccionado o None en caso de no seleccionar ninguno
    """
    os.chdir(os.getcwd())
    root = tk.Tk()
    root.withdraw()
    root.focus_force()
    file = filedialog.askopenfilename(title='Seleccionar archivo fuente', filetypes=[(nombre, extension)])
    if file:
        return file
    else:
        return None
    
def obtenerColumna(archivo,tabs="",excluir=False):
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
            if excluir:
                print(tabs,0,". No excluir ninguna",)
            while True:
                seleccion = input(tabs)
                try:
                    a = int(seleccion)
                    if a > 0 and a < contador:
                        contador2 = 1
                        for celda in fila:
                            if contador2 == a:
                                return [contador2,celda]
                            contador2 = contador2 + 1
                    elif a == 0 and excluir:
                        return [0,"SinCeldaExcluida"]
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
        #se imprime el menu        
        print()
        print("Seleccione una opcion")
        print(tabMenu,"1 . Generar Firmas")
        print(tabMenu,"2 . Entrenar modelo")
        print(tabMenu,"3 . Clasificar Datos")
        print(tabMenu,"4 . Evaluar Resultados")
        print(tabMenu,"0 . Salir")
        print()
        seleccion = input()
        try:
            # se verifica que lo ingresado sea numerico y que este en el rango
            a = int(seleccion)
            if a < 0 and a >4:
                a = 1 / 0
            else:
                menu1 = a
            # if else que corrobora cada opcion
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
                    anchoImagen = 0#obtenerDimension("Ancho",tabs=tabMenu)
                    altoImagen = 0#obtenerDimension("Alto",tabs=tabMenu)
                    while True:
                        carpetaDestino = os.path.dirname(archivoOrigen) + "/" + "Firmas_Fuente_" + str(datetime.now().strftime("%d_%m_%y_%H_%M_%S"))
                        #print(tabMenu,"Utilice el dialogo del sistema para seleccionar la carpeta donde se guardaran las firmas")
                        #carpetaDestino = obtenerDirectorio()
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
                    firmas = generarFirmasGraficas.codificarExcel(origen=archivoOrigen,destino=carpetaDestino,columnaClasificadora=columnaClasificadora[0],ancho=anchoImagen,alto=altoImagen)                                                        
                    #print("Las firmas se generan con los siguienbtes datos: ")
                    #print("Archivo fuente: ",archivoOrigen)
                    #print("Celda clasificadora:", columnaClasificadora[1])
                    #if anchoImagen == 0:
                    #    print("Ancho de las firmas: Dinamico")
                    #else:
                    #    print("Ancho de las firmas ",anchoImagen)
                    #if altoImagen == 0:
                    #    print("Alto de las firmas: Dinamico")
                    #else:
                    #    print("Alto de las firmas ",altoImagen)                 
                    #carpetaDestino = carpetaDestino + "/"   
                    #print("Carpeta destino",carpetaDestino)
                    #print()
                    #seleccion = input("Presione enter para generar las firmas o digite 0 para salir sin generar")
                    #if seleccion != "0":
                    #    firmas = generarFirmasGraficas.codificarExcel(origen=archivoOrigen,destino=carpetaDestino,columnaClasificadora=columnaClasificadora[0],ancho=anchoImagen,alto=altoImagen)
                    
            #opcion dos del menu                        
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
                    destino = os.path.dirname(origen)
                    #print(tabMenu,"Utilice el dialogo del sistema para seleccionar la carpeta donde se guardara el modelo")
                    #destino = obtenerDirectorio()
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
                    #print(origen)
                    #print(destino)
                    while True:
                        try:
                            print(tabMenu,"Seleccione el tipo de modelo a entrenar")
                            print(tabMenu,"1. Red neuronal convolucional CNN")
                            print(tabMenu,"2. Red completamente conectada FCN")                          
                            print
                            seleccion = input()
                            a = int(seleccion)
                            if a == 1:
                                tipo = "CNN"
                                break
                            elif a == 2:
                                tipo = "FCN"
                                break
                            else:
                                a = 1/0
                        except Exception as e:
                            print("Seleccione una opcion correcta")
                    from scripts import entrenamiento
                    entrenamiento.Modelos(dataSet=origen,destino=destino,tipo=tipo)
                    print("terminado")
            #opcion 3 del menu
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
                        print(tabMenu,"Seleccione la columna a excluir")
                        columnaClasificadora = obtenerColumna(archivoClasificar,tabs=tabMenu,excluir=True)
                        break
                while flagMenuPrincipal == False:
                    destino = os.path.dirname(archivoClasificar)
                    #sys.exit()
                    #print(tabMenu,"Utilice el dialogo del sistema para seleccionar la carpeta donde se guardaran los resultados")
                    #destino = obtenerDirectorio()
                    if not destino:
                        print(tabMenu,"Debe seleccionar una carpeta para continuar o si desea volver al menu ingrese 0 (presione enter)")
                        a = input()
                        if a == "0":
                            flagMenuPrincipal = True
                            break
                    else:
                        break   
                if not flagMenuPrincipal:            
                    anchoImagen = 0#obtenerDimension("Ancho",tabs=tabMenu)
                    altoImagen = 0#obtenerDimension("Alto",tabs=tabMenu)                                          
                if not flagMenuPrincipal:
                    from scripts import clasificacion
                    from scripts import generarFirmasGraficas
                    firmas = generarFirmasGraficas.codificarExcel(origen=archivoClasificar,destino=destino,columnaClasificadora=columnaClasificadora[0],ancho=anchoImagen,alto=altoImagen, modo="clasificar")
                    rutaDataSet = firmas.carpetaDestinoPrincipal + firmas.carpetaDestinoSecundaria
                    clasificar = clasificacion.Clasificar(rutaModelo=rutaModelo,rutaArchivo=archivoClasificar,rutaDataSetClasificar=rutaDataSet,rutaResultado=destino,ancho=anchoImagen,alto=altoImagen)
            elif menu1 == 4:
                tabMenu = "         "            
                flagMenuPrincipal = False
                while flagMenuPrincipal == False:
                    print(tabMenu,"Utilice el dialogo del sistema para seleccionar el archivo a evaluar")
                    archivoEvaluar = seleccionarArchivo("Excel","*.xlsx")
                    if not archivoEvaluar:
                        print(tabMenu,"Debe seleccionar un archivo para continuar o si desea volver al menu ingrese 0 (presione enter)")
                        a = input()
                        if a == "0":
                            flagMenuPrincipal = True
                            break
                    else:
                        print(tabMenu,"Seleccione la columna que contiene las etiquetas verdaderas.")
                        verdaderas = obtenerColumna(archivoEvaluar,tabs=tabMenu)
                        print(tabMenu,"Seleccione la columna que contiene las etiquetas predichas.")
                        predichas = obtenerColumna(archivoEvaluar,tabs=tabMenu)                        
                        from scripts import evaluar
                        evaluacion = evaluar.evaluar(rutaArchivo=archivoEvaluar,columnaVerdadera=verdaderas,columnaPredicha=predichas)
                        break
            elif menu1 == 0:
                break                    
        except Exception as e:
            print(e)
            print("Seleccione una opcion correcta")
        


    