import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split # Paquete para separar datos en: datos para entrenamiento(los que tengo en la BD) y datos para prueba(los que voy a probar), porque los de prueba los va a validar, para aplicar métricas que digan si el modelo se está comportando bien
from sklearn.metrics import mean_absolute_error, r2_score # Métricas para validar el modelo

# encoding: en qué código en que está configurado el DataSet. Dane "latin-1". Se pone cono parámetro el read. Sep se usa para separar

# Importar varias tablas
inmuebles = pd.read_csv('inmuebles_bogota_tratada.csv', sep=',')
upz = pd.read_csv('cod_upz.csv', sep=',')
datos_a = pd.read_csv('Identificación (Capítulo A).csv', sep = ';', encoding='latin-1')
datos_b = pd.read_csv('Datos de la vivenda y su entorno (Capítulo B).csv', sep = ';', encoding='latin-1')
datos_c = pd.read_csv('Condiciones habitacionales del hogar (Capítulo C).csv', sep = ';', encoding='latin-1')
datos_k = pd.read_csv('Fuerza de trabajo (Capítulo K).csv', sep = ';', encoding='latin-1')
# print(datos_a.head(10))
# shape: Ver tamaño
# print(datos_a.shape)

# Seleccionar datos de Bogotá (que es el código 11001)
datos_a = datos_a.loc[datos_a.MPIO == 11001]
# datos_b = datos_b.loc[datos_b.MPIO == 11001]
# print(datos_a)

# merge: Fusionar tablas a través de una "clave", que es un identificador. En este caso, es la columna diectorio. Solo se pueden fusionar dos tablas al tiempo, si quiero fusionar otra, entonces en otra línea la fusiono con la original (en este caso, datos_dane, datos_c)
datos_dane = pd.merge(datos_a, datos_b, on='DIRECTORIO', how='left') # on es el identificador, how, es en qué dirección va a fusionar 
datos_dane = pd.merge(datos_dane, datos_c, on='DIRECTORIO', how='left') # on es el identificador, how, es en qué dirección va a fusionar 
datos_dane = pd.merge(datos_dane, datos_k, on='DIRECTORIO', how='left') # on es el identificador, how, es en qué dirección va a fusionar 
print(datos_dane.head(10))

# Si los nombres de las columnas no son comprensibles, se le cambia los nombres con diccionarios
dic_dane = {
       'NVCBP4':'CONJUNTO_CERRADO',
       'NVCBP14A':'FABRICAS_CERCA', 'NVCBP14D':'TERMINALES_BUS', 'NVCBP14E':'BARES_DISCO', 
       'NVCBP14G':'OSCURO_PELIGROSO', 'NVCBP15A':'RUIDO', 'NVCBP15C':'INSEGURIDAD',
       'NVCBP15F':'BASURA_INADECUADA', 'NVCBP15G':'INVASION','NVCBP16A3':'MOV_ADULTOS_MAYORES', 
       'NVCBP16A4':'MOV_NINOS_BEBES',
       'NPCKP17':'OCUPACION','NPCKP18':'CONTRATO','NPCKP23':'SALARIO_MES', 
       'NPCKP44A':'DONDE_TRABAJA', 'NPCKPN62A':'DECLARACION_RENTA', 
       'NPCKPN62B':'VALOR_DECLARACION', 'NPCKP64A':'PERDIDA_TRABAJO_C19', 
       'NPCKP64E':'PERDIDA_INGRESOS_C19',
       'NHCCP3':'TIENE_ESCRITURA', 'NHCCP6':'ANO_COMPRA', 'NHCCP7':'VALOR_COMPRA', 'NHCCP8_1':'HIPOTECA_CRED_BANCO',
       'NHCCP8_2':'OTRO_CRED_BANCO', 'NHCCP8_3':'CRED_FNA', 'NHCCP8_6':'PRESTAMOS_AMIGOS',
       'NHCCP8_7':'CESANTIAS', 'NHCCP8_8':'AHORROS', 'NHCCP8_9':'SUBSIDIOS',
       'NHCCP9':'CUANTO_PAGARIA_MENSUAL', 'NHCCP11':'PLANES_ADQUIRIR_VIVIENDA', 
       'NHCCP11A':'MOTIVO_COMPRA', 'NHCCP12':'RAZON_NO_ADQ_VIV', 'NHCCP41':'TIENE_CARRO','NHCCP41A':'CUANTOS_CARROS',
       'NHCCP47A':'TIENE_PERROS', 'NHCCP47B':'TIENE_GATOS', 'NHCLP2A':'VICTIMA_ATRACO', 'NHCLP2B':'VICTIMA_HOMICIDIO', 
       'NHCLP2C':'VICTIMA_PERSECUSION',
       'NHCLP2E':'VICTIMA_ACOSO', 'NHCLP4':'COMO_VIVE_ECON', 'NHCLP5':'COMO_NIVEL_VIDA', 
       'NHCLP8AB':'REACCION_OPORTUNA_POLICIA', 'NHCLP8AE':'COMO_TRANSPORTE_URBANO', 'NHCLP10':'SON_INGRESOS_SUFICIENTES',
       'NHCLP11':'SE_CONSIDERA_POBRE', 'NHCLP29_1A':'MED_C19_TRABAJO', 
       'NHCLP29_1C':'MED_C19_CAMBIO_VIVIENDA', 'NHCLP29_1E':'MED_C19_ENDEUDAMIENTO', 
       'NHCLP29_1F':'MED_C19_VENTA_BIENES','NPCHP4':'NIVEL_EDUCATIVO'
       }

