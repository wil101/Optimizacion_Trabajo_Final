import numpy as np
from utilidades import formatear_numero

def _mostrar_problema(problema: dict, nombre_problema: str):
    """
    Imprime en consola la definición de un problema de PL.
    """
    print(f"\nCargando '{nombre_problema}':")
    
    # Función Objetivo
    tipo_str = "Maximizar" if problema['tipo'] == 'max' else "Minimizar"
    c = problema['c']
    nombres = problema['nombres_vars']
    
    objetivo_parts = []
    for i in range(len(c)):
        coef_str = formatear_numero(c[i], 2)
        if c[i] != 0:
             objetivo_parts.append(f"{coef_str}{nombres[i]}")

    objetivo_str = " + ".join(objetivo_parts).replace("+ -", "- ")
    print(f"Función Objetivo: {tipo_str} Z = {objetivo_str}\n")

    # Restricciones
    print("Restricciones:")
    A = problema['A']
    b = problema['b']
    tipos = problema['tipos_restricciones']
    for i in range(len(b)):
        rest_parts = []
        for j in range(len(A[i])):
            if A[i][j] != 0:
                coef_str = formatear_numero(A[i][j], 2)
                rest_parts.append(f"{coef_str}{nombres[j]}")
        rest_str = " + ".join(rest_parts).replace("+ -", "- ")
        b_str = formatear_numero(b[i], 2)
        print(f"  {rest_str} {tipos[i]} {b_str}")
    
    # No negatividad
    print(f"  {', '.join(nombres)} ≥ 0")


def _validar_y_preparar(problema: dict, nombre_problema: str) -> dict:
    """
    Función interna para validar las dimensiones de un problema y
    calcular num_vars y num_restricciones automáticamente.
    """
    try:
        problema['num_vars'] = len(problema['c'])
        problema['num_restricciones'] = len(problema['b'])
        assert len(problema['A']) == problema['num_restricciones']
        assert all(len(row) == problema['num_vars'] for row in problema['A'])
        assert len(problema['tipos_restricciones']) == problema['num_restricciones']
        assert len(problema['nombres_vars']) == problema['num_vars']
        # print(f"\n✅ Problema '{nombre_problema}' cargado correctamente.")
        return problema
    except (AssertionError, IndexError, TypeError) as e:
        print(f"\n❌ Error: Las dimensiones del '{nombre_problema}' en 'problema_definido.py' son inconsistentes.")
        print(f"   Detalle del error: {e}")
        return None

def obtener_problema_personalizado():
    """
    Este es un problema genérico que se puede modificar para
    realizar tus propias pruebas rápidas.
    """
    nombre = "Problema Personalizado"
    problema = {
        'tipo': 'max',
        'c': np.array([10.0, 20.0]),
        'A': np.array([
            [1.0, 2.0],
            [3.0, 2.0]
        ]),
        'b': np.array([15.0, 20.0]),
        'tipos_restricciones': ['<=', '<='],
        'nombres_vars': ['x1', 'x2'],
    }
    _mostrar_problema(problema, nombre)
    return _validar_y_preparar(problema, nombre)

def obtener_problema_dos_fases():
    """
    Prueba con minimización y restricciones mixtas ('<=', '>=', '=')
    para forzar el uso del método de dos fases.
    Solución óptima conocida: x1=5, x2=5, Z=25
    """
    nombre = "Prueba Dos Fases"
    problema = {
        'tipo': 'min',
        'c': np.array([2.0, 3.0]),
        'A': np.array([
            [0.5, 0.25],
            [1.0, 3.0],
            [1.0, 1.0]
        ]),
        'b': np.array([4.0, 20.0, 10.0]),
        'tipos_restricciones': ['<=', '>=', '='],
        'nombres_vars': ['x1', 'x2'],
    }
    _mostrar_problema(problema, nombre)
    return _validar_y_preparar(problema, nombre)

def obtener_problema_grafico_grande():
    """
    Prueba para la generación de gráficos con números grandes
    para verificar el escalado de los ejes.
    Solución óptima: x1=2000, x2=4000, Z=2,600,000
    """
    nombre = "Prueba Gráfico Grande"
    problema = {
        'tipo': 'max',
        'c': np.array([300.0, 500.0]),
        'A': np.array([
            [2.0, 1.0],
            [1.0, 2.0],
            [1.0, 0.0]
        ]),
        'b': np.array([8000.0, 10000.0, 3500.0]),
        'tipos_restricciones': ['<=', '<=', '<='],
        'nombres_vars': ['x1', 'x2'],
    }
    _mostrar_problema(problema, nombre)
    return _validar_y_preparar(problema, nombre)

def obtener_problema_multiples_variables():
    """
    Prueba con 5 variables para verificar el manejo
    de un problema de mayor dimensionalidad.
    """
    nombre = "Prueba Múltiples Variables"
    problema = {
        'tipo': 'max',
        'c': np.array([5.0, 4.0, 3.0, 7.0, 6.0]),
        'A': np.array([
            [2.0, 3.0, 1.0, 4.0, 2.0],
            [3.0, 2.0, 4.0, 1.0, 3.0],
            [4.0, 1.0, 2.0, 3.0, 1.0]
        ]),
        'b': np.array([50.0, 40.0, 60.0]),
        'tipos_restricciones': ['<=', '<=', '<='],
        'nombres_vars': ['x1', 'x2', 'x3', 'x4', 'x5'],
    }
    _mostrar_problema(problema, nombre)
    return _validar_y_preparar(problema, nombre)

def obtener_problema_infactible():
    """
    Prueba un problema sin solución factible.
    El método de dos fases debería detectar esto en la Fase 1.
    """
    nombre = "Prueba Problema Infactible"
    problema = {
        'tipo': 'max',
        'c': np.array([3.0, 2.0]),
        'A': np.array([
            [2.0, 1.0],
            [3.0, 4.0]
        ]),
        'b': np.array([2.0, 12.0]),
        'tipos_restricciones': ['<=', '>='],
        'nombres_vars': ['x1', 'x2'],
    }
    _mostrar_problema(problema, nombre)
    return _validar_y_preparar(problema, nombre)

def obtener_problema_no_acotado():
    """
    Prueba un problema con solución no acotada.
    El solver debería detectar que no hay variable saliente.
    """
    nombre = "Prueba Solución No Acotada"
    problema = {
        'tipo': 'max',
        'c': np.array([2.0, 1.0]),
        'A': np.array([
            [1.0, -1.0],
            [2.0, -1.0]
        ]),
        'b': np.array([10.0, 40.0]),
        'tipos_restricciones': ['<=', '<='],
        'nombres_vars': ['x1', 'x2'],
    }
    _mostrar_problema(problema, nombre)
    return _validar_y_preparar(problema, nombre)

def obtener_problema_multiples_optimos():
    """
    Prueba un problema con múltiples soluciones óptimas.
    El tablero final tendrá un costo reducido de cero para una variable no básica.
    """
    nombre = "Prueba Múltiples Óptimos"
    problema = {
        'tipo': 'max',
        'c': np.array([3.0, 2.0]),
        'A': np.array([
            [3.0, 2.0],
            [1.0, 0.0],
            [0.0, 1.0]
        ]),
        'b': np.array([18.0, 4.0, 6.0]),
        'tipos_restricciones': ['<=', '<=', '<='],
        'nombres_vars': ['x1', 'x2'],
    }
    _mostrar_problema(problema, nombre)
    return _validar_y_preparar(problema, nombre)