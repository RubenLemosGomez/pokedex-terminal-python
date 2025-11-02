import pathlib

from .poke_api_client import PokeApiClient
from .utils import clean_terminal, generate_random_id


class Pokedex:
    def __init__(self):
        self.poke_api_client = PokeApiClient()

    def show_pokedex_logo(self) -> None:
        dir_path = pathlib.Path(__file__).resolve().parent
        logo_path = dir_path / "pokedex_logo.txt"
        try:
            # Abrimos el archivo de forma segura
            with open(logo_path, encoding="utf-8") as file:
                # Leemos el contenido completo del archivo
                logo_content = file.read()
                # Imprimimos el contenido
                print(logo_content)
        except FileNotFoundError as e:
            print(f"ERROR: El archivo 'pokedex_logo.txt' no se encontró. Error: {e}")
        except Exception as e:
            print(f"ERROR al leer el archivo del logo: {e}")

    def show_pokemon_info(self, data: dict[str, any]) -> None:
        """
        Muestra la informacion principal de un Pokemon en formato columna.
        Simula la pantalla de una Pokedex clasica.

        Parametros:
            datos: diccionario con los datos del Pokemon obtenidos de la API

        Comentario: Alineamos los datos a la derecha usando espacios para simular
        una interfaz de dos columnas (menu izquierda, datos derecha).
        """

        # Es preferible usar el método .get() en lugar de acceder
        # directamente a la propiedad con [""]
        name = data.get("name")
        height = data.get("height") / 10
        weight = data.get("weight") / 10
        types = [  # Usamos list comprehension, forma más "pythonic"
            t.get("type").get("name").capitalize() for t in data.get("types")
        ]

        print("\n" + "=" * 70)
        print(" " * 20 + "------- POKEDEX ENTRY -------")
        print(" " * 20 + "NAME: " + name.upper())
        print(" " * 20 + "TYPE(S): " + ", ".join(types))
        print(" " * 20 + "HEIGHT: " + str(height) + " m")
        print(" " * 20 + "WEIGHT: " + str(weight) + " kg")
        print(" " * 20 + "-----------------------------")
        print("=" * 70)
        print()

    def get_pokemon_by_id(self, pokemon_id: str | int) -> None:
        """
        Permite al usuario consultar un Pokemon introduciendo su ID numerico.
        Valida que el ID este en el rango valido (1-1025).

        Comentario: Uso try/except para capturar el ValueError que se produce
        si el usuario introduce texto en vez de un numero.
        """
        try:
            pokemon_id = int(pokemon_id)

            # Valido el rango usando comparadores
            if pokemon_id < 1 or pokemon_id > 1025:
                print("ERROR: ID fuera de rango. Debe estar entre 1 y 1025.")
                return  # Salgo de la funcion sin hacer nada mas

            # Si llegamos aqui, el ID es valido
            data = self.poke_api_client.fetch_pokemon_data(pokemon_id)
            self.show_pokemon_info(data)
            input("Pulsa ENTER para volver al inicio...")
            clean_terminal()

        except ValueError:
            # Se ejecuta si int() falla al convertir (ej: usuario escribe "abc")
            print("ERROR: Debes introducir un numero valido.")

    def get_pokemon_by_name(self, pokemon_name: str) -> None:
        """
        Permite al usuario consultar un Pokemon introduciendo su nombre.

        Comentario: lower() convierte a minusculas (la API es case-sensitive)
        y strip() elimina espacios al inicio y final.
        """
        pokemon_name = pokemon_name.lower().strip()

        # Verifico que el usuario haya escrito algo
        if pokemon_name == "":
            print("ERROR: Debes introducir un nombre valido.")
            return

        data = self.poke_api_client.fetch_pokemon_data(pokemon_name)
        self.show_pokemon_info(data)
        input("Pulsa ENTER para volver al inicio...")
        clean_terminal()

    def get_random_pokemon(self) -> None:
        """
        Consulta un Pokemon aleatorio generando un ID al azar.

        Comentario: random.randint(a, b) genera un entero aleatorio
        entre a y b, ambos incluidos.
        """
        random_id = generate_random_id()
        print("\nBuscando Pokemon aleatorio con ID: " + str(random_id) + "...")

        data = self.poke_api_client.fetch_pokemon_data(random_id)
        self.show_pokemon_info(data)
        input("Pulsa ENTER para volver al inicio...")
        clean_terminal()
