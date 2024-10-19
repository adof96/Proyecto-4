
# %% [markdown]
# ## Inicialización

# %%
import pandas as pd
from matplotlib import pyplot as plt 
import seaborn as sns 
import numpy as np
import math as m
from scipy.stats import ttest_ind

# Cargar todas las librerías


# %% [markdown]
# ## Cargar datos

# %%
# Carga los archivos de datos en diferentes DataFrames

df_calls = pd.read_csv('datasets/megaline_calls.csv' )
df_internet= pd.read_csv('datasets/megaline_internet.csv')
df_messages = pd.read_csv('datasets/megaline_messages.csv')
df_plans= pd.read_csv('datasets/megaline_plans.csv' )
df_users= pd.read_csv('datasets/megaline_users.csv')




# %%
# Imprime la información general/resumida sobre el DataFrame de las tarifas

df_plans.info()

# %%
# Imprime una muestra de los datos para las tarifas

df_plans.head()

# %% [markdown]
# ## Corregir datos

# %%
df_plans['gb_per_month_included'] = df_plans['mb_per_month_included'] / 1024
print(df_plans)

# %% [markdown]
#
# Fue necesario agregar una columna con la transformacion de mb a gb que incluye el plan para facilitar su calculo mas adelante, ya que cada plan cobra por gb no por mb



# %% [markdown]
# ## Usuarios/as

# %%
# Imprime la información general/resumida sobre el DataFrame de usuarios

df_users.info()

# %%
# Imprime una muestra de datos para usuarios

df_users.head(15)

# %% [markdown]
# Los registros del apartado churn_date dan la fecha en la que el usuario dejo de utilizar el servicio, si el valor es ausente, es porque el usuario seguia utilizandolo al momento en que se extrajo la base de datos, esta es la razon de que haya bastantes NaN's


# %% [markdown]
# ### Corregir los datos

# %% [markdown]
# la columna 5 son fechas y esta como objet, cambiar a fechas


# %%
df_users['reg_date'] = pd.to_datetime(df_users['reg_date'], format='%Y-%m-%d')
df_users['churn_date'] = pd.to_datetime(df_users['churn_date'], format='%Y-%m-%d')

total_duplicados = df_users.duplicated().sum()
print("Total de registros duplicados:", total_duplicados)


# %%
df_users.info()
df_users.head(15)

# %% [markdown]
# ## Llamadas

# %%
# Imprime la información general/resumida sobre el DataFrame de las llamadas

df_calls.info()

# %%
# Imprime una muestra de datos para las llamadas

df_calls.head()

# %%
df_calls['call_date'] = pd.to_datetime(df_calls['call_date'], format='%Y-%m-%d')
df_calls['duration'] = np.ceil(df_calls['duration'])

total_duplicados = df_calls.duplicated().sum()
print("Total de registros duplicados:", total_duplicados)

# %%
df_calls.info()
df_calls.head()



# %% [markdown]
# Las llamadas con duracion de 0 segundos pueden deberser a llamadas perdidas o fallidas

# %% [markdown]
# ## Mensajes

# %%
# Imprime la información general/resumida sobre el DataFrame de los mensajes

df_messages.info()

# %%
# Imprime una muestra de datos para los mensajes

df_messages.head()


# %%
df_messages['message_date'] = pd.to_datetime(df_messages['message_date'], format='%Y-%m-%d')

total_duplicados = df_messages.duplicated().sum()
print("Total de registros duplicados:", total_duplicados)


# %%
df_messages.info()

# %% [markdown]
# ## Internet

# %%
# Imprime la información general/resumida sobre el DataFrame de internet

df_internet.info()

# %%
# Imprime una muestra de datos para el tráfico de internet

df_internet.head()


df_internet['session_date'] = pd.to_datetime(df_internet['session_date'], format='%Y-%m-%d')

total_duplicados = df_internet.duplicated().sum()
print("Total de registros duplicados:", total_duplicados)

