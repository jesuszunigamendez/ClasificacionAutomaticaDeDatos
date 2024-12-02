from sklearn.metrics import classification_report
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score, roc_auc_score, log_loss
import openpyxl
import sys
import time


class evaluar:

    def __init__(self,*,rutaArchivo,columnaVerdadera,columnaPredicha):
        """"
            Esta clase utiliza la biblioteca sklearn para evaluar los resultados de la clasificacion
        """       
        self.rutaArchivo = rutaArchivo
        self.columnaVerdaderos = columnaVerdadera
        self.columnaPredichos = columnaPredicha
        #
        self.arrayVerdaderos = self.obtenerArrayValores(columna=self.columnaVerdaderos[0])
        #se da un correcto formato a los strings
        self.arrayVerdaderos= self.darFormato(arreglo=self.arrayVerdaderos)
        #
        self.arrayPredichos = self.obtenerArrayValores(columna=self.columnaPredichos[0])
        #se da un correcto formato a los strings
        self.arrayPredichos= self.darFormato(arreglo=self.arrayPredichos)
        #
        self.probabilidadesPredichas = self.obtenerArrayValores(columna=(self.columnaPredichos[0]+1))        
        #se da un correcto formato a los floats
        self.probabilidadesPredichas = self.darFormato(arreglo=self.probabilidadesPredichas,probabilidad=True)
        #print(self.arrayVerdaderos)
        #print(self.arrayPredichos)
        #print(self.probabilidadesPredichas)
        #print(self.rutaArchivo) 
        #print(self.columnaVerdaderos) 
        #print(self.columnaPredichos) 
        #print(self.arrayVerdaderos)
        #print(self.arrayPredichos)
        # Generar el reporte de clasificación
        report = classification_report(self.arrayVerdaderos, self.arrayPredichos)
        print(report)
        #self.imprimirMetricas()



#    def imprimirMetricas(self):
#        """
#            Funcion que permite imprimir las metricas correspondientes para evaluar las predicciones
#
#        """
#        # Precisión
#        arraytemporarTrue = [0 if val == 'false' else 1 for val in self.arrayVerdaderos]
#        arraytemporalPredichos = [0 if val == 'false' else 1 for val in self.arrayPredichos]
#        precision = precision_score(arraytemporarTrue, arraytemporalPredichos, average='binary')  # Cambia 'binary' a 'macro' o 'weighted' si es multiclase
#        print(f"Precisión: {precision:.2f}")
#
#        # Recuperación
#        recall = recall_score(arraytemporarTrue, arraytemporalPredichos, average='binary')
#        print(f"Recuperación: {recall:.2f}")
#
#        # Exactitud
#        accuracy = accuracy_score(self.arrayVerdaderos, self.arrayPredichos)
#        print(f"Exactitud: {accuracy:.2f}")
#
#        # F1-Score
#        f1 = f1_score(arraytemporarTrue, arraytemporalPredichos, average='binary')
#        print(f"F1-Score: {f1:.2f}")
#
#        # AUC-ROC
#        try:
#            auc_roc = roc_auc_score(self.arrayVerdaderos, self.probabilidadesPredichas)  # Necesita probabilidades predichas para binaria
#            print(f"AUC-ROC: {auc_roc:.2f}")
#        except ValueError:
#            print("AUC-ROC no se puede calcular para etiquetas únicas.")

        # Log-Loss
        logloss = log_loss(self.arrayVerdaderos, self.probabilidadesPredichas)
        print(f"Log-Loss: {logloss:.2f}")        

    def darFormato(self,*,arreglo=[],probabilidad = False):
        """
            Funcion que convierte datos string contenidos en un Arreglo a minusculas y quita espacios a inicio y fin

            Argumentos:
                arreglo: arreglo al que se le aplicara el cambio

            Retorn: Arreglo formateado
        """
        retorno = []
        #se convierte a minusculas
        retorno = [x.lower() if isinstance(x, str) else x for x in arreglo]
        #se quitan espacios
        retorno = [cadena.strip() for cadena in retorno]
        if probabilidad:
            retorno = [float(cadena) for cadena in retorno]
        return retorno

    def obtenerArrayValores(self,*,columna):
        """
            Esta funcion lee un archivo de excel y retorna todos los valores existentes en la columna en forma de arreglo

            Argumentos:
                columna: numero de columna que se desea en el array
            
            Retorna:
                arreglo creado
        """
        #  se abre e; excel
        wb = openpyxl.load_workbook(self.rutaArchivo)
        # se selecciona la primera hoja
        hoja = wb.active
        #se inicializan variables
        numeroFila = 0
        numeroCelda = 0
        # for que recorre fila for fila
        arrayResultado = []
        for fila in hoja.iter_rows(values_only=True):
            numeroFila = numeroFila + 1            
            print("procesando fila ",numeroFila)            
            numeroCelda = 0
            # for que recorre celda por celda
            for celda in fila:
                numeroCelda = numeroCelda + 1
                # se procesan todas las filas menos ;a primera    
                if (numeroFila != 1):# and (identificadorCelda != 0):
                    if numeroCelda == (columna):
                        arrayResultado.append(str(celda))                                        
        return arrayResultado

