import requests


class PokeApiClient:
    def __init__(self):
        self.base_url: str = "https://pokeapi.co/api/v2/pokemon/"

    def fetch_pokemon_data(self, pokemon_id: str | int) -> dict[str, any] | None:
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
            # Usamos f-strings que además de ser más actuales, son
            # preferibles en la mayoría de casos
            url = f"{self.base_url}{pokemon_id}"

            # Hago la peticion GET con timeout de 10 segundos para evitar bloqueos
            response = requests.get(url, timeout=10)

            # Usamos el método .raise_for_status() para que lance una
            # excepción si el ćodigo HTTP es 4xx o 5xx
            response.raise_for_status()

            return response.json()

        # Tomamos varios errores para saber especificamente que ha
        # fallado en caso de excepción
        except requests.HTTPError as e:
            print(f"Error tratando de obtener los datos de la API. Error: {e}")
            return None
        # Capturamos cualquier excepción (sin conexion, timeout, etc.)
        except Exception as e:
            print(f"Error desconocido: {e}")
            return None
