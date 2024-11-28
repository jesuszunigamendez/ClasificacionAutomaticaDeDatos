import openpyxl
from PIL import Image
import os
import argparse
import sys
import shutil
from datetime import datetime

class codificarExcel:
    def __init__(self,*,origen,destino,columnaClasificadora,ancho,alto,modo="entrenar"):
        """
            Clase que permite codificar un archivo de excel en arreglos bidimensionales

            Argumentos:
                origen: Archivo fuente
                destino: Carpeta donde se guardaran
                columnaClasificadora: columna donde se tomaran las clases a clasificar
                ancho: ancho de las firmas en pixeles
                alto: alto de las firmas en pixeles
                modo: indica si las firmas son para entrenar o para clasificar

            Retorna:
        """
        self.archivoOrigen = origen
        corrida = datetime.now().strftime("%d_%m_%y_%H_%M_%S")
        self.carpetaDestinoPrincipal = destino + "/" + str(corrida) + "_"
        print("aquii")
        print(self.carpetaDestinoPrincipal)
        if os.path.exists(self.carpetaDestinoPrincipal):
            shutil.rmtree(self.carpetaDestinoPrincipal)
        self.elMayor = 0
        self.elMenor = 0
        self.anchoImagenes = ancho
        self.altoImagenes = alto
        self.columnaClasificadora = columnaClasificadora
        if modo == "entrenar":
            self.procesarArchivo()
        else:
            self.generarImagenesDeArchivo()
        print("Archivo procesado correctamente")



    def generarImagenesDeArchivo(self):
        """
            Funcion que procesa todo el archivo generando firmas aptas para clasificar
        """
        #  se abre e; excel
        wb = openpyxl.load_workbook(self.archivoOrigen)
        # se selecciona la primera hoja
        hoja = wb.active
        #se inicializan variables
        numeroFila = 0
        numeroCelda = 0
        CarpetaDestino = "FirmasTemporales"
        #self.columnaClasificadora = 10
        # for que recorre fila for fila
        for fila in hoja.iter_rows(values_only=True):
            numeroFila = numeroFila + 1            
            print("procesando fila ",numeroFila)            
            numeroCelda = 0
            arrayRGB = []
            arrayceldas = []
            # for que recorre celda por celda
            contadorCelda = 0
            for celda in fila:
                contadorCelda = contadorCelda + 1
                numeroCelda = numeroCelda + 1
                # si son las demas filas entonces se procesa cada celda como una linea de pixeles para la imagen 
                if (numeroFila != 1):# and (identificadorCelda != 0):
                    if numeroCelda == self.columnaClasificadora:
                        print("excluida",celda)
                    else:
                        #if numeroCelda == self.columnaClasificadora
                        # todo el valor de la celda se convierte en un arreglo de valores unicode convertidos a decimal
                        arrayceldas.append(celda)
                        unicodedec, unicodehex = self.cadenaADecimalHexadecimal(str(celda))
                        # para cada valor decimal en el arreglo equivalenter a la informacion de la celda se obtiene su equivalente en RGB
                        for dec in unicodedec:
                            arrayRGB.append(self.array_binarios_a_RGB(self.dividirBinarioenBytes(self.decialABinario24(dec))))
                            # se actualizan baderas de valores
                            #################################
                            if dec > self.elMayor:
                                self.elMayor = dec
                            if dec < self.elMenor:
                                self.elMenor = dec
                            #################################                        
                        # al terminar de convertir los caracteres a su equivalente unicode y de unicode a su equivalente RGB se agrega un identificador de fin de celda    
                        arrayRGB.append([256,256,256])

            if numeroFila != 1:
                # cuando se procesa toda una fila se guarda la imagen resultante en la carpeta correspondiente
                nombre = os.path.basename(self.archivoOrigen) + "_fila_" + str(numeroFila) + ".png"
                arrayRGBAjustado = self.ajustarColores(arrayRGB)
                self.guardarImagen(arrayRGBAjustado,CarpetaDestino,nombre)



    def procesarArchivo(self):
        """
            Funcion que procesa todo el archivo generando firmas aptas para entrenar
        """
        #  se abre e; excel
        wb = openpyxl.load_workbook(self.archivoOrigen)
        # se selecciona la primera hoja
        hoja = wb.active
        #se inicializan variables
        numeroFila = 0
        numeroCelda = 0
        identificadorCelda = 0
        CarpetaDestino = "failFolder"
        # for que recorre fila for fila
        for fila in hoja.iter_rows(values_only=True):
            numeroFila = numeroFila + 1            
            print("procesando fila ",numeroFila)            
            numeroCelda = 0
            arrayRGB = []
            arrayceldas = []
            # for que recorre celda por celda
            contadorCelda = 0
            for celda in fila:
                contadorCelda = contadorCelda + 1
                numeroCelda = numeroCelda + 1
                # si es la primera fila solo se identifica cual va a ser la columna que indica la carpeta organizadora
                if numeroFila == 1:
                    #if celda == self.columnaClasificadora:
                    if contadorCelda == self.columnaClasificadora:
                        identificadorCelda = numeroCelda
                # si son las demas filas entonces se procesa cada celda como una linea de pixeles para la imagen 
                elif (numeroFila != 1) and (identificadorCelda != 0):
                #if (numeroFila != 1) and (identificadorCelda != 0):
                    # si estamos sobre la celda que indica la carpeta destino entonces indicamos el nombre que traiga la celda como carpeta destino
                    if identificadorCelda == numeroCelda:
                        CarpetaDestino = str(celda)
                    # si es otra celda entonces tomamos su informacion y la codificamos a valores RGB                        
                    else:
                        # todo el valor de la celda se convierte en un arreglo de valores unicode convertidos a decimal
                        arrayceldas.append(celda)
                        unicodedec, unicodehex = self.cadenaADecimalHexadecimal(str(celda))
                        # para cada valor decimal en el arreglo equivalenter a la informacion de la celda se obtiene su equivalente en RGB
                        for dec in unicodedec:
                            #print("aqui")
                            #print(dec)
                            #print(self.decialABinario24(dec))
                            #print(self.dividirBinarioenBytes(self.decialABinario24(dec)))
                            #print(self.array_binarios_a_RGB(self.dividirBinarioenBytes(self.decialABinario24(dec))))
                            #if celda == None or celda == "None":
                                #arrayRGB.append([256,256,256])
                                #break
                            #else:
                            arrayRGB.append(self.array_binarios_a_RGB(self.dividirBinarioenBytes(self.decialABinario24(dec))))
                            #print("fin")
                            # se actualizan baderas de valores
                            #################################
                            if dec > self.elMayor:
                                self.elMayor = dec
                            if dec < self.elMenor:
                                self.elMenor = dec
                            #################################                        
                        # al terminar de convertir los caracteres a su equivalente unicode y de unicode a su equivalente RGB se agrega un identificador de fin de celda    
                        arrayRGB.append([256,256,256])
            if identificadorCelda == 0:
                print("La columna " + self.columnaClasificadora + " no se encontro en el archivo a procesar")                        
                sys.exit()
            if numeroFila != 1:
                # cuando se procesa toda una fila se guarda la imagen resultante en la carpeta correspondiente
                nombre = os.path.basename(self.archivoOrigen) + "_fila_" + str(numeroFila) + ".png"
                arrayRGBAjustado = self.ajustarColores(arrayRGB)
                self.guardarImagen(arrayRGBAjustado,CarpetaDestino,nombre)
                #sys.exit()
                #print(arrayRGB)
                #print("Ya se proceso la fila ",numeroFila)
                #print("las celdas originales eran ", arrayceldas)
                #print("las celdas decodificadas son ")
                #self.decodificarArrayRGB(arrayRGB)
