import requests  # Libreria para hacer peticiones HTTP a APIs REST
import random    # Libreria para generar numeros aleatorios
import json      # Libreria para manejar datos en formato JSON



# Logo principal de la Pokedex que se muestra en el menu
pokedex_logo = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║           |  _ \ / _ \| |/ / ____|  \/  |/ _ \| \ | |          ║
║           | |_) | | | | ' /|  _| | |\/| | | | |  \| |          ║
║           |  __/| |_| | . \| |___| |  | | |_| | |\  |          ║
║           |_|    \___/|_|\_\_____|_|  |_|\___/|_| \_|          ║
║                                                                ║
║                                                                ║
║                            0xPOKEDEX                           ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# FUNCIONES DE CONEXION A LA API
# ============================================================================

def obtener_pokemon_api(identificador):
    """
    Realiza una peticion HTTP GET a la PokeAPI para obtener datos de un Pokemon.
    
    Parametros:
        identificador: puede ser un ID numerico (int) o un nombre (str)
    
    Retorna:
        dict: diccionario con los datos JSON del Pokemon si tiene exito
        None: si hay algun error en la peticion o el Pokemon no existe
    
    Comentario: La API devuelve altura en decimetros y peso en hectogramos,
    por lo que hay que dividir entre 10 para obtener metros y kilogramos.
    """
    try:
        # Construyo la URL concatenando el endpoint base con el identificador
        # str() asegura que funcione tanto con numeros como con strings
        url = "https://pokeapi.co/api/v2/pokemon/" + str(identificador)
        
        # Hago la peticion GET con timeout de 10 segundos para evitar bloqueos
        respuesta = requests.get(url, timeout=10)
        
        # Verifico que el codigo de respuesta sea 200 (exito)
        if respuesta.status_code == 200:
            # .json() convierte la respuesta JSON en un diccionario de Python
            return respuesta.json()
        else:
            # Si el codigo no es 200, puede ser 404 (no encontrado) u otro error
            return None
    except:
        # Capturo cualquier excepcion (sin conexion, timeout, etc.)
        return None

# ============================================================================
# FUNCIONES DE VISUALIZACION
# ============================================================================

def mostrar_info_pokemon(datos):
    """
    Muestra la informacion principal de un Pokemon en formato columna.
    Simula la pantalla de una Pokedex clasica.
    
    Parametros:
        datos: diccionario con los datos del Pokemon obtenidos de la API
    
    Comentario: Alineamos los datos a la derecha usando espacios para simular
    una interfaz de dos columnas (menu izquierda, datos derecha).
    """
    if not datos:
        print("ERROR: No se pudo obtener informacion del Pokemon.")
        return
    
    # Extraigo los datos basicos del diccionario
    nombre = datos["name"].capitalize()  # capitalize() pone solo la primera en mayuscula
    altura_dm = datos["height"]  # Viene en decimetros segun la documentacion de PokeAPI
    peso_hg = datos["weight"]    # Viene en hectogramos
    
    # Los tipos estan en una lista dentro de "types", los extraigo iterando
    tipos = []
    for tipo in datos["types"]:
        # Navego por la estructura: types -> type -> name
        tipos.append(tipo["type"]["name"].capitalize())
    
    # Convierto las unidades a metros y kilogramos
    altura_m = altura_dm / 10
    peso_kg = peso_hg / 10
    
    # Muestro la informacion con formato de caja ASCII
    print("\n" + "="*70)
    print(" "*20 + "------- POKEDEX ENTRY -------")
    print(" "*20 + "NAME: " + nombre.upper())
    print(" "*20 + "TYPE(S): " + ", ".join(tipos))
    print(" "*20 + "HEIGHT: " + str(altura_m) + " m")
    print(" "*20 + "WEIGHT: " + str(peso_kg) + " kg")
    print(" "*20 + "-----------------------------")
    print("="*70)
    print()

# ============================================================================
# FUNCIONES DE CONSULTA
# ============================================================================

