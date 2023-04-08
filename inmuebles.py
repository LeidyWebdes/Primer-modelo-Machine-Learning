import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer archivo con Pandas
inmuebles = pd.read_csv('./inmuebles_bogota.csv')
# Imprimir primeras 5 líneas del archivo. Esto es crear un Pandas Data Frame (Frame de datos), en el que se agrega una columna como auto-increment, para encontrar datos más fácilmente
print('*****\n', 'PRIMERAS 5 COLUMNAS')
print(inmuebles.head())
#shape devuelve el número de filas y columnas del archivo, los devuelve en una tupla
print('*****\n', 'NÚMERO DE FILAS Y NÚMERO DE COLUMNAS')
print(inmuebles.shape)

# Columns devuelve los nombres de las columnas del header
print('*****\n', 'NOMBRES DE COLUMNAS')
print(inmuebles.columns)

# Cambiar nombres de las columnas en un diccionario, por ejemplo para eliminar caracteres especiales
columnas = {'Baños':'Banos', 'Área':'Area'} # nombres a cambiar
inmuebles = inmuebles.rename(columns=columnas) # Asignar los nuevos diccionarios
print(inmuebles.columns)
# Samle trae una muestra de la BD, se le debe especificar cuántas filas quiero ver
print('*****\n', 'VER 5 COLUMNAS ALEATORIAS CON LOS DATOS CAMBIADOS')
print(inmuebles.sample(5))

# info muestra la información del DataSet (BD)_
print('*****\n', 'INFO DEL DATASET: rango de datos, total de columnas en orden, celdas sin valores nulos, tipo de columna (int u object(alfanumérico))')
print(inmuebles.info())

# iloc ayuda a localizar el índice 
print('*****\n', 'BUSCAR LOS DATOS DEL ÍNDICE 300')
print(inmuebles.iloc[300])

# iloc para traer varios índices seguidos
print('*****\n', 'DATOS DE ÍNDICES 300 a 305')
print(inmuebles.iloc[300:305])

# iloc para buscar por valor
print('*****\n', 'BUSCAR COl VALOR DEL ÍNDICE 300. Esto ya no es un "Pandas DataFrame" sino un "Pandas Series (que es un tipo de dato boleano)"')
print(inmuebles['Valor'][300])

# mean y nombre de columna para traer los datos de una columna determinada
print('*****\n', 'DATOS DE LA COLUMNA AREA')
print(inmuebles.Area.mean)

# mean() y nombre de col traen el promedio de los datos de la columna
print('*****\n', 'PROMEDIO DE LOS DATOS DE LA COLUMNA ÁREA')
print(inmuebles.Area.mean())

# Traer suma de datos de columna Barrio que cumplen con la condición
print('*****\n', 'NÚMERO DE INMUEBLES DEL BARRO CHICÓ RESERVADO')
print(sum(inmuebles.Barrio == 'Chico Reservado'))

# Crear una variable con los inmuebles de cierto barrio, como Pandas Series (un dato boleano)
inmuebles_chico = (inmuebles.Barrio == "Chico Reservado")
# Crear un nuevo DataFrame con los inmuebles del barrio Chico
chico_reservado = inmuebles[inmuebles_chico]
print('*****\n', 'NUEVO DATASET SOLO CON LOS INMUEBLES  DEL BARRIO CHICO RESERVADO')
print(chico_reservado)

# Precio promedio del área de chico_reservado
print('*****\n', 'PROMEDIO DE ÁREA DEL BARRIO CHICO RESERVADO')
print(chico_reservado.Area.mean())

# len value_counts() muestra cantidad de barrios
print('*****\n', 'CANTIDAD DE BARRIOS DEL ARCHIVO\nCANTIDAD DE INMUEBLES POR BARRIO')
print(len(inmuebles.Barrio.value_counts()))
# value_counts() sin len muestra cuántos inmuebles hay en cada barrio
print(inmuebles.Barrio.value_counts())

# GRÁFICOS

