# AnalisisMacroeconomico
Autor: Rodrigo Baranda. La práctica se ha realizado de manera individual por problemas personales.

Repositorio que contiene datos Macroeconómicos extraídos vía web scraping de la web: https://datosmacro.expansion.com/. Los datos scrapeados corresponden con datos de Tasa de Desempleo, Salario Mínimo y Salario Medio. Siendo los tres links los siguientes:

-https://datosmacro.expansion.com/paro  
-https://datosmacro.expansion.com/smi  
-https://datosmacro.expansion.com/mercado-laboral/salario-medio

No todas las secciones de la página contienen los mismos países (por ejemplo, podemos tener datos de paro de España pero no datos relativos a SMI o Salario Medio). Por lo tanto, el objetivo inicial era preparar un Dataset que contuviera toda ésta información; sin embargo, habrá países para los que podamos disponer de toda y otros para la que no. Se ha decidido exportar todos los datos recogidos por si fueran necesarios en momentos posteriores del análisis.

Los ficheros generados son:

- RodrigoBaranda_Práctica1.py. Archivo que realiza el scraping de las páginas mencionadas para los años [2006, 2020] y a partir del cual se generan los demás CSVs.
- datos_macro.csv. Archivo que contiene los datos macroeconómicos de paro, smi y salario medio para aquellos países que tengan la información registrada en la web.
- desempleo.csv. Archivo que contiene los datos de desempleo.
- salario_medio.csv. Archivo que contiene los datos de salario_medio.
- salario_minimo.csv. Archivo que contiene los datos de salario_mínimo.