def consultar_por_id():
    """
    Permite al usuario consultar un Pokemon introduciendo su ID numerico.
    Valida que el ID este en el rango valido (1-1025).
    
    Comentario: Uso try/except para capturar el ValueError que se produce
    si el usuario introduce texto en vez de un numero.
    """
    try:
        # input() siempre devuelve string, int() lo convierte a entero
        id_pokemon = int(input("\nIntroduce el ID del Pokemon (1-1025): "))
        
        # Valido el rango usando comparadores
        if id_pokemon < 1 or id_pokemon > 1025:
            print("ERROR: ID fuera de rango. Debe estar entre 1 y 1025.")
            return  # Salgo de la funcion sin hacer nada mas
        
        # Si llegamos aqui, el ID es valido
        datos = obtener_pokemon_api(id_pokemon)
        mostrar_info_pokemon(datos)
        
    except ValueError:
        # Se ejecuta si int() falla al convertir (ej: usuario escribe "abc")
        print("ERROR: Debes introducir un numero valido.")

def consultar_por_nombre():
    """
    Permite al usuario consultar un Pokemon introduciendo su nombre.
    
    Comentario: lower() convierte a minusculas (la API es case-sensitive)
    y strip() elimina espacios al inicio y final.
    """
    nombre = input("\nIntroduce el nombre del Pokemon: ").lower().strip()
    
    # Verifico que el usuario haya escrito algo
    if not nombre:
        print("ERROR: Debes introducir un nombre valido.")
        return
    
    datos = obtener_pokemon_api(nombre)
    mostrar_info_pokemon(datos)

def consultar_aleatorio():
    """
    Consulta un Pokemon aleatorio generando un ID al azar.
    
    Comentario: random.randint(a, b) genera un entero aleatorio
    entre a y b, ambos incluidos.
    """
    id_aleatorio = random.randint(1, 1025)
    print("\nBuscando Pokemon aleatorio con ID: " + str(id_aleatorio) + "...")
    
    datos = obtener_pokemon_api(id_aleatorio)
    mostrar_info_pokemon(datos)

# ============================================================================
# JUEGOS INTERACTIVOS
# ============================================================================

def juego_adivinar_nombre():
    """
    Juego estilo ahorcado para adivinar el nombre de un Pokemon.
    El usuario tiene un maximo de 5 fallos.
    
    Comentario: Uso una lista para mantener el estado del nombre oculto,
    donde cada posicion puede ser "_" (no adivinada) o la letra correcta.
    """
    # Obtengo un Pokemon aleatorio
    id_aleatorio = random.randint(1, 1025)
    datos = obtener_pokemon_api(id_aleatorio)
    
    if not datos:
        print("ERROR: No se pudo obtener Pokemon. Intenta de nuevo.")
        return
    
    # Guardo el nombre en minusculas para facilitar comparaciones
    nombre_pokemon = datos["name"].lower()
    
    # Creo la representacion oculta del nombre
    nombre_oculto = []
    for letra in nombre_pokemon:
        # Los guiones los mantengo visibles para dar pistas
        if letra == "-":
            nombre_oculto.append("-")
        else:
            # Todas las demas letras las oculto con "_"
            nombre_oculto.append("_")
    
    # Variables de control del juego
    letras_usadas = []  # Lista para recordar que letras ya se probaron
    fallos = 0          # Contador de intentos fallidos
    max_fallos = 5      # Maximo de fallos permitidos segun el enunciado
    
    # Muestro las instrucciones del juego
    print("\n" + "="*70)
    print("         JUEGO: ADIVINA EL NOMBRE DEL POKEMON")
    print("="*70)
    print("Pokemon: " + " ".join(nombre_oculto))  # .join() une la lista con espacios
    print("Fallos permitidos: " + str(max_fallos))
    print()
    
    # Bucle principal del juego
    # Continua mientras haya intentos Y queden letras por adivinar
    while fallos < max_fallos and "_" in nombre_oculto:
        letra = input("Introduce una letra: ").lower()
        
        # Validacion: debe ser exactamente una letra
        if len(letra) != 1 or not letra.isalpha():
            print("ERROR: Introduce solo una letra valida.")
            continue  # Vuelve al inicio del bucle sin contar como intento
        
        # Verifico si ya uso esa letra antes
        if letra in letras_usadas:
            print("Ya has usado esa letra. Prueba otra.")
            continue
        
        # Anado la letra a la lista de usadas
        letras_usadas.append(letra)
        
        # Compruebo si la letra esta en el nombre del Pokemon
        if letra in nombre_pokemon:
            # Si esta, revelo TODAS las posiciones donde aparece
            for i in range(len(nombre_pokemon)):
                if nombre_pokemon[i] == letra:
                    nombre_oculto[i] = letra
            print("CORRECTO! " + " ".join(nombre_oculto))
        else:
            # Si no esta, sumo un fallo
            fallos += 1
            print("INCORRECTO. Fallos: " + str(fallos) + "/" + str(max_fallos))
            print("Estado actual: " + " ".join(nombre_oculto))
    
    # Resultado final del juego
    print("\n" + "="*70)
    if "_" not in nombre_oculto:
        # Si no quedan "_", el jugador gano
        print("¡GANASTE! El Pokemon era: " + nombre_pokemon.upper())
    else:
        # Si aun hay "_", se acabaron los intentos
        print("PERDISTE. El Pokemon era: " + nombre_pokemon.upper())
    print("="*70)
    
    # Muestro la info completa del Pokemon
    mostrar_info_pokemon(datos)

