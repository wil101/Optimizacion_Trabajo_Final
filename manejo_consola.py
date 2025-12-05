"""
==================================================================================
MÓDULO DE MANEJO DE CONSOLA
==================================================================================
Funciones para interacción con el usuario a través de consola.
==================================================================================
"""

import numpy as np
from utilidades import (
    validar_numero_positivo, 
    validar_lista_numeros,
    validar_opcion,
    mostrar_titulo
)
from ejemplos_casos_prueba import generar_problema_complejo


# ==================================================================================
# INGRESO DE DATOS
# ==================================================================================

def ingresar_tipo_optimizacion():
    """
    Solicita al usuario el tipo de optimización.
    
    Returns:
        str: 'max' o 'min'
    """
    while True:
        tipo = input("¿Desea MAXIMIZAR o MINIMIZAR? (max/min): ").strip().lower()
        if tipo in ['max', 'min']:
            return tipo
        print("⚠️  Por favor ingrese 'max' o 'min'")


def ingresar_numero_variables():
    """
    Solicita al usuario el número de variables.
    
    Returns:
        tuple: (num_vars, nombres_vars)
    """
    num_vars = validar_numero_positivo(
        "\n¿Cuántas variables tiene el problema? (2 o 3 recomendado): "
    )
    nombres_vars = [f'x{i+1}' for i in range(num_vars)]
    return num_vars, nombres_vars


def ingresar_coeficientes_objetivo(num_vars, nombres_vars):
    """
    Solicita los coeficientes de la función objetivo.
    
    Args:
        num_vars: Número de variables
        nombres_vars: Lista de nombres de variables
    
    Returns:
        np.array: Vector de coeficientes
    """
    print(f"\nIngrese los coeficientes de la función objetivo (separados por espacio):")
    print(f"Ejemplo para Z = 3x₁ + 5x₂: ingrese '3 5'")
    
    coef = validar_lista_numeros(
        f"Coeficientes ({' '.join(nombres_vars)}): ",
        num_vars
    )
    return np.array(coef)


def ingresar_numero_restricciones():
    """
    Solicita al usuario el número de restricciones.
    
    Returns:
        int: Número de restricciones
    """
    return validar_numero_positivo("\n¿Cuántas restricciones tiene el problema? ")


def ingresar_restriccion(numero, num_vars):
    """
    Solicita una restricción al usuario.
    
    Args:
        numero: Número de la restricción
        num_vars: Número de variables
    
    Returns:
        tuple: (coeficientes, valor, tipo_restriccion) o None si hay error
    """
    while True:
        try:
            rest_str = input(f"Restricción {numero}: ")
            partes = rest_str.split()
            
            tipo_idx = -1
            tipo_rest = None
            for idx, parte in enumerate(partes):
                if parte in ['<=', '>=', '=']:
                    tipo_idx = idx
                    tipo_rest = parte
                    break
            
            if tipo_idx == -1:
                print("⚠️  Debe incluir un tipo de restricción: <=, >= o =")
                continue
            
            coef = [float(x) for x in partes[:tipo_idx]]
            valor = float(partes[tipo_idx + 1])
            
            if len(coef) != num_vars:
                print(f"⚠️  Debe ingresar {num_vars} coeficientes para las variables.")
                continue
            
            return coef, valor, tipo_rest
                
        except (ValueError, IndexError):
            print("⚠️  Formato inválido. Ejemplo: '2 3 <= 10'. Intente nuevamente.")


def ingresar_problema_completo():
    """
    Guía al usuario para ingresar un problema completo.
    
    Returns:
        dict: Diccionario con todos los datos del problema
    """
    try:
        mostrar_titulo("INGRESO MANUAL DE PROBLEMA DE PROGRAMACIÓN LINEAL")
        
        tipo = ingresar_tipo_optimizacion()
        num_vars, nombres_vars = ingresar_numero_variables()
        c = ingresar_coeficientes_objetivo(num_vars, nombres_vars)
        num_rest = ingresar_numero_restricciones()
        
        print(f"\nIngrese cada restricción en formato: coeficientes tipo valor")
        print(f"Ejemplo para 2x₁ + 3x₂ ≤ 10: ingrese '2 3 <= 10'")
        print(f"Tipos permitidos: <= (menor o igual), >= (mayor o igual), = (igual)\n")
        
        A_list = []
        b_list = []
        tipos_rest_list = []
        
        for i in range(num_rest):
            coef, valor, tipo_rest = ingresar_restriccion(i+1, num_vars)
            A_list.append(coef)
            b_list.append(valor)
            tipos_rest_list.append(tipo_rest)
        
        A = np.array(A_list)
        b = np.array(b_list)
        
        print("\n✅ Problema ingresado correctamente!")
        
        return {
            'tipo': tipo,
            'c': c,
            'A': A,
            'b': b,
            'tipos_restricciones': tipos_rest_list,
            'num_vars': num_vars,
            'num_restricciones': num_rest,
            'nombres_vars': nombres_vars
        }
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Ingreso cancelado por el usuario")
        return None