# %%
df_internet.info()
df_internet.head()



# %% [markdown]
# ## Estudiar las condiciones de las tarifas

# %% [markdown]
# [Es sumamente importante entender cómo funcionan las tarifas, cómo se les cobra a los usuarios en función de su plan de suscripción.]

# %%
# Imprime las condiciones de la tarifa y asegúrate de que te quedan claras
df_plans.head()


# %% [markdown]
# ## Agregar datos por usuario

# %%
# Calcula el número de llamadas hechas por cada usuario al mes. Guarda el resultado.

df_calls['month'] = df_calls['call_date'].dt.month
calls_per_month = df_calls.groupby(['user_id', 'month']).size().reset_index(name='calls_count')
print(calls_per_month)



# %%
# Calcula la cantidad de minutos usados por cada usuario al mes. Guarda el resultado.

minutes_per_month = df_calls.groupby(['user_id', 'month'])['duration'].sum().reset_index(name='total_minutes')
print(minutes_per_month)

# %%
# Calcula el número de mensajes enviados por cada usuario al mes. Guarda el resultado.

df_messages['month'] = df_messages['message_date'].dt.month
messages_per_month = df_messages.groupby(['user_id', 'month']).size().reset_index(name='message_count')
print(messages_per_month)

# %%
# Calcula el volumen del tráfico de Internet usado por cada usuario al mes. Guarda el resultado.

df_internet['month'] = df_internet['session_date'].dt.month
internet_traffic_per_month = df_internet.groupby(['user_id', 'month'])['mb_used'].sum().reset_index(name='total_mb_used')
print(internet_traffic_per_month)

internet_traffic_per_month['total_gb_used'] = internet_traffic_per_month['total_mb_used'] / 1024
print(internet_traffic_per_month)
internet_traffic_per_month['total_gb_used'] = internet_traffic_per_month['total_gb_used'].apply(m.ceil)
print(internet_traffic_per_month)



# %%
# Fusiona los datos de llamadas, minutos, mensajes e Internet con base en user_id y month


merged_data = pd.merge(calls_per_month, minutes_per_month, on=['user_id', 'month'], how='outer')
merged_data = pd.merge(merged_data, messages_per_month, on=['user_id', 'month'], how='outer')
merged_data = pd.merge(merged_data, internet_traffic_per_month, on=['user_id', 'month'], how='outer')
merged_data = merged_data.fillna(0)
print(merged_data)


# %%
# Añade la información de la tarifa

merged_data = pd.merge(merged_data, df_users[['user_id', 'plan']], on='user_id', how='left')
print(merged_data)




# %%
final_merge= pd.merge(merged_data, df_plans, left_on='plan', right_on='plan_name', how='left')
final_merge= final_merge.drop(['plan_name'], axis=1)

print(final_merge)


# %%
# Calcula el ingreso mensual para cada usuario

final_merge['exceso_minutos'] = final_merge['total_minutes'] - final_merge['minutes_included']
final_merge['exceso_gb'] = final_merge['total_gb_used'] - final_merge['gb_per_month_included']
final_merge['exceso_sms'] = final_merge['message_count'] - final_merge['messages_included']


final_merge['exceso_minutos'] = final_merge['exceso_minutos'].apply(lambda x: max(x, 0))
final_merge['exceso_gb'] = final_merge['exceso_gb'].apply(lambda x: max(x, 0))
final_merge['exceso_sms'] = final_merge['exceso_sms'].apply(lambda x: max(x, 0))


costo_exceso_minutos = final_merge['exceso_minutos'] * final_merge['usd_per_minute']
costo_exceso_sms = final_merge['exceso_sms'] * final_merge['usd_per_message']
costo_exceso_gb= final_merge['exceso_gb'] * final_merge['usd_per_gb']

final_merge['tarifa_mensual'] = final_merge['usd_monthly_pay'] + costo_exceso_minutos + costo_exceso_gb + costo_exceso_sms