def juego_adivinar_peso():
    """
    Juego donde el usuario debe adivinar cual de dos Pokemon pesa mas.
    
    Comentario: Genero dos IDs aleatorios y me aseguro de que sean diferentes
    usando un bucle while.
    """
    # Genero dos IDs aleatorios
    id1 = random.randint(1, 1025)
    id2 = random.randint(1, 1025)
    
    # Me aseguro de que sean diferentes
    while id2 == id1:
        id2 = random.randint(1, 1025)
    
    # Obtengo los datos de ambos Pokemon
    p1 = obtener_pokemon_api(id1)
    p2 = obtener_pokemon_api(id2)
    
    # Verifico que ambas peticiones fueron exitosas
    if not p1 or not p2:
        print("ERROR: No se pudieron obtener los Pokemon.")
        return
    
    # Extraigo nombres y pesos
    nombre1 = p1["name"].capitalize()
    peso1 = p1["weight"]
    nombre2 = p2["name"].capitalize()
    peso2 = p2["weight"]
    
    # Muestro las opciones al usuario
    print("\n" + "="*70)
    print("           JUEGO: ¿QUIEN PESA MAS?")
    print("="*70)
    print("1. " + nombre1)
    print("2. " + nombre2)
    print()
    
    try:
        eleccion = int(input("Elige 1 o 2: "))
        
        # Valido que sea 1 o 2
        if eleccion not in [1, 2]:
            print("ERROR: Opcion no valida.")
            return
        
        # Muestro los pesos reales (convierto de hectogramos a kg)
        print("\nRESULTADO:")
        print(nombre1 + ": " + str(peso1/10) + " kg")
        print(nombre2 + ": " + str(peso2/10) + " kg")
        
        # Determino cual es el mas pesado usando comparadores
        if peso1 > peso2:
            ganador = 1
        elif peso2 > peso1:
            ganador = 2
        else:
            # Caso raro pero posible: mismo peso
            print("EMPATE! Ambos pesan exactamente lo mismo.")
            return
        
        # Verifico si el usuario acerto
        if eleccion == ganador:
            print("\nCORRECTO! Acertaste!")
        else:
            print("\nINCORRECTO. Mejor suerte la proxima.")
            
    except ValueError:
        # Si el usuario no introduce un numero
        print("ERROR: Introduce solo 1 o 2.")

def juego_adivinar_altura():
    """
    Juego donde el usuario debe adivinar cual de dos Pokemon es mas alto.
    
    Comentario: Estructura identica al juego de peso, pero usando altura.
    """
    # Genero dos IDs aleatorios diferentes
    id1 = random.randint(1, 1025)
    id2 = random.randint(1, 1025)
    
    while id2 == id1:
        id2 = random.randint(1, 1025)
    
    # Obtengo los datos
    p1 = obtener_pokemon_api(id1)
    p2 = obtener_pokemon_api(id2)
    
    if not p1 or not p2:
        print("ERROR: No se pudieron obtener los Pokemon.")
        return
    
    # Extraigo nombres y alturas
    nombre1 = p1["name"].capitalize()
    altura1 = p1["height"]
    nombre2 = p2["name"].capitalize()
    altura2 = p2["height"]
    
    # Muestro las opciones
    print("\n" + "="*70)
    print("           JUEGO: ¿QUIEN ES MAS ALTO?")
    print("="*70)
    print("1. " + nombre1)
    print("2. " + nombre2)
    print()
    
    try:
        eleccion = int(input("Elige 1 o 2: "))
        
        if eleccion not in [1, 2]:
            print("ERROR: Opcion no valida.")
            return
        
        # Muestro las alturas reales (convierto de decimetros a metros)
        print("\nRESULTADO:")
        print(nombre1 + ": " + str(altura1/10) + " m")
        print(nombre2 + ": " + str(altura2/10) + " m")
        
        # Determino el mas alto
        if altura1 > altura2:
            ganador = 1
        elif altura2 > altura1:
            ganador = 2
        else:
            print("EMPATE! Ambos miden exactamente lo mismo.")
            return
        
        # Verifico el resultado
        if eleccion == ganador:
            print("\nCORRECTO! Acertaste!")
        else:
            print("\nINCORRECTO. Mejor suerte la proxima.")
            
    except ValueError:
        print("ERROR: Introduce solo 1 o 2.")