#            if numeroFila == 5:                
#                sys.exit()


    def ajustarColores(self,arrayRGB):
        """
            Funcion que permite convertir un arreglo de valores en un nuevo arreglo que derscarta los valores
            nulos, recive un arreglo de la forma [[0,0,#],[0,#,#]...,[0#,0,#]] y devuelve [[#,#,#],...,[#,#,#]]

            Argumentos: 
                arrayRGB: arreglo que contiene valores de pixeles

            Retorna:
                arrayPixelesARetornar: arreglo que contiene los pixeles validos de array RGB
        """
        #primera accion, obtenemos todos los colores de los pixeles diferentes de cero y los guardamos en el array de colores validos
        # #######################################
        # print("imprimimos el array original")
        # for p in arrayRGB:
        #     if p != [256,256,256]:
        #         print(p)
        #     else:
        #         print("")
        # ######################################
        arrayColoresValidos = []
        for pixel in arrayRGB:
            if pixel != [256,256,256]:
                for color in pixel:
                    if color != 0:
                        arrayColoresValidos.append(color)
            else:
                arrayColoresValidos.append(256)
        # ################################################                
        # print("imprimimos colores validos")
        # print(arrayColoresValidos)
        # for p in arrayColoresValidos:
        #     if p != 256:
        #         print(p)
        #     else:
        #         print("")
        # #sys.exit()                
        # #######################################        
        arrayPixelesARetornar = []
        #segunda accion, colvemos a poner los colores en grupos de trews para generar un pixel
        tamanio = len(arrayColoresValidos)
        contadorColor = 0
        pixelOriginal = [255,255,255]
        pixel = pixelOriginal.copy()
        for i in range(tamanio - 1):
            color = arrayColoresValidos[i]
            colorSiguiente = arrayColoresValidos[i + 1]
            if color == 256:
                arrayPixelesARetornar.append([256,256,256])
            else:
                pixel[contadorColor] = color
                contadorColor = contadorColor + 1
                if (contadorColor == 3) or  (colorSiguiente == 256):
                    #print(pixel)
                    arrayPixelesARetornar.append(pixel.copy())
                    pixel = pixelOriginal.copy()
                    contadorColor = 0                
        # #######################################
        # print("imprimimos el array nuevo")
        # for p in arrayPixelesARetornar:
        #     if p != [256,256,256]:
        #         print(p)
        #     else:
        #         print("")
        # ######################################

        return arrayPixelesARetornar


    def guardarImagen(self,arrayRGB,CarpetaDestino,nombreimagen):
        """
            Funcion que permite guardar un arreglo de pixeles como una imagen

            Argumentos:
                arrayRGB: arreglo de pixeles
                CarpetaDestino: carpeta donde se fguardara la imagen
                nombreimagen: combre de la imagen a guardar
            Retorna 
        """
        # si alguna de las dos variables es cero significa que el programa debe definir el tamanio del archivo de salida
        anchoMayor = 1
        altoMayor = 1
        contadorAncho = 0
        #Variables de tamanio de archivo
        alto = self.altoImagenes
        ancho = self.anchoImagenes
        # Si alguna de las dos variables es cero se debe ajustar el tamanio a el maximo necesario para los datos 
        if (self.anchoImagenes == 0) or (self.altoImagenes == 0):
            for pixel in arrayRGB:
                if pixel != [256,256,256]:
                    contadorAncho = contadorAncho + 1
                    print(contadorAncho,pixel,end="")
                else:
                    print(pixel)
                    if contadorAncho > anchoMayor:
                        anchoMayor = contadorAncho
                    contadorAncho = 0
                    altoMayor = altoMayor + 1
            if self.anchoImagenes == 0:
                ancho = anchoMayor
            if self.altoImagenes == 0:
                alto = altoMayor
        if (anchoMayor > ancho):
            print("El ancho en pixeles necesario para escribir la imagen " + nombreimagen + " es mayor a (" + str(ancho) + ") por lo que se ajusto al tamaño necesario (" + str(anchoMayor) + ")")
            ancho = anchoMayor
        if (altoMayor > alto):
            print("El alto en pixeles necesario para escribir la imagen " + nombreimagen + " es mayor a (" + str(alto) + ") por lo que se ajusto al tamaño necesario (" + str(altoMayor) + ")")            
            alto = altoMayor
        #print("Ancho a guardar",ancho)
        #print("Alto a guardar",alto)

        # se crea una nueva imagen en modo RGB
        print("Tama;os",ancho,alto)
        ancho = ancho + 1
        alto = alto + 1
        try:
            imagen = Image.new("RGB", (ancho, alto), "white")  # Color de fondo blanco por defecto
        except Exception as e:
            print("Ocurrio un error al generar la firma grafica")
            print(e)
            return 0
        CarpetaDestino = self.carpetaDestinoPrincipal + CarpetaDestino
        #print(CarpetaDestino)
        # se asignan los valores RGB a cada píxel
        #print("Los valores rgb a guardarse como imagen en  ",CarpetaDestino)        
        x = 0
        y = 0
        contador = 0
        for pixel in arrayRGB:
            contador = contador + 1
            if pixel != [256,256,256]:
                #print(pixel,end="")
                try:
                    imagen.putpixel((x, y), tuple(pixel))
                except Exception as e:
                    print(e)
                    print(pixel)
                    sys.exit()
                x = x + 1
            else:
                #print("")
                y = y + 1
                x = 0
        ## Primer píxel (fila 1, columna 1)
        #imagen.putpixel((1, 0), tuple(pixeles_rgb[1]))  # Segundo píxel (fila 1, columna 2)
        #imagen.putpixel((0, 1), tuple(pixeles_rgb[2]))  # Tercer píxel (fila 2, columna 1)
        print("el for afuera")
        # Crear la carpeta si no existe
        if not os.path.exists(CarpetaDestino):
            os.makedirs(CarpetaDestino)
    
        # Guardar la imagen en la carpeta correspondiente
        ruta_imagen = os.path.join(CarpetaDestino, nombreimagen)
        #print(ruta_imagen)
        imagen.save(ruta_imagen)
    
        #print(f"Imagen guardada en '{ruta_imagen}'")



    # def decodificarArrayRGB(self, arrayRGB):
    #     #print("\033[91m" + "voy a decodificar " + "\033[0m",arrayRGB)
    #     arrayHex = []
    #     for rgb in arrayRGB:
    #         #print("este es el rgb ",rgb)
    #         if rgb != [256,256,256]:
    #             #print("rgb diferente de 0")
    #             unicodeBinario = ""
    #             for decimal in rgb:
    #                 unicodeBinario = unicodeBinario + str(self.decimal_a_binario_8bits(decimal))
    #             #print("este es el binario  ",unicodeBinario)
    #             unicodeHex = self.binario_a_hexadecimal(unicodeBinario)    
    #             #print("este es el binario  en hex ",unicodeHex)
    #             arrayHex.append(unicodeHex)
    #         else:
    #             #print("rgb es o o o ")
    #             #print(arrayHex)
    #             print(self.obtener_caracter_desde_unicode(arrayHex))
    #             arrayHex = []
        
            



    def cadenaADecimalHexadecimal(self,cadena):
        """
            Funcion que convierte una cadena de caracteres a sus valores decimales y hexadecimales codificados segu unicode

            Argumentos
                cadena: cadena de bits

            Retorna
                tupla que contiene la conversion
        """
        # Codificar la cadena en UTF-8
        utf8_bytes = cadena.encode('utf-8')

        # Convertir los bytes a valores decimales
        utf8_codificacion_decimal = [byte for byte in utf8_bytes]

        # Convertir los bytes a valores hexadecimales
        utf8_codificacion_hex = [f"{byte:02X}" for byte in utf8_bytes]

        return utf8_codificacion_decimal, utf8_codificacion_hex  


    # def binario_a_hexadecimal(self,binario):
    #     decimal = int(binario, 2)

    #     hexadecimal = hex(decimal)[2:]  # Eliminar el prefijo '0x'
    
    #     return hexadecimal.upper()  # Devolver en mayúsculas



    # def obtener_caracter_desde_unicode(self,arrayhex):
    #     try:
    #         cadena = ""
    #         for hex in arrayhex:
    #             punto_de_codigo_int = int(hex, 16)
    #             caracter = chr(punto_de_codigo_int)
    #             cadena = cadena + caracter
    #         try:
    #             return int(cadena)
    #         except Exception as e:
    #             if cadena == "None":
    #                 return None
    #             elif cadena == "True":
    #                 return True
    #             elif cadena == "False":
    #                 return False
    #             else:
    #                 return cadena
    #     except ValueError:
    #         return None              



    # def decimal_a_binario_8bits(self, decimal):
    #     # Manejar el caso 0 explícitamente
    #     if decimal == 0:
    #         return '00000000'
    #     # Convertir a binario y eliminar el prefijo '0b'
    #     binario = bin(decimal)[2:]
    # 	# Asegurar que tenga 8 bits, agregando ceros a la izquierda si es necesario
    #     binario_8bits = binario.zfill(8)
    #     # Si el número es mayor que 255, se puede truncar o gestionar según sea necesario
    #     if decimal > 255:
    #         return binario_8bits[-8:]  # Devolver los últimos 8 bits
    #     return binario_8bits

    def decialABinario24(self,decimal):
        """
            Funcion que convierte un valor decimal a bonario de 24 bits

            Argumentos:
                decimal: valor a convertir

            Retorna: valor convertido
        """
        if decimal >= 0:
            binario = bin(decimal)[2:] 
        else:
            binario = bin(decimal & 0xFFFFFF)[2:]

        binario_24bits = binario.zfill(24)

        return binario_24bits
    
    def dividirBinarioenBytes(self,binario):
        """
            Funcion que divide un valor binario de 24 bits en un arreglo de bytes

            Argumentos:
                binario: valor a convertir

            Retorna: arreglo de bytes 
        """
        #se procesa caracter por caracter 
        cadena = str(binario)
        #print(cadena)
        arrayBytes = []
        byte = ""
        contador = 0
        for caracter in cadena:
            byte = byte + caracter
            contador = contador + 1
            if contador == 8:
                arrayBytes.append(byte)
                byte = ""
                contador = 0
        return arrayBytes                

    def array_binarios_a_RGB(self,arrayBinario):
        """
            Funcion que convierte un arreglo de bytes en binario a sus valor respectiivos en decimal o RGB

            Argumentos:
                arrayBinario: arreglo a convertir

            Retorna: arreglo convertido
        """
        arrayDecimales = []
        for binario in arrayBinario:
            # Validar si la cadena es un número binario válido
            if not all(bit in '01' for bit in binario):
                raise ValueError("La cadena no es un número binario válido.")
    
            # Convertir binario a decimal
            decimal = 0
            longitud = len(binario)

            for i in range(longitud):
                # Convertir el bit a decimal y leerlo desde el final
                bit = int(binario[longitud - 1 - i])  
                decimal += bit * (2 ** i)

            arrayDecimales.append(decimal)
        

        # se revisa si el arrray resultante se compone de solo un pixel valido, es decir tiene al menos dos pixeles en cero probocando un color azulado
        # suma = 0
        # tamanio = len(arrayDecimales)
        # contador = 0
        # for decimal in arrayDecimales:
        #     suma = suma + decimal
        #     if decimal == 0:
        #         contador = contador + 1
        # if contador == (tamanio - 1):
        #     for i in range (tamanio):
        #         arrayDecimales[i] = suma

        # print(arrayDecimales)


        return arrayDecimales


