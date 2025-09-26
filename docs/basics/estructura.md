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
  * [CursorInterface.py](../../controller/CursorInterface.py): interfaz que permite acceder fácilmente a las distintas implementaciones de control de cursor.
  * [CursorTracker.py](../../controller/CursorTracker.py): primera implementación para el suavizado del desplazamiento del cursor.
  * [AdaptiveCursor.py](../../controller/AdaptiveCursor.py): implementación final avanzada para el suavizado del desplazamiento del cursor.
* `hooks/`: Contiene "hooks" para el empaquetado de la aplicación con _PyInstaller_.&#x20;
  * [hook-mediapipe.py](../../hooks/hook-mediapipe.py): un script que asegurar que todos los archivos necesarios de la biblioteca _Mediapipe_ se incluyan correctamente cuando se crea el ejecutable de la aplicación.
* `model/`: Contiene los modelos de machine learning pre-entrenados.&#x20;
  * `hand/`: Almacena el modelo de _Mediapipe_ para la detección de los puntos de referencia de la mano.&#x20;
  * `gesture/`: Contiene los modelos (.tflite) entrenados para clasificar los gestos de la mano.&#x20;
    * **gesture\_lstm.tflite**: modelo entrenado para detectar un único gesto.
    * **gesture\_lstm\_multiclass.tflite**: modelo multi-clase entrenado para detectar 3 gestos.
* `training/`: Scripts y datos para entrenar los modelos de reconocimiento de gestos.&#x20;
  * [FormatData.py](../../training/FormatData.py):  funcionalidades de normalización de las coordenadas de la mano para el entrenamiento como la detección del los gestos.
  * [TestModel.py](../../training/TestModel.py): script para evaluar el rendimiento de los modelos entrenados.
* `/` (Directorio Raíz):&#x20;
  * [.gitattributes](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/.gitattributes): indicar que los archivos grandes o binarios(modelos entrenados) deben ser gestionados por Git LFS.
  * [.gitignore](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/.gitignore): archivos ignorados por el control de versiones de git.
  * [.lfsconfig](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/.lfsconfig): define la configuración de Git LFS para el repositorio.
  * [.python-version](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/.python-version): versión de python utilizada en el proyecto.
  * [DrawHand.py](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/DrawHand.py): funcionalidades para dibujar puntos de referencia de la mano.
  * [HandTracker.py](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/HandTracker.py): toda la lógica central de el software para el seguimiento de la mano y detección de gestos.
  * [LICENCE](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/LICENCE): licencia del software.
  * [README.md](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/README.md): documentación resumida del proyecto.
  * [ResourcePaths.py](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/ResourcePaths.py): obtiene las rutas absolutas de recursos para que el programa funcione correctamente tanto en desarrollo como empaquetado con _PyInstaller_.
  * [main.py](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/main.py): punto de entrada principal del software.
  * [main.spec](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/main.spec): archivo de especificación para _PyInstaller_.
  * [requirements.txt](https://github.com/MartinMosqueira/TIFVirtualMouse/blob/0fc54c7fe0dcbeb25bf05408656eda4e8c798c06/requirements.txt): dependencias de producción del proyecto.