# Gráfico de cantidad de inmuebles por barrio
inmuebles_barrio = inmuebles.Barrio.value_counts() # Asignar la función a una variable
inmuebles_barrio.plot.bar() # Generar gráfico de barras
# plt.show()

inmuebles_barrio.head(10).plot.bar() # generar gráfico. Head indica cuántos barrios quiero que me salgan en el gráfico
# plt.show()

# CLASE 2

# split separa cadenas en función de un parámetro. El parámetro por defecto es el espacio
print('*****\n', 'CONVERTIR CADENAS CON SPLIT: Separar por espacio en el index 0')
print(inmuebles.Valor[0].split()) # Separé en dos cadenas
print('*****\n', 'CONVIERTO LOS VALORES EN CADENAS (porque son PandasSeries), Y CADA ELEMENTO SE CIERRA EN UNA LISTA, CONVERTIDO EN UN DATAFRAME\nEl dato se convierte en 3 columnas')
valor = inmuebles.Valor.str.split(expand=True)  # expand convierte el formato a DataFrame. Y lo almaceno en una nueva variable
inmuebles['Moneda'] = valor[0] #asigno los datos de la primera columna un nuevo atributo de la BD
inmuebles['Precio'] = valor[1]
inmuebles['Precio'] = inmuebles['Precio'].str.replace('.','', regex=True) # En la columna precio, se vuelve a definir igual pero reemplazando los puntos por nada. regex se debe poner porque si no aparece una alerta. Si no se encuentra el caracter a reemplazar, no pasa nada
print('*****\n', 'REEMPLAZAR LOS PUNTOS DEL PRECIO')
print(inmuebles[['Barrio', 'Precio']])
# print(inmuebles.sample(3))

# astype: Transformar dato str a float
print('*****\n', 'PASO STR A NÚMERO Y CONVERTIRLO A PRECIO EN MILLONES')
inmuebles['Precio_Millon'] = inmuebles.Precio.astype('float')/1000000 # Se cambia el tipo de dato con astype, y se divide por un millon para que sea más fácil leerlo, asignando este nuevo dato a un nuevo atributo

#set_option para eliminar decimales
print('*****\n', 'LIMITAR DECIMALES')
pd.set_option('display.precision',2) # display_precision: solo ver dos decimales
pd.set_option('display.float_format', lambda x: '%.2f' % x) #para los datos float, mostrar el formato también con 2 decimales

# describe: función con varios datos estadísticos de cada atributo
print('*****\n', 'DATOS ESTADÍSTICOS DE CADA ATRIBUTO: count: cantidad total, mean:promedio de datos, std:desviación standard(alejamiento o cercanía con respecto a la media), min:mínimo, máximo, percentiles, max: máximo')
print(inmuebles.describe())

# loc: localizar cierto dato
print('*****\n', 'LOCALIZAR UN DATO EN PARTICULAR')
print(inmuebles.loc[inmuebles.Area == 2])

# hist: histograma
inmuebles['Precio_Millon'].plot.hist(bins=50) #bins: define el rango de visualización, entre má alto el número, más definido será el rango
# plt.show()

# SEABORN: librería basada en MatPlotLib para graficar datos, estéticamente esta más desarrollada
# Crear histograma con seaborn
plt.figure(figsize=(10,8)) # Hacer figura con seaborn, la figsize es el tamaño del gráfico
grafica = sns.histplot(data=inmuebles, x='Precio_Millon', kde=True, hue='Tipo') # crear el gráfico con seaborn, hay muchos parámetros para la visualización. kde hace la curva de los datos. hue añade otro parámetro a la gráfica, para hacer comparaciones, aquí usamos el tipo de inmueble
grafica.set_title('Distribución de los valores de los inmuebles en Bogotá') # Título de la gráfica
plt.xlim((500, 2000)) # definir los límites del gráfico, para que sea más facil de leer, se puede definir el criterio con los valores mínimo y máximo del atributo, o menos (con los cuartiles), dependiento de las necesidades
plt.savefig('C:/Users/User/Desktop/valor_inmuebles.png', format='png') #guardar archivo. Se debe poner la ruya completa y el formato
plt.ylim(0,100) # definir el rango en el eje y
# plt.show()

