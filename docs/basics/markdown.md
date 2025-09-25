---
icon: list-check
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Dependencias

A continuación todas las dependencias utilizadas en el desarrollo de Visionic.

### Dependencias de producción

```python
mediapipe==0.10.21
opencv-python==4.11.0.86
autopy==4.0.1
numpy==1.26.4
tensorflow==2.19.0
PyAutoGUI==0.9.54
playsound==1.3.0
dearpygui==2.0.0
```

* **Lenguaje:** Python 3.12.8
  * **Librerías utilizadas:**
    * [Mediapipe](https://pypi.org/project/mediapipe/): configuración del modelo de detección de manos.
    * [OpenCV](https://pypi.org/project/opencv-python/): captura, visualización y conversión de formato de frames de video.
    * [Autopy](https://pypi.org/project/autopy/): control de las operaciones básicas del cursor (desplazamiento, click derecho e izquierdo).
    * [Numpy](https://pypi.org/project/numpy/): formato correcto de los datos para la interpretación por parte del modelo entrenado.
    * [Tensorflow](https://pypi.org/project/tensorflow/): cargar y ejecutar los modelos entrenados.
    * [Pyautogui](https://pypi.org/project/PyAutoGUI/): control de la operación del cursor (scroll).
    * [Playsound](https://pypi.org/project/playsound/): importación de audio personalizado para detección del gesto.
    * [Dearpygui](https://pypi.org/project/dearpygui/): creación de interfaz gráfica de configuración.
  * **Módulos:**&#x20;
    * [Threading](https://docs.python.org/3.12/library/threading.html): ejecución de los gestos en hilos de procesamiento.
    * [Time](https://docs.python.org/3.12/library/time.html): control de tiempo entre procesamiento de frames.
    * [Math](https://docs.python.org/3.12/library/math.html): cálculo de distancia euclidiana para la normalización de datos de entrenamiento.

### Dependencias de desarrollo

* **Lenguaje:** Python 3.12.8
  * **Módulos:**&#x20;
    * [CSV](https://docs.python.org/3.12/library/csv.html): importación de archivo para la prueba del modelo entrenado en formato csv.

### Dependencias de entrenamiento

Dependencias utilizadas para la creación y entrenamiento de los modelos de IA.

**Lenguaje:** Python 3.12.8

* **Librerías utilizadas:**
  * [Pandas](https://pypi.org/project/pandas/): leer el archivo csv y agrupar los datos por secuencia.
  * [Numpy](https://pypi.org/project/numpy/): apilar la secuencia en matrices.
  * [Sklearn](https://pypi.org/project/scikit-learn/): división de datos (entrenamiento y prueba) para la construcción de la red neuronal.
  * [Tensorflow](https://pypi.org/project/tensorflow/)(keras): construcción, configuración y entrenamiento de la red neuronal.
