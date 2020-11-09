"""
Created on Sat Nov 07 11:58:13 2020

@author: Rodrigo Baranda
@Description: Extracción de datos Macroeconómicos de Expansión para la realización de la Práctica 1 de Tipología y Ciclo de Vida del Dato.
@Webs scrapeadas: https://datosmacro.expansion.com/paro ; https://datosmacro.expansion.com/smi ; https://datosmacro.expansion.com/mercado-laboral/salario-medio.

"""

import os
import selenium # Scraping
import time #Sleeps
import pandas as pd #Tratamiento de ficheros. 
from selenium import webdriver

os.chdir(r'C:\Users\rbaranda\Documents\Rodrigo\UOC\Tipología y Ciclo de Vida del Dato\Práctica\Práctica 1')

"""
Función que realiza la lectura de los datos de las tablas de expansión y que los va recogiendo en un diccionario.
...

Attributes
----------
diccionario: dict
	estructura de datos que contiene la estructura de la tabla que se va a leer en cada caso (tasa_desempleo, salario_minimo o salario_medio).
año : int
	año para el que se están leyendo los datos.
driver : selenium object
	objeto de selenium que emula el navegador de Chrome.
table_tasa_desempleo: str
	contiene el xpath que hace referencia a la tabla que queremos leer en el caso de obtención de datos de tasa de desempleo.
table_salario_minimo: str
	contiene el xpath que hace referencia a la tabla que queremos leer en el caso de obtención de datos de salario mínimo.
table_salario_medio: str
	contiene el xpath que hace referencia a la tabla que queremos leer en el caso de obtención de datos de salario medio.

Output
-------
diccionario
	el resultado siempre es el diccionario con los datos de la web completados.
"""

def get_data_from_table(diccionario, año, driver,
                        table_tasa_desempleo = None, table_salario_minimo = None, table_salario_medio = None,
                        flag_tasa_desempleo = False, flag_salario_minimo = False, flag_salario_medio = False):
    
    # Dependiendo de la tabla que estemos leyendo, habrá unas columnas u otras.
    
    if flag_tasa_desempleo == True:
		
		# Leemos desde la fila 1 hasta el total de filas que haya para ese año.
		
        for fila in range(1, len(driver.find_elements_by_xpath(table_tasa_desempleo))):

            fila_path = '//*[@id="tb1_42"]/tbody/tr['
            fila_path += str(fila)

            diccionario['Año'].append(año)
            diccionario['País'].append(driver.find_element_by_xpath(fila_path + ']/td[1]').text)
            diccionario['Tasa Desempleo'].append(driver.find_element_by_xpath(fila_path + ']/td[2]').text)
            diccionario['Var.'].append(driver.find_element_by_xpath(fila_path + ']/td[4]').text)
            diccionario['Var. Año'].append(driver.find_element_by_xpath(fila_path + ']/td[5]').text)
            diccionario['Mes'].append(driver.find_element_by_xpath(fila_path + ']/td[6]').text)
    
    elif flag_salario_minimo == True:
        
        for fila in range(1, len(driver.find_elements_by_xpath(table_salario_minimo))):

            fila_path = '//*[@id="tb1"]/tbody/tr['
            fila_path += str(fila)

            diccionario['Año'].append(año)
            diccionario['País'].append(driver.find_element_by_xpath(fila_path + ']/td[1]').text)
            diccionario['Fecha'].append(driver.find_element_by_xpath(fila_path + ']/td[2]').text)
            diccionario['SMI Mon. Local'].append(driver.find_element_by_xpath(fila_path + ']/td[4]').text)
            diccionario['SMI €'].append(driver.find_element_by_xpath(fila_path + ']/td[6]').text)
            diccionario['Var.'].append(driver.find_element_by_xpath(fila_path + ']/td[7]').text)
            
    elif flag_salario_medio == True:
        
        for fila in range(1, len(driver.find_elements_by_xpath(table_salario_medio))):

            fila_path = '//*[@id="tb1"]/tbody/tr['
            fila_path += str(fila)

            diccionario['Año'].append(año)
            diccionario['País'].append(driver.find_element_by_xpath(fila_path + ']/td[1]').text)
            diccionario['Salario Medio'].append(driver.find_element_by_xpath(fila_path + ']/td[2]').text)
            diccionario['Var.'].append(driver.find_element_by_xpath(fila_path + ']/td[4]').text)
        
    
    return diccionario
            			