print(final_merge[['user_id', 'month', 'tarifa_mensual']])

# %% [markdown]
# ## Estudia el comportamiento de usuario

# %% [markdown]
# [Calcula algunas estadísticas descriptivas para los datos agregados y fusionados que nos sean útiles y que muestren un panorama general captado por los datos. Dibuja gráficos útiles para facilitar la comprensión. Dado que la tarea principal es comparar las tarifas y decidir cuál es más rentable, las estadísticas y gráficas deben calcularse por tarifa.]

# %% [markdown]
# ### Llamadas

# %%
# Compara la duración promedio de llamadas por cada plan y por cada mes. Traza un gráfico de barras para visualizarla.
average_duration_per_plan_month = merged_data.groupby(['plan', 'month'])['total_minutes'].mean().reset_index(name='average_duration')
print(average_duration_per_plan_month)

sns.set(style="whitegrid")

plt.figure(figsize=(12, 6))
barplot = sns.barplot(x='month', y='average_duration', hue='plan', data=average_duration_per_plan_month)
barplot.set_title('Promedio de Minutos por Llamada por Plan y Mes')
barplot.set_xlabel('Mes')
barplot.set_ylabel('Promedio de Minutos por Llamada')

barplot.legend(title='Plan', title_fontsize='12')

plt.show()

# %%
# Compara el número de minutos mensuales que necesitan los usuarios de cada plan. Traza un histograma.

plt.figure(figsize=(12, 6))

for plan, group in merged_data.groupby('plan'):
    plt.hist(group['total_minutes'], bins=20, alpha=0.7, label=plan, edgecolor='black')

plt.title('Distribución del Número de Minutos Mensuales por Plan')
plt.xlabel('Número de Minutos Mensuales')
plt.ylabel('Frecuencia')
plt.legend(title='Plan', title_fontsize='12')

plt.show()


# %%
# Calcula la media y la varianza de la duración mensual de llamadas.

duracion_mensual = merged_data.groupby('month')['total_minutes'].agg(['mean', 'var']).reset_index()
print(duracion_mensual)



# %%
# Traza un diagrama de caja para visualizar la distribución de la duración mensual de llamadas
sns.boxplot(duracion_mensual['mean']) 



# %% [markdown]
# ### Mensajes

# %%
# Comprara el número de mensajes que tienden a enviar cada mes los usuarios de cada plan

plt.figure(figsize=(12, 6))

promedio_mensajes_por_mes = merged_data.groupby(['plan', 'month'])['message_count'].mean().reset_index()

for plan, group in promedio_mensajes_por_mes.groupby('plan'):
    plt.bar(group['month'], group['message_count'], label=plan, alpha=0.7)

plt.title('Promedio de Mensajes por Mes y Plan')
plt.xlabel('Mes')
plt.ylabel('Promedio de Mensajes')
plt.legend(title='Plan', title_fontsize='12')
plt.xticks(range(1, 13)) 

plt.show()


# %%
plt.figure(figsize=(12, 6))

for plan, group in merged_data.groupby('plan'):
    plt.hist(group['message_count'], bins=20, alpha=0.7, label=plan, edgecolor='black')

plt.title('Distribución del Número de Mensajes Mensuales por Plan')
plt.xlabel('Número de Mensajes Mensuales')
plt.ylabel('Frecuencia')
plt.legend(title='Plan', title_fontsize='12')

plt.show()




# %%
mensajes_mensuales = merged_data.groupby('month')['message_count'].agg(['mean', 'var']).reset_index()

print(mensajes_mensuales)

sns.boxplot(mensajes_mensuales['mean']) 

# %% [markdown]
# En base a los graficos podemos ver que el comportamiento si varia en funcion del plan, los usuarios del plan ultimate utilizan mas mensajes.

# %% [markdown]
# ### Internet