## AULA 3

# Crear nueva columna
print('*****\n', 'NUEVA COLUMNA: valor M2 en millones por cada inmueble')
inmuebles['Valor_m2_Millon'] = inmuebles['Precio_Millon'] / inmuebles['Area']

# print(inmuebles.head(3))

# Groupy = para agrupar por precio por M2
print('*****\n', 'AGRUPAR POR BARRIOS: PROMEDIO PRECIO M2 A NIVEL DE CIUDAD: con base en todos los barrios, no por el barrio en particular')
print(inmuebles.groupby('Barrio').mean())
# Agrupar por precio por barrio, para sacar el promedio de cada barrio
print('*****\n', 'PROMEDIO $ x M2 POR BARRIO')
datos_barrio = inmuebles.groupby('Barrio').sum() # sumar los datos por barrio
datos_barrio['Valor_m2_Barrio'] = datos_barrio['Precio_Millon'] / datos_barrio['Area'] # dividir los metros2 entre el precio de cada barrio
print(datos_barrio)

# Aignar el valor del M2 barrio y asignarlo al DataSet inmuebles, generando un diccionario almacenando los nuevos valores
m2_barrio = dict(datos_barrio['Valor_m2_Barrio']) #Diccionario con el nombre del barrio y el nuevo valor de $ x M2
#Asignar valores a los barrios
inmuebles['Valor_m2_Barrio'] = inmuebles['Barrio']
inmuebles['Valor_m2_Barrio'] = inmuebles['Valor_m2_Barrio'].map(m2_barrio) # cambiar los valores por los del nuevo valor calculado

# Exportar tabla
# inmuebles.to_csv('inmuebles_bogota_tratada.csv')

# CONSULTAR DATOS CON OTRAS FUNCIONES
print('*****\n', 'LOS 10 BARRIOS CON MÁS INMUEBLES A LA VENTA')
top_barrio = inmuebles['Barrio'].value_counts()[:10].index # El índice es el nombre del barrio, el contenido es el contador
print(top_barrio)

datos_barrio.reset_index(inplace=True) #convertir "Barrio" en una columna, no en index

datos_barrio.query('Barrio in @top_barrio') # traer el top 10 en un dataframe, con una consulta

# Graficar los 10 barrio
print('*****\n', 'GRÁFICA DE BARRAS LOS 10 BARRIOS CON MÁS INMUEBLES A LA VENTA')
plt.figure(figsize=(10,8))
ax = sns.barplot(x='Barrio', y='Valor_m2_Barrio', data = datos_barrio.query('Barrio in @top_barrio')) # data es el query
ax.tick_params(axis='x', rotation=45) #Rotar el je x
# plt.show()
print('*****\n', 'GRÁFICA DE CAJA LOS 10 BARRIOS CON MÁS INMUEBLES A LA VENTA, HASTA 15 MILLONES x M2')
ax = sns.boxplot(x='Barrio', y='Valor_m2_Barrio', data = inmuebles.query('Barrio in @top_barrio & Valor_m2_Millon < 15')) # data es el query, viendo el precio, y agregando condición al query, máximo 15' por m2, para eliminar los datos atípicos

# Ver datos por área
ax = sns.boxplot(x='Barrio', y='Area', data = inmuebles.query('Barrio in @top_barrio & Area < 500')) # Ver barrios por área

# Datos por precio
ax = sns.boxplot(x='Barrio', y='Precio_Millon', data = datos_barrio.query('Barrio in @top_barrio & Precio_Millon < 2000')) # data es el query, viendo el precio, y agregando condición al query
# plt.show()

# encoding: en qué código en que está configurado el DataSet. Dane "latin-1". Se pone cono parámetro el read. Sep se usa para separar
