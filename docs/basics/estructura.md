---
icon: folder-tree
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

# Estructura del proyecto

* `assets/`: Almacena todos los recursos visuales y de audio.
  * `fonts/`: Contiene las fuentes tipográficas utilizadas en la interfaz gráfica.
  * `icons/`: Guarda los logos e iconos de la aplicación.
  * `sound/`: Contiene los archivos de sonido que se reproduce al detectar un gesto.
* `controller/`: Contiene la lógica de control del cursor del mouse.&#x20;
  * CursorInterface.py:
  * CursorTracker.py:
  * AdaptiveCursor.py:
* `hooks/`: Contiene "hooks" para el empaquetado de la aplicación con PyInstaller.&#x20;
  * hook-mediapipe.py:&#x20;
* `model/`: Contiene los modelos de machine learning pre-entrenados.&#x20;
  * `hand/`: Almacena el modelo de _mediapipe_ para la detección de los puntos de referencia de la mano. &#x20;
  * `gesture/`: Contiene los modelos (.tflite) entrenados para clasificar los gestos de la mano.&#x20;
  * &#x20;ConvertModel.py:
* `training/`: Scripts y datos para entrenar los modelos de reconocimiento de gestos.&#x20;
  * FormatData.py:&#x20;
  * TestModel.py:
* `/` (Directorio Raíz):&#x20;
  * .gitattributes:
  * .gitignore:
  * .lfsconfig:
  * .python-version:
  * DrawHand.py:
  * HandTracker.py:
  * LICENCE:&#x20;
  * README.md:
  * ResourcePaths.py:
  * main.py:
  * main.spec:
  * requirements.txt:
