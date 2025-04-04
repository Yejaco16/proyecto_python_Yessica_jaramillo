import json
import datetime
import random
import os
from dotenv import load_dotenv
import bcrypt

DATA = "data.json"
CREDENCIALES = ".credenciales_admin"
USUARIO_ADMIN = "USUARIO_ADMIN"
CLAVE_ADMIN = "CLAVE_ADMIN"
CLAVE_RECUPERACION = "CLAVE_RECUPERACION"

#######################SECCION GESTION############################## 
def cargar_datos(): 
    try:
        with open(DATA, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"No se econtró '{DATA}'.")
        return {"clientes": [], "envios": []}

def guardar_datos(data):
    with open(DATA, "w") as archivo:
        json.dump(data, archivo, indent=4)

def registrar_cliente(data, nombres, apellidos, identificacion, tipo_identificacion, direccion, telefono_fijo, celular, barrio):
    if buscar_cliente(data, identificacion):
        print(f"Advertencia: Ya existe un cliente con indentificado con '{identificacion}'.")
        return data

    nuevo_cliente = {
        "nombres": nombres,
        "apellidos": apellidos,
        "identificacion": identificacion,
        "tipo_identificacion": tipo_identificacion,
        "direccion": direccion,
        "telefono_fijo": telefono_fijo,
        "celular": celular,
        "barrio": barrio
    }
    data["clientes"].append(nuevo_cliente)
    guardar_datos(data)
    return data

def buscar_cliente(data, identificacion):
    for cliente in data["clientes"]:
        if cliente["identificacion"] == identificacion:
            return cliente
    return None

def generar_numero_guia():
    return str(random.randint(1000000000, 9999999999))

def registrar_envio(data, destinatario_nombre, destinatario_direccion, destinatario_telefono, destinatario_ciudad, destinatario_barrio, remitente_identificacion, estado):
    remitente = buscar_cliente(data, remitente_identificacion)
    if remitente:
        fecha_actual = datetime.datetime.now()
        nuevo_envio = {
            "numero_guia": generar_numero_guia(),
            "fecha_envio": fecha_actual.strftime("%Y-%m-%d"),
            "hora_envio": fecha_actual.strftime("%H:%M:%S"),
            "destinatario": {
                "nombre": destinatario_nombre,
                "direccion": destinatario_direccion,
                "telefono": destinatario_telefono,
                "ciudad": destinatario_ciudad,
                "barrio": destinatario_barrio
            },
            "remitente_identificacion": remitente_identificacion,
            "estado": estado
        }
    
        data["envios"].append(nuevo_envio)
        guardar_datos(data)
        return data
    else:
        print("No existe remitente registrado con identificación '{remitente_identificacion}'.")
        return None

def seguimiento_envio(data, numero_guia):
    for envio in data["envios"]:
        if envio["numero_guia"] == numero_guia:
            print(f"--- Seguimiento del Envío ---")
            print(f"Número de Guía: {envio['numero_guia']}")
            print(f"Fecha de Envío: {envio['fecha_envio']}")
            print(f"Hora de Envío: {envio['hora_envio']}")
            print(f"Estado: {envio['estado']}")
            return
    print("Envío no encontrado.")

def generar_informe_volumen(data):
    print(f"Volumen total de envíos: {len(data['envios'])}")

#################################SECCION ADMIN####################################
def generar_clave_recuperacion(usuario, contrasena):
    frase_semilla = f"{usuario}-{contrasena}-unique-salt"
    semilla_encriptada = bcrypt.hashpw(frase_semilla.encode('utf-8'), bcrypt.gensalt())
    return semilla_encriptada.decode('utf-8')

def encriptar_contrasena(contrasena):
    contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
    return contrasena_hash

def verificar_contrasena(contrasena, contrasena_encriptada):
    return bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_encriptada)

def cargar_credenciales_admin():
    load_dotenv(CREDENCIALES)
    usuario = os.getenv(USUARIO_ADMIN)
    contrasena_encriptada = os.getenv(CLAVE_ADMIN)
    clave_recuperacion = os.getenv(CLAVE_RECUPERACION)
    return usuario, contrasena_encriptada, clave_recuperacion

def guardar_credenciales_admin(usuario, contrasena_encriptada, clave_recuperacion):
    with open(CREDENCIALES, "w") as f:
        f.write(f"{USUARIO_ADMIN}={usuario}\n")
        f.write(f"{CLAVE_ADMIN}={contrasena_encriptada.decode('utf-8')}\n")
        f.write(f"{CLAVE_RECUPERACION}={clave_recuperacion.decode('utf-8')}\n")

def verificar_clave_recuperacion(clave_ingresada, clave_recuperacion):
    return bcrypt.checkpw(clave_ingresada.encode('utf-8'), clave_recuperacion)

