# Proyecto-4
Descripción del proyecto
Trabajaremos como analista para el operador de telecomunicaciones Megaline. La empresa ofrece a sus clientes dos tarifas de prepago, Surf y Ultimate. El departamento comercial quiere saber cuál de los planes genera más ingresos para poder ajustar el presupuesto de publicidad.

Vas a realizar un análisis preliminar de las tarifas basado en una selección de clientes relativamente pequeña. Tendrás los datos de 500 clientes de Megaline: quiénes son los clientes, de dónde son, qué tarifa usan, así como la cantidad de llamadas que hicieron y los mensajes de texto que enviaron en 2018. Tu trabajo es analizar el comportamiento de los clientes y determinar qué tarifa de prepago genera más ingresos. Más adelante, encontrarás en las instrucciones del proyecto cuáles son exactamente los aspectos del comportamiento de los clientes que debes analizar. Determinar qué plan, en promedio, aporta más ingresos es una cuestión que se abordará mediante pruebas estadísticas. Más adelante encontrarás más información al respecto en la sección de instrucciones del proyecto.
A continuación encontrarás las rutas de los archivos que hay que leer, junto con los enlaces para descargarlos si es necesario:

/datasets/megaline_calls.csv Descargar el dataset

/datasets/megaline_internet.csv Descargar el dataset

/datasets/megaline_messages.csv Descargar el dataset

/datasets/megaline_plans.csv Descargar el dataset

/datasets/megaline_users.csv Descargar el dataset

Paso 2. Prepara los datos

Convierte los datos en los tipos necesarios.
Encuentra y elimina errores en los datos. Asegúrate de explicar qué errores encontraste y cómo los eliminaste.
Para cada usuario, busca:

El número de llamadas realizadas y minutos utilizados al mes.
La cantidad de los SMS enviados por mes.
El volumen de datos por mes.
Los ingresos mensuales por cada usuario. Para ello, necesitas:
Restar el límite del paquete gratuito del número total de llamadas, mensajes de texto y datos.
Multiplicar el resultado por el valor de la tarifa de llamadas.
Añadir la cuota mensual en función del plan de llamadas.
Paso 3. Analiza los datos

Describe el comportamiento de la clientela:

Encuentra los minutos, SMS y volumen de datos que requieren los usuarios de cada tarifa por mes.
Calcula la media, la varianza y la desviación estándar.
Traza histogramas. Describe las distribuciones.
Paso 4. Prueba las hipótesis

El ingreso promedio de los usuarios de las tarifas Ultimate y Surf difiere.
El ingreso promedio de los usuarios en el área de estados Nueva York-Nueva Jersey es diferente al de los usuarios de otras regiones.
Tú decides qué valor alfa usar. Además, tienes que explicar:

Cómo formulaste las hipótesis nula y alternativa.
Qué criterio utilizaste para probar las hipótesis y por qué.
Paso 5. Escribe una conclusión general

Formato: Completa todas las tareas en un Jupyter Notebook. Almacena todo el código en las celdas code y las explicaciones de texto en las celdas markdown. Añade títulos y el formato adecuado si es necesario.