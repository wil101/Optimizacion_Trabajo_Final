from resolucion_simplex import resolver_problema_general

def caso_empate_variable_entrante():
    """
    Caso de prueba con empate en la variable entrante.
    Maximizar Z = 3x1 + 3x2
    Sujeto a:
    x1 + 2x2 <= 10
    2x1 + x2 <= 8
    x1, x2 >= 0
    """
    print("\n--- CASO: EMPATE EN VARIABLE ENTRANTE ---")
    problema = {
        'c': [3, 3],
        'A': [[1, 2], [2, 1]],
        'b': [10, 8],
        'tipo': 'max',
        'num_vars': 2,
        'nombres_vars': ['x1', 'x2'],
        'tipos_restricciones': ['<=', '<=']
    }
    resolver_problema_general(problema)

def caso_degeneracion():
    """
    Caso de prueba con degeneración (empate en la variable saliente).
    Maximizar Z = 3x1 + 9x2
    Sujeto a:
    x1 + 4x2 <= 8
    x1 + 2x2 <= 4
    x1, x2 >= 0
    """
    print("\n--- CASO: DEGENERACIÓN (EMPATE EN VARIABLE SALIENTE) ---")
    problema = {
        'c': [3, 9],
        'A': [[1, 4], [1, 2]],
        'b': [8, 4],
        'tipo': 'max',
        'num_vars': 2,
        'nombres_vars': ['x1', 'x2'],
        'tipos_restricciones': ['<=', '<=']
    }
    resolver_problema_general(problema)

def caso_solucion_no_acotada():
    """
    Caso de prueba con solución no acotada.
    Maximizar Z = 2x1 + x2
    Sujeto a:
    x1 - x2 <= 10
    2x1 - x2 <= 40
    x1, x2 >= 0
    """
    print("\n--- CASO: SOLUCIÓN NO ACOTADA ---")
    problema = {
        'c': [2, 1],
        'A': [[1, -1], [2, -1]],
        'b': [10, 40],
        'tipo': 'max',
        'num_vars': 2,
        'nombres_vars': ['x1', 'x2'],
        'tipos_restricciones': ['<=', '<=']
    }
    resolver_problema_general(problema)

if __name__ == '__main__':
    while True:
        print("\n=============================================")
        print("  MENÚ DE PRUEBA DE CASOS ESPECIALES SIMPLEX")
        print("=============================================")
        print("1. Empate en la variable que entra")
        print("2. Empate en la variable que sale (Degeneración)")
        print("3. Solución no acotada (Z no acotada)")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción para probar: ")
        
        if opcion == '1':
            caso_empate_variable_entrante()
        elif opcion == '2':
            caso_degeneracion()
        elif opcion == '3':
            caso_solucion_no_acotada()
        elif opcion == '4':
            print("Saliendo del programa de pruebas.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        input("\nPresione ENTER para volver al menú...")