chromeDriver = r'.\chromedriver.exe' # Driver de Chrome.
driver = webdriver.Chrome(executable_path=chromeDriver)
driver.maximize_window()

# Urls de las webs que queremos leer
urls = ['https://datosmacro.expansion.com/paro?anio=', 'https://datosmacro.expansion.com/smi?anio=',
        'https://datosmacro.expansion.com/mercado-laboral/salario-medio?anio=']

# Selecciona los años en que quieres obtener los datos.
año_inicial = 2006 
año_final = 2020

años = range(año_inicial-1, año_final+1)

aceptar_cookies = '//*[@id="didomi-notice-agree-button"]' # Botón para aceptar las cookies la primera vez que se abre el navgador.

# Estructura de datos para cada caso.
tasa_desempleo = {'Año':[], 'País':[], 'Tasa Desempleo':[],'Var.':[], 'Var. Año':[], 'Mes':[]}
salario_minimo = {'Año':[], 'País':[], 'Fecha':[],'SMI Mon. Local':[], 'SMI €':[], 'Var.':[]}
salario_medio = {'Año':[], 'País':[], 'Salario Medio':[], 'Var.':[]}

# Xpaths que contiene el nombre de la tabla a leer en cada caso.
table_tasa_desempleo = '//*[@id="tb1_42"]/tbody/tr'
table_salario_minimo = '//*[@id="tb1"]/tbody/tr' 
table_salario_medio = '//*[@id="tb1"]/tbody/tr' 

# Flag para saber si se han aceptado ya o no las cookies.
cookies_accepted = False

for url in urls:
    
    for index, año in enumerate(años):

        driver.get(url+str(año)) # Para ir pasando de un año a otro partimos de la url inicial y le concatenamos el año que aplique en cada caso.

        if index == 0 and not cookies_accepted: # Hay que aceptar las cookies de la web la primera vez que se abre el navegador.
            # Intento clickar en Aceptar Cookies hasta que aparezca el elemento.
            while not cookies_accepted:
                try:
                    driver.find_element_by_xpath(aceptar_cookies).click()
                    cookies_accepted = True
                except:
                    pass

        time.sleep(2)
        
        if url == 'https://datosmacro.expansion.com/paro?anio=':
            tasa_desempleo = get_data_from_table(tasa_desempleo, año, driver, table_tasa_desempleo=table_tasa_desempleo,
                                                 flag_tasa_desempleo = True)
        elif url == 'https://datosmacro.expansion.com/smi?anio=':
            salario_minimo = get_data_from_table(salario_minimo, año, driver, table_salario_minimo=table_salario_minimo,
                                                 flag_salario_minimo = True)
        elif url == 'https://datosmacro.expansion.com/mercado-laboral/salario-medio?anio=':
            salario_medio = get_data_from_table(salario_medio, año, driver, table_salario_medio=table_salario_medio,
                                                 flag_salario_medio = True)
												 
driver.close()

tasa_desempleo = pd.DataFrame.from_dict(tasa_desempleo)
salario_minimo = pd.DataFrame.from_dict(salario_minimo)
salario_medio = pd.DataFrame.from_dict(salario_medio)

# Consolidamos la información de tasa_desempleo y salario_mínimo en un único dataset.
datos_macroec = pd.merge(tasa_desempleo, salario_minimo, how = 'inner', on =['Año', 'País'], indicator = True)

columns_mapper = {'Var. Año':'Varianza Anual Desempleo'}
datos_macroec.rename(columns = columns_mapper, inplace = True)
datos_macroec.drop(columns='_merge', inplace = True)

# Consolidamos datos macroeconómicos con salario medio.
datos_macroec = datos_macroec.merge(salario_medio, how = 'inner', on =['Año', 'País'], indicator = True)

# Elegimos las columnas que queremos exportar.
datos_macroec = datos_macroec[['Año', 'País', 'Tasa Desempleo', 'Varianza Anual Desempleo','SMI €', 'Salario Medio']]

# Exportamos todos los DataFrames creados por si nos pueden ser útiles en momentos posteriores del análisis.
datos_macroec.to_csv('.\datos_macro.csv', encoding = 'Windows-1252', sep = ',')
salario_medio.to_csv('.\salario_medio.csv', encoding = 'Windows-1252', sep = ',')
salario_minimo.to_csv('.\salario_minimo.csv', encoding = 'utf-8', sep = ',')
tasa_desempleo.to_csv('.\desempleo.csv', encoding = 'Windows-1252', sep = ',')