datos_dane = datos_dane.rename(columns=dic_dane)
datos_dane.columns

# Agrupar por UPZ, mirando otras variables
datos_dane.groupby('NOMBRE_ESTRATO')[['CONJUNTO_CERRADO','INSEGURIDAD','TERMINALES_BUS', 'BARES_DISCO','RUIDO','OSCURO_PELIGROSO','TIENE_ESCRITURA','PERDIDA_TRABAJO_C19','PERDIDA_INGRESOS_C19','PLANES_ADQUIRIR_VIVIENDA','SALARIO_MES']].mean().head() # No funcionaron ,

# Reemplazar el #2 por el # 0, para que 0 sea No, y 1 sea Sí eb los datos binarios
datos = datos_dane[['NOMBRE_ESTRATO','CONJUNTO_CERRADO','INSEGURIDAD','TERMINALES_BUS','BARES_DISCO','RUIDO','OSCURO_PELIGROSO','TIENE_ESCRITURA','PERDIDA_TRABAJO_C19','PERDIDA_INGRESOS_C19','PLANES_ADQUIRIR_VIVIENDA','SALARIO_MES']].replace(2, 0)

print(datos.NOMBRE_ESTRATO.value_counts())

#Calcular promedio agrupados por estrato, en porcentaje
datos_Tratados = datos.groupby('NOMBRE_ESTRATO')[['CONJUNTO_CERRADO','INSEGURIDAD','TERMINALES_BUS','BARES_DISCO','RUIDO','OSCURO_PELIGROSO','TIENE_ESCRITURA','PERDIDA_TRABAJO_C19','PERDIDA_INGRESOS_C19','PLANES_ADQUIRIR_VIVIENDA','SALARIO_MES']].mean()
print(datos_Tratados)

# FUSIONAR DATOS DEL DANE CON LA BD DE INMUEBLES
datos_ml = pd.merge(inmuebles, datos_Tratados, left_on='UPZ', right_on='NOMBRE_ESTRATO', how='left') # Primero se pone la tabla de la izquierda. Como las variables con las que voy a agrupar, se poner left_on para el nombre de la tabla de la izquierda, y right_on para el nombre de la variable de la tabla del lado derecho. El campo se queda llamado con el nombre de la tabla de la izquierda.

# Fusionar datos_ml con upz 
datos_ml = pd.merge(datos_ml, upz, left_on='UPZ', right_on='NOMBRE_ESTRATO', how='inner') #  INNER fusiona los datos que coinciden en ambas tablas

print(datos_ml.info())

# Graficar

plt.figure(figsize=(10, 8))
sns.boxplot(data=datos_ml, y= 'Precio_Millon')
# plt.show()

datos_ml = datos_ml.query('Precio_Millon > 60 & Precio_Millon < 5000') # Excluir del DataSet los datos mayores a 5000 y menores a 60 millones, porque son datos atípicos que pueden afectar el modelo. | significa 'o', & significa 'y'. Si se cambia ese rango, el modelado después cambia significativamente, se debe evaluar los datos atípicos, quitarlos

# # Crear nueva variable, salario anual, en millones
datos_ml['SALARIO_ANUAL'] = datos_ml['SALARIO_MES'] * 12 / 1000000
print(datos_ml['SALARIO_ANUAL']) 

# Graficar: salario anual, en función del valor m2
plt.figure(figsize=(10, 8))
sns.scatterplot(data=datos_ml, x='SALARIO_ANUAL', y='Valor_m2_Millon') # scatterplot: Muestra mejor una correlación
plt.ylim((0, 15)) # definir límites del eje y, para quitar datos atípicos
# plt.show() # Este gráfico específico no muestra una correlación entre ambas salario y precio por m2

#corr: relaciona variables, entre más cercano a 1, significa que se relaciona más, si es 1, entonces puede significar que son la misma
print(datos_ml.corr())