# %%
# Compara la cantidad de tráfico de Internet consumido por usuarios por plan


plt.figure(figsize=(12, 6))

promedio_trafico_por_plan = merged_data.groupby('plan')['total_gb_used'].mean().reset_index()

plt.bar(promedio_trafico_por_plan['plan'], promedio_trafico_por_plan['total_gb_used'], alpha=0.7)

plt.title('Promedio de Tráfico de Internet Consumido por Plan')
plt.xlabel('Plan')
plt.ylabel('Promedio de Tráfico de Internet Consumido (GB)')
plt.xticks(rotation=45)

plt.show()


# %%

plt.figure(figsize=(12, 6))

# Agrupar por plan y mes y calcular el promedio de tráfico de Internet por mes
promedio_trafico_internet_por_mes = merged_data.groupby(['plan', 'month'])['total_gb_used'].mean().reset_index()

# Trama de barras para cada plan
for plan, group in promedio_trafico_internet_por_mes.groupby('plan'):
    plt.bar(group['month'], group['total_gb_used'], label=plan, alpha=0.7)

# Configuración del gráfico
plt.title('Promedio de Tráfico de Internet por Mes y Plan')
plt.xlabel('Mes')
plt.ylabel('Promedio de Tráfico de Internet (GB)')
plt.legend(title='Plan', title_fontsize='12')
plt.xticks(range(1, 13))  # Asegurarse de que los meses se muestren correctamente en el eje x

# Mostrar el gráfico
plt.show()


# %%
gb_mensuales = merged_data.groupby('month')['total_gb_used'].agg(['mean', 'var']).reset_index()

print(gb_mensuales)
sns.boxplot(gb_mensuales['mean']) 

# %% [markdown]
# [Elabora las conclusiones sobre cómo los usuarios tienden a consumir el tráfico de Internet. ¿Su comportamiento varía en función del plan?]
# 
# El consumo de internet varia en funcion del plan por los primeros 5 meses, a partir de junio los dos planes tienden a consumir casi el mismo numero de mb. Por razones desconocidas en enero casi no se utiliza el internet en ninguno de los dos planes resultando un dato atipico. 


# %% [markdown]
# ## Ingreso

# %%
# Agrupar por plan y mes y sumar los ingresos mensuales
ingresos_por_plan_mes = final_merge.groupby(['plan', 'month'])['tarifa_mensual'].sum().reset_index()

# Crear el gráfico de barras
plt.figure(figsize=(12, 6))

# Trama de barras para cada plan
for plan, group in ingresos_por_plan_mes.groupby('plan'):
    plt.bar(group['month'], group['tarifa_mensual'], label=plan, alpha=0.7)

# Configuración del gráfico
plt.title('Ingresos por Plan y Mes')
plt.xlabel('Mes')
plt.ylabel('Ingresos Mensuales')
plt.legend(title='Plan', title_fontsize='12')
plt.xticks(range(1, 13))  # Asegurarse de que los meses se muestren correctamente en el eje x

# Mostrar el gráfico
plt.show()


# %%
plt.figure(figsize=(12, 6))

ingresos_por_plan_mes = final_merge.groupby(['plan', 'month'])['tarifa_mensual'].sum().reset_index()

for plan, group in ingresos_por_plan_mes.groupby('plan'):
    plt.hist(group['tarifa_mensual'], bins=20, alpha=0.7, label=plan, edgecolor='black')

plt.title('Distribución del Número de Ingresos Mensuales por Plan')
plt.xlabel('Ingresos Mensuales')
plt.ylabel('Frecuencia')
plt.legend(title='Plan', title_fontsize='12')

plt.show()


# %%

ingresos_mensuales = final_merge.groupby('month')['tarifa_mensual'].agg(['mean', 'var']).reset_index()

print(ingresos_mensuales)
sns.boxplot(ingresos_mensuales['mean']) 

# %% [markdown]
# A pesas de que el plan ultimate es mas caro, el plan surf genera mayores ingresos