if __name__ == "__main__":
    # Configurar el analizador de argumentos
    parser = argparse.ArgumentParser(description="Argumentos que permiten ejecutar el programa")
    # Agregar argumentos
    parser.add_argument("--archivoEntrenamiento", type=str, required=True, default="",                  help="Nombre del archivo que se va a procesar")
    parser.add_argument("--carpetaSalida",        type=str               , default="Resultado/",      help="Nombre de la carpeta donde se va a guardar")
    parser.add_argument("--columnaClasificadora", type=int, required=True, default="",                  help="Columna que permitira la clasificacion de cada registro")
    parser.add_argument("--anchoImagenes",        type=int,                default=0,                   help="Ancho de la imagen a generar")  
    parser.add_argument("--altoImagenes",         type=int,                default=0,                   help="Alto de la imagen a generar")  
    parser.add_argument("--listaCategorias",      type=str,                default="",                  help="Lista de categorias, se compone de [[Columna1Categoria1,Columna2Categoria1,...],[[Columna1Categoria2,Columna2Categoria2,...],[.........]]")  
    args = parser.parse_args()

    #codificar = codificarExcel('./DummieDataSet.xlsx','./ResultDataSet.xlsx',"NeedRV",100,100)
    codificar = codificarExcel(origen=args.archivoEntrenamiento,destino=args.carpetaSalida,columnaClasificadora=args.columnaClasificadora,ancho=args.anchoImagenes,alto=args.altoImagenes)


    #print(codificar.decialABinario24(codificar.elMayor))
    #print(codificar.decialABinario24(codificar.elMenor))
    #print(codificar.decialABinario24(1114111))
    #print(codificar.dividirBinarioenBytes("12345678abcdefghABCDEFGH"))
    #print(codificar.dividirBinarioenBytes(codificar.decialABinario24(1114111)))
    #print(codificar.array_binarios_a_RGB(codificar.dividirBinarioenBytes(codificar.decialABinario24(1114111))))
