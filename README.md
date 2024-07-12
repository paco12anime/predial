# Sistema de Predial

Sistema de Predial es una aplicación de escritorio desarrollada con PyQt5 y SQLite para gestionar el registro de usuarios, inicio de sesión, consulta de adeudos y proceso de pago.

## Características

- Registro de usuarios
- Inicio de sesión
- Consulta de adeudos
- Proceso de pago

## Requisitos

- Python 3.x
- PyQt5
- SQLite3

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/paco12anime/sistema-de-predial.git
    cd sistema-de-predial
    ```

2. Crea un entorno virtual (opcional pero recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Crea la base de datos y las tablas necesarias:

    ```bash
    python create_db.py
    ```

## Uso

1. Ejecuta la aplicación:

    ```bash
    python main.py
    ```

2. Se abrirá la ventana principal donde puedes registrarte o iniciar sesión.

## Estructura del Proyecto

- `main.py`: Archivo principal que contiene la lógica de la aplicación.
- `create_db.py`: Script para crear la base de datos y las tablas necesarias.
- `requirements.txt`: Archivo de dependencias del proyecto.
- `usuarios.db`: Archivo de base de datos SQLite.

## Licencia

Este proyecto está licenciado bajo la Licencia GPLv3. Consulta el archivo `LICENSE` para obtener más detalles.
