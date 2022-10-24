# Taller Smart Robots Challenge  
## Ingeniería en Robótica y Sistemas Digitales (IRS)  

### Objetivo  
<p align="justify"> Controlar un carrito usando señas con las manos. Para esto es necesario crear un modelo de clasificación de imágenes para diferenciar las señas que
representarán los movimientos del carrito (Adelante, Atras, Izquierda, Derecha y Parar). Este modelo se usará en Python, el cual se comunica por
medio de Bluetooth a un Arduino que controla los motores del carrito para hacer los movimientos que se obtienen de un video en vivo haciendo las señas
con las que se entreno el modelo. </p>

### Pasos para controlar el carrito  
#### 1. Teachable Machine (Aquí se crea el modelo de clasificación de imágenes)  
 a) Entrar a <a href="https://teachablemachine.withgoogle.com/train/image" target="_blank">Teachable Machine</a>  
 b) Crear y renombrar 5 clases (Adelante, Atras, Izquierda, Derecha y Parar)  
 c) Usar la webcam para tomar fotos de cada clase. Se recomienda tomar al menos 150 imágenes por clase, así como mover la mano haciendo la misma seña.
 Importante: se clasifica todo el cuadrado, por lo que el fondo puede afectar.  
 d) Dar a train model para empezar el entrenamiento del modelo. Puede tardar en empezar, una vez que lo haga aparecera una barra de progreso. No se
 recomienda mover las opciones avanzadas.  
 d) Una vez terminado el entrenamiento se puede probar el modelo con la webcam, aparecerán unas barras que se llenan de acuerdo a la seña que se cree
 que se esta haciendo.  
 e) Exportar el modelo. Ir a la opción del medio (Tensorflow) y descargarlo en Keras.  
 f) Descomprimir el archivo descargado. Importante saber donde se guardaron los archivos resultantes.  
 
#### 2. Python (Aquí se hace la clasificación para mandar los movimientos a Arduino)  
  a) Descargar la última versión de <a href="https://www.python.org/downloads/" target="_blank"> Python</a>. Asegurarse de marcar la opción "Add Python to
  Path" antes de iniciar la instalación y la opción "Disable path length limit" al finalizar la instalación.  
  b) Descargar las librerías tkinter, pillow, opencv, tensorflow, numpy, pyserial. [Instrucciones al final](#librerias-necesarias)  
  
  


### Librerias necesarias  
pip install tk  
pip install pillow  
pip install opencv-python  
pip install tensorflow  
pip install numpy  
pip install pyserial  