# ============================================================================
# MENU PRINCIPAL (HUD POKEDEX)
# ============================================================================

def menu_principal():
    """
    Funcion del menu principal que gestiona la navegacion por la Pokedex.
    Implementa un bucle infinito que solo termina cuando el usuario elige salir.
    
    Comentario: Este es el HUD principal de la Pokedex, diseñado con
    caracteres box-drawing de Unicode para una apariencia retro.
    """
    # Lista con todas las opciones del menu
    opciones = [
        "Buscar por ID",
        "Buscar por nombre", 
        "Pokemon aleatorio",
        "Juego: Adivinar nombre (Ahorcado)",
        "Juego: ¿Quien pesa mas?",
        "Juego: ¿Quien es mas alto?",
        "Salir"
    ]
    
    # Bucle infinito del menu (while True)
    while True:
        # Muestro el logo de la Pokedex
        print(pokedex_logo)
        
        # Dibujo el menu con bordes decorativos
        print("╔" + "═"*66 + "╗")
        print("║" + " "*20 + "MENU PRINCIPAL" + " "*32 + "║")
        print("╠" + "═"*66 + "╣")
        
        # Itero sobre las opciones usando enumerate para tener el indice
        for i, opcion in enumerate(opciones):
            # Calculo los espacios necesarios para alinear el borde derecho
            espacios = 64 - len(str(i+1) + ". " + opcion)
            print("║ " + str(i+1) + ". " + opcion + " "*espacios + " ║")
        
        print("╚" + "═"*66 + "╝")
        
        try:
            seleccion = int(input("\nSelecciona una opcion (1-7): "))
            
            # Estructura if/elif para ejecutar la funcion correspondiente
            if seleccion == 1:
                consultar_por_id()
            elif seleccion == 2:
                consultar_por_nombre()
            elif seleccion == 3:
                consultar_aleatorio()
            elif seleccion == 4:
                juego_adivinar_nombre()
            elif seleccion == 5:
                juego_adivinar_peso()
            elif seleccion == 6:
                juego_adivinar_altura()
            elif seleccion == 7:
                print("\nCerrando Pokedex... ¡Hasta pronto!")
                break  # Rompe el bucle while y termina el programa
            else:
                print("ERROR: Opcion no valida. Elige entre 1 y 7.")
                
        except ValueError:
            # Se ejecuta si el usuario no introduce un numero
            print("ERROR: Introduce un numero valido.")
        except KeyboardInterrupt:
            # Se ejecuta si el usuario presiona Ctrl+C
            print("\n\nPrograma interrumpido. ¡Adios!")
            break

# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
    Punto de entrada principal del script.
    Solo se ejecuta si el archivo se ejecuta directamente,
    no si se importa como modulo.
    
    Comentario: Verifico la conexion a la API antes de iniciar
    para dar feedback inmediato al usuario si hay problemas de red.
    """
    try:
        # Hago una peticion de prueba a Bulbasaur (ID 1)
        print("\nVerificando conexion a PokeAPI...")
        test = requests.get("https://pokeapi.co/api/v2/pokemon/1", timeout=5)
        
        if test.status_code == 200:
            print("Conexion establecida correctamente.")
            input("\nPresiona ENTER para iniciar la Pokedex...")
            menu_principal()
        else:
            print("ERROR: No se puede conectar a PokeAPI (codigo " + str(test.status_code) + ").")
    except:
        # Capturo errores de conexion (sin internet, API caida, etc.)
        print("ERROR: Verifica tu conexion a Internet.")