# MAPA DE CALOR
plt.figure(figsize=(18, 7))
#https://tylervigen.com/spurious-correlations Página para ver ejemplos de correlaciones espúreas: se correlacionaron por casualidad
heatmap = sns.heatmap(datos_ml.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlación de las variables', fontdict={'fontsize': 7}, pad=16);
# plt.show()

# *******************
# MACHINE LEARNING
# ***************

#Como variable respuesta usamos Precio_Millon, que es lo que queremos predecir

#Línea base, para partir de él para mejorar el modelo con experimentos. Primero se crea la variable X
# X = datos_ml[['COD_UPZ_GRUPO']] # Esta variable se escribe en mayúscula generalmente, porque es una matriz, y la variable respuesta se ingresa como un array (generando un DataFrame). Se puede escoger cualquier variable para crear la línea base. Escogimos UPZ porque puede influir el barrio en el precio del inmueble
# y = datos_ml['Precio_Millon'] # se pone y en minúscula, y se pone el pandas series. 

# #Procedemos a hacer el Split. Para eso se necesitan 4 variables: 'x' de entrenamiento, 'x' de prueba, 'y' de entrenamiento y 'y' de prueba, se hace el split con el paquete train_test_split

# X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.25, random_state=99) # a cada variable le asignamos el valor de respuesta. Test_size es la cantidad de datos que voy a usar para la prueba, por defecto es 0.25 (es en porcentaje, equivale al 75% de los datos). Siempre se debe poner random, para garantizar que en las diferentes pruebas sea repoductible los datos, porque es un modelo probabilístico, se puede poner el número que quiera, pero siempre se debe poner el mismo, que es el estado de aleatoriedad

# print(X_train) 

# modelo = LinearRegression() # Esto es instanciar el modelo
# modelo.fit(X_train, Y_train) # ajustar los datos de entrenamiento. Esto es aplicar el Machine Learning, ya el modelo está entrenado

# y_predict_test = modelo.predict(X_test) # esto luego se va a comparar con el y_test. Se predice colocando los datos de X, y que él prediga y, y luego se compara con los datos que tengo de y

# # Ahora se debe validar el modelo, aplicar métricas para conocer indicadores, para saber cómo se está desempeñando el modelo. Se usan dos métricas: error absoluto medio (mae - toma la dfcia de valores que puedo encontrar a la hora de hacer el cálculo, cuando ingreso datos en el modelo puede haber cierto margen de error, la idea es reducir ese error, para acercarse a los valores reales) medio y r2 (es el coeficiente de determinación, permite ver qué tan bien está trabajando al modelo, entre más próximo a 1 significa que el modelo está más ajustado)

# # MÉTRICAS

# # MAE
# baseline_mae = mean_absolute_error(Y_test, y_predict_test) # instanciar el mae, se pone y_prueba y y_precict, va a comparar ese cjto de datos que el modelo no vio al mometo de entrenarlo, con lo que se predijo al momento de entrenarlo
# print(baseline_mae) #el resultado de esta consulta es que si introducimos el valor de un inmueble, él va a tener una variación de 329 millones, eso significa que tiene muchos errores

# # r2
# baseline_r2 = r2_score(Y_test, y_predict_test) # r2 funciona igual que el mae
# print(baseline_r2) # este resultado muestra 0,02, lo que significa qel modelo no se está desempeñando bien

# # Lo que se hizo fue separar un datos de entrenamiento ( x y 'y', donde 'y' es la variable que queremos predecir: precio de los inmuebles), se entrena con el 75% de los datos, y el otro 25% de deja para prueba. Una vez se ejecuta el modelo, se tienen valores predichos de 'y', y los compara con los 2 indicadores que miden la eficacia del modelo (mae y r2) para ver esa eficacia, y en ambos nos arroja que el modelo no está performando bien. El siguiente paso es seguir con experimentos, entonces se usan otras 2 variables adicionales para el eje 'x' y en 'y' ponemos los los mismos datos

X = datos_ml[['COD_UPZ_GRUPO', 'Habitaciones', 'Banos']] # Tres variables para el eje x
# X = datos_ml[['COD_UPZ_GRUPO', 'Habitaciones', 'Banos', 'CONJUNTO_CERRADO', 'SALARIO_ANUAL', 'TIENE_ESCRITURA']] # Más variables(para ejecutar 'Prueba')
y = datos_ml['Precio_Millon'] 

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.25, random_state=99)
print(X_train) 

modelo_1 = LinearRegression() 
modelo_1.fit(X_train, Y_train) 

y_predict_test = modelo_1.predict(X_test) 
y_predict_train = modelo_1.predict(X_train)
# MÉTRICAS

# MAE
mae_test = mean_absolute_error(Y_test, y_predict_test) 
mae_train = mean_absolute_error(Y_train, y_predict_train)
# r2
r2_test = r2_score(Y_test, y_predict_test)
r2_train = r2_score(Y_train, y_predict_train)
# print(mae_test, r2_test) # Mejoraron los indicadores
# print(mae_train, r2_train)

# Otro caso, ingresando yo los datos, para que me diga cuánto debería costar una casa
# Prueba = modelo_1.predict([[816,3,2,1,50,1]]) # Datos ingresados: UPZ, habitaciones, baños, conjunto cerrado(1), salario anual, tiene escritura(1)
# print(Prueba)