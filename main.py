# Traemos nuestros propios paquetes
from src.poke_games import PokeGames
from src.pokedex import Pokedex
from src.utils import clean_terminal

# ============================================================================
# MENU PRINCIPAL (HUD POKEDEX)
# ============================================================================


def main():
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
        "Salir",
    ]

    # Bucle infinito del menu (while True)
    while True:
        clean_terminal()
        poke_games = PokeGames()
        pokedex = Pokedex()

        # Muestro el logo de la Pokedex
        pokedex.show_pokedex_logo()

        # Dibujo el menu con bordes decorativos
        print("╔" + "═" * 66 + "╗")
        print("║" + " " * 20 + "MENU PRINCIPAL" + " " * 32 + "║")
        print("╠" + "═" * 66 + "╣")

        # Itero sobre las opciones usando enumerate para tener el indice
        for i, opcion in enumerate(opciones):
            # Calculo los espacios necesarios para alinear el borde derecho
            espacios = 64 - len(str(i + 1) + ". " + opcion)
            print("║ " + str(i + 1) + ". " + opcion + " " * espacios + " ║")

        print("╚" + "═" * 66 + "╝")

        try:
            seleccion = int(input("\nSelecciona una opcion (1-7): "))

            # Estructura if/elif para ejecutar la funcion
            # correspondiente
            match seleccion:
                case 1:
                    pokemon_id: str = input("Dame el ID del Pokémon: ")
                    pokedex.get_pokemon_by_id(pokemon_id)
                case 2:
                    pokemon_name: str = input("Dame el nombre del Pokémon: ")
                    pokedex.get_pokemon_by_name(pokemon_name)
                case 3:
                    pokedex.get_random_pokemon()
                case 4:
                    poke_games.guess_pokemon_name()
                case 5:
                    poke_games.guess_pokemon_weight()
                case 6:
                    poke_games.guess_pokemon_height()
                case 7:
                    print("\nCerrando Pokedex... ¡Hasta pronto!")
                    break  # Rompe el bucle while y termina el programa
                case _:
                    print("ERROR: Opcion no valida. Elige entre 1 y 7.")

        except ValueError:
            # Se ejecuta si el usuario no introduce un numero
            print("ERROR: Introduce un numero valido.")
        except KeyboardInterrupt:
            # Se ejecuta si el usuario presiona Ctrl+C
            print("\n\nPrograma interrumpido. ¡Adios!")
            break
        except Exception as e:
            print(f"Error desconocido: {e}")
            break


# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
    Punto de entrada principal del script.
    Solo se ejecuta si el archivo se ejecuta directamente,
    no si se importa como modulo.
    """
    main()
