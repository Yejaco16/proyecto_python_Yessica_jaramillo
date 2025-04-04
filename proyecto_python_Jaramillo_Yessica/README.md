# Sistema de Gestión de Envíos (CLI)

Este script de Python implementa un sistema de gestión de envíos a través de una interfaz de línea de comandos (CLI). Permite registrar clientes, registrar envíos, realizar seguimiento, generar informes básicos y gestionar una cuenta de administrador segura.

## Contenido

* [Dependencias](#dependencias)
* [Configuración Inicial (Primer Inicio)](#configuración-inicial-primer-inicio)
* [Uso](#uso)
    * [Inicio de Sesión del Administrador](#inicio-de-sesión-del-administrador)
    * [Recuperación de Acceso del Administrador](#recuperación-de-acceso-del-administrador)
    * [Menú Principal](#menú-principal)
* [Archivos Generados](#archivos-generados)

## Dependencias

Este proyecto utiliza las siguientes librerías externas:

* **dotenv:** Para cargar variables de entorno desde un archivo `.env`.
* **bcrypt:** Para el hashing seguro de contraseñas.

Se recomienda utilizar un entorno virtual de Python para gestionar las dependencias del proyecto de forma aislada.

**Pasos para configurar el entorno virtual:**

1.  **Crear el entorno virtual:**

    ```bash
    python -m venv venv
    ```

2.  **Activar el entorno virtual:**

    * **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **Windows (CMD):**
        ```bash
        .\venv\Scripts\activate.bat
        ```
    * **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\activate.ps1
        ```

3.  **Instalar las dependencias:**

    Puedes instalar las dependencias directamente con `pip`:

    ```bash
    pip install dotenv bcrypt
    ```

    O, si tienes un archivo `requirements.txt` (que puedes generar con `pip freeze > requirements.txt`), puedes usar:

    ```bash
    pip install -r requirements.txt
    ```

## Configuración Inicial (Primer Inicio)

Al ejecutar el script por primera vez, se realizará la configuración inicial de la cuenta de administrador:

1.  Se detectará la ausencia del archivo `.admin_credentials`.
2.  Se solicitará al administrador que ingrese un nombre de usuario y una contraseña para la cuenta administrativa.
3.  Se generará una **clave única de recuperación** basada en las credenciales ingresadas, utilizando la librería `bcrypt` para seguridad.
4.  **¡Importante!** Esta clave única se mostrará una sola vez. **Guárdala en un lugar seguro**, ya que será la única forma de recuperar el acceso a la cuenta de administrador en caso de olvidar la contraseña.
5.  El nombre de usuario y el hash seguro de la contraseña y la clave única de recuperación se almacenarán encriptados en el archivo `.admin_credentials`.

## Uso

Una vez configurada la cuenta de administrador, al ejecutar el script se presentará un menú de inicio de sesión.

### Inicio de Sesión del Administrador

1.  Ingrese el nombre de usuario y la contraseña de la cuenta de administrador.
2.  El sistema verificará las credenciales comparando la contraseña ingresada con el hash almacenado de forma segura.
3.  Si las credenciales son correctas, se accederá al menú principal de la aplicación.

### Recuperación de Acceso del Administrador

1.  En el menú de inicio de sesión, seleccione la opción para recuperar el acceso (generalmente preguntando si olvidó su contraseña).
2.  Se le solicitará que ingrese la **clave única de recuperación** que se generó durante la configuración inicial.
3.  El sistema verificará la clave ingresada con el hash de la clave única almacenado.
4.  Si la clave es válida, se le permitirá establecer una **nueva contraseña** para la cuenta de administrador.
5.  Al establecer una nueva contraseña, se generará una **nueva clave única de recuperación**, la cual deberá guardar nuevamente de forma segura.

### Menú Principal

Una vez que el administrador ha iniciado sesión, tendrá acceso a las siguientes funcionalidades:

1.  **Registrar Cliente:** Permite ingresar la información de un nuevo cliente.
2.  **Registrar Envío:** Permite registrar un nuevo envío, asociándolo a un remitente existente.
3.  **Seguimiento de Envío:** Permite buscar un envío por su número de guía y mostrar su estado.
4.  **Generar Informe de Volumen:** Muestra la cantidad total de envíos registrados.
5.  **Cerrar Sesión:** Finaliza la sesión del administrador y vuelve al menú de inicio de sesión.

## Archivos Generados

Durante la ejecución del script, se pueden generar los siguientes archivos:

* `.admin_credentials`: Archivo (oculto en sistemas Unix) que almacena de forma segura la información de la cuenta de administrador (nombre de usuario y hashes de contraseña y clave única de recuperación). **No modificar este archivo manualmente.**
* `data.json`: Archivo que almacena la información de los clientes y los envíos en formato JSON.
* `sistema_envios.log.json`: Archivo que guarda los logs de la aplicación en formato JSON para seguimiento y depuración.
