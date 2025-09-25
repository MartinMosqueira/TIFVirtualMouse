---
icon: download
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

# Inicio rápido

Los siguientes pasos son para instalar Visionic en su ordenador.

### Modo desarrollo

{% hint style="info" %}
Asegurarse de tener instalado en su ordenador Git y Python 3.12.8
{% endhint %}

1. Clonar el repositorio:

```sh
git clone https://github.com/MartinMosqueira/TIFVirtualMouse.git
cd TIFVirtualMouse
```

2. Crear y activar un entorno virtual:

```sh
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias dentro del entorno:

```sh
pip install -r requirements.txt
```

4. Ejecutar aplicación:

```sh
python main.py
```

### Modo usuario

