def calculate() -> float:
    try:
        entrada = input("Ingresa una operación (ej. 5 + 3), 'c' para borrar, 'q' para salir: ").strip()

        if entrada.lower() == 'q':
            print("Saliendo...")
            exit()

        if entrada.lower() == 'c':
            print("Operación borrada.")
            return 0.0

        entrada = entrada.replace(" ", "")  # quitar espacios

        # Suma
        if "+" in entrada:
            a, b = entrada.split("+")
            return float(a) + float(b)

        # Resta
        elif "-" in entrada:
            a, b = entrada.split("-")
            return float(a) - float(b)

        else:
            print("Operación no soportada aún.")
            return 0.0

    except ValueError:
        print("Error: Entrada inválida.")
        return 0.0
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 0.0


if __name__ == "__main__":
    while True:
        resultado = calculate()
        print("Resultado:", resultado)
