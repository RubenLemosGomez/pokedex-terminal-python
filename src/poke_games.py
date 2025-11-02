from .poke_api_client import PokeApiClient
from .pokedex import Pokedex
from .utils import clean_terminal, generate_random_id


class PokeGames:
    def __init__(self):
        self.pokedex = Pokedex()
        self.poke_api_client = PokeApiClient()

    def guess_pokemon_name(self) -> None:
        """
        Juego estilo ahorcado para adivinar el nombre de un Pokemon.
        El usuario tiene un maximo de 5 fallos.

        Comentario: Uso una lista para mantener el estado del nombre oculto,
        donde cada posicion puede ser "_" (no adivinada) o la letra correcta.
        """
        # Obtengo un Pokemon aleatorio
        random_id = generate_random_id()
        data = self.poke_api_client.fetch_pokemon_data(random_id)

        if not data:
            print("ERROR: No se pudo obtener Pokemon. Intenta de nuevo.")
            return

        # Guardo el nombre en minusculas para facilitar comparaciones
        pokemon_name = data.get("name").lower()

        # Creo la representacion oculta del nombre
        masked_name = []
        for letter in pokemon_name:
            # Los guiones los mantengo visibles para dar pistas
            if letter == "-":
                masked_name.append("-")
            else:
                # Todas las demas letras las oculto con "_"
                masked_name.append("_")

        # Variables de control del juego
        used_letters = []  # Lista para recordar que letras ya se probaron
        failed_attempts = 0  # Contador de intentos fallidos
        max_attempts = 5  # Maximo de fallos permitidos segun el enunciado

        # Muestro las instrucciones del juego
        print("\n" + "=" * 70)
        print("         JUEGO: ADIVINA EL NOMBRE DEL POKEMON")
        print("=" * 70)
        print("Pokemon: " + " ".join(masked_name))  # .join() une la lista con espacios
        print("Fallos permitidos: " + str(max_attempts))
        print()

        # Bucle principal del juego
        # Continua mientras haya intentos Y queden letras por adivinar
        while failed_attempts < max_attempts and "_" in masked_name:
            letter = input("Introduce una letra: ").lower()

            # Validacion: debe ser exactamente una letra
            if len(letter) != 1 or not letter.isalpha():
                print("ERROR: Introduce solo una letra valida.")
                continue  # Vuelve al inicio del bucle sin contar como intento

            # Verifico si ya uso esa letra antes
            if letter in used_letters:
                print("Ya has usado esa letra. Prueba otra.")
                continue

            # Anado la letra a la lista de usadas
            used_letters.append(letter)

            # Compruebo si la letra esta en el nombre del Pokemon
            if letter in pokemon_name:
                # Si esta, revelo TODAS las posiciones donde aparece
                for i in range(len(pokemon_name)):
                    if pokemon_name[i] == letter:
                        masked_name[i] = letter
                print("CORRECTO! " + " ".join(masked_name))
            else:
                # Si no esta, sumo un fallo
                failed_attempts += 1
                print(
                    "INCORRECTO. Fallos: "
                    + str(failed_attempts)
                    + "/"
                    + str(max_attempts)
                )
                print("Estado actual: " + " ".join(masked_name))

        # Resultado final del juego
        print("\n" + "=" * 70)
        if "_" not in masked_name:
            # Si no quedan "_", el jugador gano
            print("¡GANASTE! El Pokemon era: " + pokemon_name.upper())
        else:
            # Si aun hay "_", se acabaron los intentos
            print("PERDISTE. El Pokemon era: " + pokemon_name.upper())

        print("=" * 70)

        input("Pulsa ENTER para volver al inicio...")
        clean_terminal()

        # Muestro la info completa del Pokemon
        self.pokedex.show_pokemon_info(data)

    def guess_pokemon_weight(self) -> None:
        """
        Juego donde el usuario debe adivinar cual de dos Pokemon pesa mas.

        Comentario: Genero dos IDs aleatorios y me aseguro de que sean diferentes
        usando un bucle while.
        """
        # Genero dos IDs aleatorios
        id1 = generate_random_id()
        id2 = generate_random_id()

        # Me aseguro de que sean diferentes
        while id2 == id1:
            id2 = generate_random_id()

        # Obtengo los datos de ambos Pokemon
        pokemon1 = self.poke_api_client.fetch_pokemon_data(id1)
        pokemon2 = self.poke_api_client.fetch_pokemon_data(id2)

        # Verifico que ambas peticiones fueron exitosas
        if not pokemon1 or not pokemon2:
            print("ERROR: No se pudieron obtener los Pokemon.")
            return

        # Extraigo nombres y pesos
        name1 = pokemon1.get("name").capitalize()
        weight1 = pokemon1.get("weight")
        name2 = pokemon2.get("name").capitalize()
        weight2 = pokemon2.get("weight")

        # Muestro las opciones al usuario
        print("\n" + "=" * 70)
        print("           JUEGO: ¿QUIEN PESA MAS?")
        print("=" * 70)
        print("1. " + name1)
        print("2. " + name2)
        print()

        try:
            choice = int(input("Elige 1 o 2: "))

            # Valido que sea 1 o 2
            if choice not in [1, 2]:
                print("ERROR: Opcion no valida.")
                return

            # Muestro los pesos reales (convierto de hectogramos a kg)
            print("\nRESULTADO:")
            print(name1 + ": " + str(weight1 / 10) + " kg")
            print(name2 + ": " + str(weight2 / 10) + " kg")

            # Determino cual es el mas pesado usando comparadores
            if weight1 > weight2:
                winner = 1
            elif weight2 > weight1:
                winner = 2
            else:
                # Caso raro pero posible: mismo peso
                print("EMPATE! Ambos pesan exactamente lo mismo.")
                return

            # Verifico si el usuario acertó
            if choice == winner:
                print("\nCORRECTO! Acertaste!")
            else:
                print("\nINCORRECTO. Mejor suerte la proxima.")

            input("Pulsa ENTER para volver al inicio...")
            clean_terminal()
        except ValueError:
            # Si el usuario no introduce un número
            print("ERROR: Introduce solo 1 o 2.")

    def guess_pokemon_height(self):
        """
        Juego donde el usuario debe adivinar cual de dos Pokemon es mas alto.

        Comentario: Estructura identica al juego de peso, pero usando altura.
        """
        # Genero dos IDs aleatorios diferentes
        id1 = generate_random_id()
        id2 = generate_random_id()

        while id2 == id1:
            id2 = generate_random_id()

        # Obtengo los datos
        pokemon1 = self.poke_api_client.fetch_pokemon_data(id1)
        pokemon2 = self.poke_api_client.fetch_pokemon_data(id2)

        if not pokemon1 or not pokemon2:
            print("ERROR: No se pudieron obtener los Pokemon.")
            return

        # Extraigo nombres y alturas
        name1 = pokemon1.get("name").capitalize()
        height1 = pokemon1.get("height")
        name2 = pokemon2.get("name").capitalize()
        height2 = pokemon2.get("height")

        # Muestro las opciones
        print("\n" + "=" * 70)
        print("           JUEGO: ¿QUIEN ES MAS ALTO?")
        print("=" * 70)
        print("1. " + name1)
        print("2. " + name2)
        print()

        try:
            choice = int(input("Elige 1 o 2: "))

            if choice not in [1, 2]:
                print("ERROR: Opcion no valida.")
                return

            # Muestro las alturas reales (convierto de decimetros a metros)
            print("\nRESULTADO:")
            print(name1 + ": " + str(height1 / 10) + " m")
            print(name2 + ": " + str(height2 / 10) + " m")

            # Determino el mas alto
            if height1 > height2:
                winner = 1
            elif height2 > height1:
                winner = 2
            else:
                print("EMPATE! Ambos miden exactamente lo mismo.")
                return

            # Verifico el resultado
            if choice == winner:
                print("\nCORRECTO! Acertaste!")
            else:
                print("\nINCORRECTO. Mejor suerte la proxima.")

            input("Pulsa ENTER para volver al inicio...")
            clean_terminal()

        except ValueError:
            print("ERROR: Introduce solo 1 o 2.")
