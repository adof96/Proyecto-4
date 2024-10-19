# Proyecto-4
## Herramientas usadas
-Python
-Pandas 
-Matplotlib 
-Seaborn
-Numpy
-Scipy
## Descripción del proyecto
Trabajaremos como analista para el operador de telecomunicaciones Megaline. La empresa ofrece a sus clientes dos tarifas de prepago, Surf y Ultimate. El departamento comercial quiere saber cuál de los planes genera más ingresos para poder ajustar el presupuesto de publicidad.

Vamos a realizar un análisis preliminar de las tarifas basado en una selección de clientes relativamente pequeña. Tenemos los datos de 500 clientes de Megaline: quiénes son los clientes, de dónde son, qué tarifa usan, así como la cantidad de llamadas que hicieron y los mensajes de texto que enviaron en 2018. Nuestro trabajo es analizar el comportamiento de los clientes y determinar qué tarifa de prepago genera más ingresos. Determinar qué plan, en promedio, aporta más ingresos es una cuestión que se abordará mediante pruebas estadísticas.

### Paso 1 Abrir el archivo de datos y estudia la información general


### Paso 2. Preparar los datos

Conversion de los datos en los tipos necesarios.
Encontrar y elimina errores en los datos.
Para cada usuario, buscaremos:

-El número de llamadas realizadas y minutos utilizados al mes.
-La cantidad de los SMS enviados por mes.
-El volumen de datos por mes.
-Los ingresos mensuales por cada usuario. 

Para ello, necesitamos:

-Restar el límite del paquete gratuito del número total de llamadas, mensajes de texto y datos.
-Multiplicar el resultado por el valor de la tarifa de llamadas.
-Añadir la cuota mensual en función del plan de llamadas.

### Paso 3. Analizar los datos

Describiremos el comportamiento de la clientela:

-Encuentraremos los minutos, SMS y volumen de datos que requieren los usuarios de cada tarifa por mes.
-Calcularemos la media, la varianza y la desviación estándar.
-Trazaremos histogramas. Describiremos las distribuciones.

### Paso 4. Prueba las hipótesis

-El ingreso promedio de los usuarios de las tarifas Ultimate y Surf difiere.
-El ingreso promedio de los usuarios en el área de estados Nueva York-Nueva Jersey es diferente al de los usuarios de otras regiones.
Además,explicaremos:

Cómo formulamos las hipótesis nula y alternativa.
Qué criterio utilizamos para probar las hipótesis y por qué.

### Paso 5. Escribiremos una conclusión general