# Taller Smart Robots Challenge  
## Ingeniería en Robótica y Sistemas Digitales (IRS)  

### Objetivo  
<p align="justify"> Controlar un carrito usando señas con las manos. Para esto es necesario crear un modelo de clasificación de imágenes para diferenciar las señas que representarán los movimientos del carrito (Adelante, Atras, Izquierda, Derecha y Parar). Este modelo se usará en Python, el cual se comunica por medio de Bluetooth a un Arduino que controla los motores del carrito para hacer los movimientos que se obtienen de un video en vivo haciendo las señas con las que se entreno el modelo. </p>

### Pasos para controlar el carrito  
#### 1. Teachable Machine (Aquí se crea el modelo de clasificación de imágenes)  
 a) Entrar a <a href="https://teachablemachine.withgoogle.com/train/image" target="_blank">Teachable Machine</a>  
 b) Crear y renombrar 5 clases (Adelante, Atras, Izquierda, Derecha y Parar)  
 c) Usar la webcam para tomar fotos de cada clase. Se recomienda tomar al menos 150 imágenes por clase, así como mover la mano haciendo la misma seña.  *Importante: se clasifica todo el cuadrado, por lo que el fondo puede afectar.*  
 d) Dar a train model para empezar el entrenamiento del modelo. Puede tardar en empezar, una vez que lo haga aparecera una barra de progreso. No se  recomienda mover las opciones avanzadas.  
 d) Una vez terminado el entrenamiento se puede probar el modelo con la webcam, aparecerán unas barras que se llenan de acuerdo a la seña que se cree  que se esta haciendo.  
 e) Exportar el modelo. Ir a la opción del medio (Tensorflow) y descargarlo en Keras.  
 f) Descomprimir el archivo descargado. Importante saber donde se guardaron los archivos resultantes.  
 
#### 2. Python (Aquí se hace la clasificación para mandar los movimientos a Arduino)  
 a) Descargar la última versión de <a href="https://www.python.org/downloads/" target="_blank"> Python</a>. Asegurarse de marcar la opción "Add Python to  Path" antes de iniciar la instalación y la opción "Disable path length limit" al finalizar la instalación.  
 b) Abrir PowerShell en Windows.  
 c) Descargar las librerías tkinter, pillow, opencv, tensorflow, numpy y pyserial. [Instrucciones al final](#librerias-necesarias)  
 d) Ejecutar el programa [SmartRobotsChallenge.py](SmartRobotsChallenge.py) con el comando "python SmartRobotsChallenge.py"  
 e) Cargar el archivo de labels generado con Teachable Machine  
 f) Cargar el archivo del modelo generado con Teachable Machine  
 g) Enceder la cámara. Se puede ver la predicción de la seña a la derecha junto con el porcentaje de la seguridad de que sea esa seña.  
 h) La tolerancia se puede ajustar para que la seña se mande a Arduino solo si es su porcentaje es mayor al de la tolerancia (Se muestra en verde  cuando si se manda y en rojo cuando no).  


#### 3. Arduino (Control de los motores para el movimiento del carrito)  
 a) Descargar <a href="https://www.arduino.cc/en/software" target="_blank">Arduino IDE 1.8.19</a>  
 b) Abrir el archivo [SmartRobotsChallenge.ino](SmartRobotsChallenge/SmartRobotsChallenge.ino)  
 c) Editar el final del código siguiendo el ejemplo. Usar condiciones if comparando la variable "opcion" con el número que aparece en el archivo labels.txt y usar la función del movimiento que corresponda, entre parentesis se pone la velocidad de 0 a 255 excepto en la función Parar().  
 d) Por ejemplo si en el archivo labels dice "2 Izquierda" entonces se debe poner if (option == '2'){Izquierda(255);}  
 e) En Herramientas seleccionar la tarjeta "Arduino UNO" y el puerto correspondiente.
 f) Compilar y subir programa al Arduino.  
 
#### 4. Probar todo junto  
 En el programa de Python:  
 a) Refrescar para mostrar las posibles conexiones.  
 b) Seleccionar el puerto que corresponde al Bluetooth (Inalámbrico) o al Arduino (Alámbrico) y dar a Conectar.  
 c) Los movimientos se empezarán a mandar al Arduino.  
 d) El carrito se moverá de acuerdo a la seña que se haga.  

### Librerias necesarias  
python -m pip install tk  
python -m pip install pillow  
python -m pip install opencv-python  
python -m pip install tensorflow  
python -m pip install numpy  
python -m pip install pyserial  

*En caso de no funcionar intentar con "py" en lugar de "python"*