# ==================================================================================
# GENERACIÓN DE EJEMPLOS
# ==================================================================================

def generar_problema_ejemplo_2d():
    """
    Genera un problema de ejemplo con 2 variables.
    
    Returns:
        dict: Diccionario con los datos del problema
    """
    print("\nFunción Objetivo: Maximizar Z = 3x₁ + 5x₂")
    print("\nRestricciones:")
    print("  x₁ ≤ 4")
    print("  2x₂ ≤ 12")
    print("  3x₁ + 2x₂ ≤ 18")
    print("  x₁, x₂ ≥ 0")
    
    return {
        'tipo': 'max',
        'c': np.array([3.0, 5.0]),
        'A': np.array([
            [1.0, 0.0],
            [0.0, 2.0],
            [3.0, 2.0]
        ]),
        'b': np.array([4.0, 12.0, 18.0]),
        'num_vars': 2,
        'num_restricciones': 3,
        'nombres_vars': ['x1', 'x2'],
        'tipos_restricciones': ['<=', '<=', '<=']
    }


def generar_problema_ejemplo_3d():
    """
    Genera un problema de ejemplo con 3 variables.
    
    Returns:
        dict: Diccionario con los datos del problema
    """
    print("\nFunción Objetivo: Maximizar Z = 2x₁ + 3x₂ + 4x₃")
    print("\nRestricciones:")
    print("  x₁ + x₂ + x₃ ≤ 10")
    print("  2x₁ + x₂ ≤ 12")
    print("  x₂ + 2x₃ ≤ 14")
    print("  x₁, x₂, x₃ ≥ 0")
    
    return {
        'tipo': 'max',
        'c': np.array([2.0, 3.0, 4.0]),
        'A': np.array([
            [1.0, 1.0, 1.0],
            [2.0, 1.0, 0.0],
            [0.0, 1.0, 2.0]
        ]),
        'b': np.array([10.0, 12.0, 14.0]),
        'num_vars': 3,
        'num_restricciones': 3,
        'nombres_vars': ['x1', 'x2', 'x3'],
        'tipos_restricciones': ['<=', '<=', '<=']
    }


# ==================================================================================
# MENÚ PRINCIPAL
# ==================================================================================

def mostrar_menu_principal():
    """
    Muestra el menú principal y retorna la opción seleccionada.
    
    Returns:
        str: Opción seleccionada ('1', '2', '3', '4', o '5')
    """
    print("\n")
    print("="*80)
    print(" "*20 + "SOLUCIONADOR DE PROGRAMACIÓN LINEAL")
    print(" "*25 + "Método Simplex Revisado & Gran M")
    print("="*80)
    print("\n  Desarrollado para resolver problemas de PL paso a paso")
    print("  Muestra cada iteración del tablero simplex y solución gráfica (2D)\n")
    print("="*80)
    
    print("\n📝 OPCIONES DE INGRESO:")
    print("  1. Ingresar problema manualmente")
    print("  2. Usar problema de ejemplo (2 variables)")
    print("  3. Usar problema complejo (con restricciones mixtas)")
    print("  4. Usar problema desde el código (Casos de prueba)")
    print("  5. Salir")
    
    return validar_opcion(['1', '2', '3', '4', '5'])


def mostrar_menu_problemas_definidos():
    """
    Muestra el submenú para elegir un problema predefinido.
    
    Returns:
        str: Opción seleccionada ('1' a '8')
    """
    print("\n")
    mostrar_titulo("SELECCIONAR PROBLEMA DESDE CÓDIGO")
    print("\n📂 Elija un caso de prueba predefinido:")
    print("  1. Problema Personalizado (Modificable en el código)")
    print("  2. Prueba de Método de Dos Fases (Minimizar, >=, =)")
    print("  3. Prueba de Gráfico con Números Grandes")
    print("  4. Prueba con Múltiples Variables (5 variables)")
    print("  --- Casos Especiales ---")
    print("  5. Prueba de Problema Infactible")
    print("  6. Prueba de Solución No Acotada")
    print("  7. Prueba de Múltiples Soluciones Óptimas")
    print("  8. Volver al menú principal")
    
    return validar_opcion(['1', '2', '3', '4', '5', '6', '7', '8'])


def confirmar_accion(mensaje):
    """
    Solicita confirmación al usuario (s/n).
    
    Args:
        mensaje: Mensaje a mostrar
    
    Returns:
        bool: True si confirma, False si no
    """
    while True:
        resp = input(f"\n{mensaje} (s/n): ").strip().lower()
        if resp in ['s', 'n']:
            return resp == 's'
        print("⚠️  Por favor ingrese 's' o 'n'")