def crear_cuenta_admin_inicial():
    if not os.path.exists(CREDENCIALES):
        print("No se encontraron credenciales de administrador.")
        usuario = input("Ingrese el nombre de usuario para el administrador inicial: ")
        contrasena = input("Ingrese la contraseña para el administrador inicial: ")
        confirmar_contrasena = input("Confirme la contraseña: ")
        if contrasena == confirmar_contrasena:
            contrasena_encriptada = encriptar_contrasena(contrasena)
            clave_recuperacion = generar_clave_recuperacion(usuario, contrasena)
            clave_recuperacion_encriptada = encriptar_contrasena(clave_recuperacion)
            guardar_credenciales_admin(usuario, contrasena_encriptada, clave_recuperacion_encriptada)
            print("\n¡Importante! Guarda esta clave única de recuperación en un lugar seguro:")
            print(f"Clave Única de Recuperación: {clave_recuperacion}")
            print("Esta clave permitirá recuperar el acceso a la cuenta de administrador en caso de olvidar la contraseña.")
            input("\nPresiona Enter una vez que se haya guardado la clave.")
            print("Cuenta de administrador inicial creada exitosamente.")
        else:
            print("Las contraseñas no coinciden. No se creó la cuenta de administrador.")
        return True
    return False

def login_administrador():
    usuario, contrasena_encriptada, _ = cargar_credenciales_admin()
    if not usuario:
        print("No se ha configurado una cuenta de administrador.")
        return False

    usuario_input = input("Nombre de usuario del administrador: ")
    contrasena_input = input("Contraseña del administrador: ")

    if usuario_input == usuario and contrasena_encriptada and verificar_contrasena(contrasena_input, contrasena_encriptada.encode('utf-8')):
        print("Acceso concedido.")
        return True
    else:
        print("Credenciales inválidas.")
        return False

def recuperar_acceso_admin():
    _, contrasena_encriptada, clave_recuperacion_encriptada = cargar_credenciales_admin()
    if not clave_recuperacion_encriptada:
        print("No se ha configurado una clave de recuperación.")

    clave_recuperacion_input = input("Ingrese su clave única de recuperación: ")
    if verificar_clave_recuperacion(clave_recuperacion_input, clave_recuperacion_encriptada.encode('utf-8')):
        print("Clave de recuperación válida.")
        nueva_contrasena = input("Ingrese la nueva contraseña: ")
        confirmar_nueva_contrasena = input("Confirme la nueva contraseña: ")
        if nueva_contrasena == confirmar_nueva_contrasena:
            usuario, _, _ = cargar_credenciales_admin()
            nueva_contrasena_encriptada = encriptar_contrasena(nueva_contrasena)
            clave_recuperacion = generar_clave_recuperacion(usuario, nueva_contrasena)
            clave_recuperacion_encriptada = encriptar_contrasena(clave_recuperacion)
            guardar_credenciales_admin(usuario, nueva_contrasena_encriptada, clave_recuperacion_encriptada)
            print("\n¡Importante! Tu nueva clave única de recuperación es:")
            print(f"Nueva Clave Única de Recuperación: {clave_recuperacion}")
            print("Guárdala en un lugar seguro.")
        else:
            print("Las contraseñas no coinciden.")
    else:
        print("Clave de recuperación inválida.")
    return False
    exit()

#####################SECCION MENU##############################
def menu_principal():
    data = cargar_datos()

    while True:
        print("\n--- Sistema de Gestión de Envíos ---")
        print("1. Registrar Cliente")
        print("2. Registrar Envío")
        print("3. Seguimiento de Envío")
        print("4. Generar Informe de Volumen")
        print("5. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombres = input("Nombres: ")
            apellidos = input("Apellidos: ")
            identificacion = input("Identificación: ")
            tipo_identificacion = input("Tipo de Identificación: ")
            direccion = input("Dirección: ")
            telefono_fijo = input("Teléfono Fijo: ")
            celular = input("Celular: ")
            barrio = input("Barrio: ")
            nuevo_cliente = registrar_cliente(data, nombres, apellidos, identificacion, tipo_identificacion, direccion, telefono_fijo, celular, barrio)
            if nuevo_cliente:
                print("El cliente ha sido registrado exitosamente!")   
        elif opcion == "2":
            destinatario_nombre = input("Nombre del Destinatario: ")
            destinatario_direccion = input("Dirección del Destinatario: ")
            destinatario_telefono = input("Teléfono del Destinatario: ")
            destinatario_ciudad = input("Ciudad del Destinatario: ")
            destinatario_barrio = input("Barrio del Destinatario: ")
            remitente_identificacion = input("Identificación del Remitente: ")
            estado = input("Estado del Envío: ")
            nuevo_envio = registrar_envio(data, destinatario_nombre, destinatario_direccion, destinatario_telefono, destinatario_ciudad, destinatario_barrio, remitente_identificacion, estado)
            if nuevo_envio:
                print("Envío registrado exitosamente!")
        elif opcion == "3":
            numero_guia = input("Número de Guía: ")
            seguimiento_envio(data, numero_guia)        
        elif opcion == "4":
            generar_informe_volumen(data)
        elif opcion == "5":
            print("Cerrando sesión.")
            return False    
        else:
            print("Opción inválida.")
    return True

def main():
    if crear_cuenta_admin_inicial():
        print("\n--- Inicio de Sesión ---")
        while not login_administrador():
            recuperar = input("¿Olvidó su contraseña? (s/n): ")
            if recuperar.lower() == 's':
                recuperar_acceso_admin()
            else:
                print("Intente nuevamente.")
        menu_principal()
    else:
        print("\n--- Inicio de Sesión ---")
        while not login_administrador():
            recuperar = input("¿Olvidó su contraseña? (s/n): ")
            if recuperar.lower() == 's':
                recuperar_acceso_admin()
            else:
                print("Intente nuevamente.")
        menu_principal()

if __name__ == "__main__":
    main()