# %% [markdown]
# ## Prueba las hipótesis estadísticas

# %% [markdown]
# [Elabora las hipótesis nula y alternativa, escoge la prueba estadística, determina el valor alfa.]
# 
# Hipótesis nula: No hay diferencia significativa en los ingresos promedio entre los usuarios de los planes Ultimate y Surf.
# 
# Hipótesis alternativa: Hay una diferencia significativa en los ingresos promedio entre los usuarios de los planes Ultimate y Surf.

# %%
# Prueba las hipótesis

ingresos_ultimate = final_merge[final_merge['plan'] == 'ultimate']['tarifa_mensual']
ingresos_surf = final_merge[final_merge['plan'] == 'surf']['tarifa_mensual']

alpha = 0.05

results = ttest_ind(ingresos_ultimate, ingresos_surf,equal_var=False)

print("Valor p:", results.pvalue)

if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula")
else:
    print("No podemos rechazar la hipótesis nula")


# %% [markdown]
# Rechazamos la hipotesis nula en ambos casos por lo que hay una diferencia significativa en los ingresos promedio concluyendo que un plan esta dando mas ingresos que otro, en este caso concreto el plan surf da mas ingresos


# %% [markdown]
# [Prueba la hipótesis de que el ingreso promedio de los usuarios del área NY-NJ es diferente al de los usuarios de otras regiones.]

# %% [markdown]
# [Elabora las hipótesis nula y alternativa, escoge la prueba estadística, determina el valor alfa.]
# 
# Hipótesis nula : No hay diferencia significativa en el ingreso promedio entre los usuarios del área NY-NJ y los usuarios de otras regiones.
# 
# Hipótesis alternativa: Hay una diferencia significativa en el ingreso promedio entre los usuarios del área NY-NJ y los usuarios de otras regiones.

# %%
# Prueba las hipótesis

ingresos_ciudad = pd.merge(final_merge, df_users[['user_id', 'city']], on='user_id', how='left')

ingresos_ny_nj = ingresos_ciudad[ingresos_ciudad['city'] == 'New York-Newark-Jersey City, NY-NJ-PA MSA']['tarifa_mensual']
ingresos_otras_regiones = ingresos_ciudad[ingresos_ciudad['city'] != 'New York-Newark-Jersey City, NY-NJ-PA MSA']['tarifa_mensual']

alpha = 0.05

results = ttest_ind(ingresos_ny_nj, ingresos_otras_regiones,equal_var=False)

print("Valor p:", results.pvalue)

if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula")
else:
    print("No podemos rechazar la hipótesis nula")

# %% [markdown]
# Rechazamos la hipotesis nula en ambos casos por lo que hay una diferencia significativa en los ingresos promedio concluyendo que la zona NY-NJ da mas ingresos que otras zonas.


# %% [markdown]
# ## Conclusión general
# %% [markdown]
# -En un inicio siempre es importante analizar los data frames y sus contenidos ya que podrian pareces que no tienen ningun error significativo a la hora del procesamiento, sin embargo hay cosas que pueden mejorarse como en este caso al pasar las fechas a date type en lugar.
# -Se tuvieron que fucionar bastantes data frame ya que no todos contienen la informacion requerida para realizar ciertas tareas.
# -A la hora de hacer las hipotesis es importante seleccionar bien la prueba ya que en este caso una prueba de una sola cola no hubiera funcionado.
# -A pesar de contar con dos planes distintos la mayoria de personas tienden a tener promedios similares a la hora de realizar llamadas, sin embargo a la hora de mensajes e internet podemos comenzar a ver diferencias significativas de consumo, por lo que las personas de ventas pueden dirigir sus enfoques a la hora de ofrecer el plan ultimate en estas dos categorias, sin embargo es tambien notorio que el plan surf genera mayores ingresos que el plan, por lo que dependerian de las necesidades de la empresa.


# %%



