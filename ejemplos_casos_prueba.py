"""
==================================================================================
CASOS DE PRUEBA PARA EL SOLUCIONADOR DE PROGRAMACIÓN LINEAL
==================================================================================
Este archivo contiene ejemplos de problemas de PL que puedes usar para probar
la aplicación. Incluye la entrada que debes proporcionar y la solución esperada.
==================================================================================
"""
import numpy as np

# ==============================================================================
# CASO COMPLEJO (MINIMIZACIÓN CON RESTRICCIONES MIXTAS)
# ==============================================================================
def generar_problema_complejo():
    """
    Genera el problema complejo con restricciones mixtas.
    Minimizar Z = 0.4x1 + 0.5x2
    S.A.
    0.3x1 + 0.1x2 <= 2.7
    0.5x1 + 0.5x2 = 6
    0.6x1 + 0.4x2 >= 6
    """
    print("\nCargando problema complejo:")
    print("Función Objetivo: Minimizar Z = 0.4x₁ + 0.5x₂")
    print("\nRestricciones:")
    print("  0.3x₁ + 0.1x₂ ≤ 2.7")
    print("  0.5x₁ + 0.5x₂ = 6")
    print("  0.6x₁ + 0.4x₂ ≥ 6")
    print("  x₁, x₂ ≥ 0")
    
    return {
        'tipo': 'min',
        'c': np.array([0.4, 0.5]),
        'A': np.array([
            [0.3, 0.1],
            [0.5, 0.5],
            [0.6, 0.4]
        ]),
        'b': np.array([2.7, 6, 6]),
        'tipos_restricciones': ['<=', '=', '>='],
        'num_vars': 2,
        'num_restricciones': 3,
        'nombres_vars': ['x1', 'x2']
    }


# ==============================================================================
# CASO 1: Problema Clásico 2D - FACTIBLE Y ACOTADO
# ==============================================================================
"""
ENTRADA:
- Tipo: max
- Variables: 2
- Coeficientes función objetivo: 3 5
- Restricciones: 3
  - 1 0 <= 4
  - 0 2 <= 12
  - 3 2 <= 18

SOLUCIÓN ESPERADA:
- x1 = 2.0
- x2 = 6.0
- Z máximo = 36.0

INTERPRETACIÓN:
Problema factible con solución única en el vértice (2, 6).
La restricción x₁ ≤ 4 no es activa en la solución óptima.
"""

# ==============================================================================
# CASO 2: Problema 2D - VÉRTICE EN EL ORIGEN
# ==============================================================================
"""
ENTRADA:
- Tipo: max
- Variables: 2
- Coeficientes función objetivo: 1 1
- Restricciones: 2
  - 1 1 <= 0
  - 1 0 <= 0

SOLUCIÓN ESPERADA:
- x1 = 0.0
- x2 = 0.0
- Z máximo = 0.0

INTERPRETACIÓN:
La región factible se reduce al origen.
"""

# ==============================================================================
# CASO 3: Problema 3D - FACTIBLE
# ==============================================================================
"""
ENTRADA:
- Tipo: max
- Variables: 3
- Coeficientes función objetivo: 2 3 4
- Restricciones: 3
  - 1 1 1 <= 10
  - 2 1 0 <= 12
  - 0 1 2 <= 14

SOLUCIÓN ESPERADA:
Aproximadamente:
- x1 ≈ 0.0
- x2 ≈ 3.0
- x3 ≈ 5.5
- Z máximo ≈ 31.0

INTERPRETACIÓN:
Problema 3D con solución en un vértice del poliedro factible.
"""

# ==============================================================================
# CASO 4: Problema de MINIMIZACIÓN
# ==============================================================================
"""
ENTRADA:
- Tipo: min
- Variables: 2
- Coeficientes función objetivo: 2 3
- Restricciones: 2
  - 1 1 <= 10
  - 2 1 <= 15

SOLUCIÓN ESPERADA:
- x1 = 0.0
- x2 = 0.0
- Z mínimo = 0.0

INTERPRETACIÓN:
En minimización, el óptimo suele estar en el vértice más cercano al origen
si las restricciones lo permiten.
"""

# ==============================================================================
# CASO 5: Problema con MÚLTIPLES RESTRICCIONES ACTIVAS
# ==============================================================================
"""
ENTRADA:
- Tipo: max
- Variables: 2
- Coeficientes función objetivo: 5 4
- Restricciones: 4
  - 1 0 <= 5
  - 0 1 <= 4
  - 1 1 <= 8
  - 2 1 <= 10

SOLUCIÓN ESPERADA:
- x1 = 4.0
- x2 = 4.0
- Z máximo = 36.0

INTERPRETACIÓN:
Varias restricciones son activas (se cumplen con igualdad) en el óptimo.
"""

# ==============================================================================
# CASO 6: Problema REDUNDANTE
# ==============================================================================
"""
ENTRADA:
- Tipo: max
- Variables: 2
- Coeficientes función objetivo: 3 2
- Restricciones: 3
  - 1 1 <= 10
  - 2 2 <= 20  (Esta es redundante: 2*(x₁ + x₂) ≤ 20 → x₁ + x₂ ≤ 10)
  - 1 0 <= 8

SOLUCIÓN ESPERADA:
- x1 = 8.0
- x2 = 2.0
- Z máximo = 28.0

INTERPRETACIÓN:
La segunda restricción es redundante (no afecta la región factible).
"""

# ==============================================================================
# CASO 7: Problema con COEFICIENTES DECIMALES
# ==============================================================================
"""
ENTRADA:
- Tipo: max
- Variables: 2
- Coeficientes función objetivo: 2.5 3.5
- Restricciones: 2
  - 0.5 1 <= 8
  - 1 0.5 <= 9

SOLUCIÓN ESPERADA:
Aproximadamente:
- x1 ≈ 6.0
- x2 ≈ 5.0
- Z máximo ≈ 32.5

INTERPRETACIÓN:
El programa maneja correctamente coeficientes decimales.
"""

# ==============================================================================
# CASO 8: Problema SIMPLE (Una sola restricción)
# ==============================================================================
"""
ENTRADA:
- Tipo: max
- Variables: 2
- Coeficientes función objetivo: 1 2
- Restricciones: 1
  - 1 1 <= 5

SOLUCIÓN ESPERADA:
- x1 = 0.0
- x2 = 5.0
- Z máximo = 10.0

INTERPRETACIÓN:
Con una sola restricción, el óptimo está en el eje x₂.
"""

# ==============================================================================
# INSTRUCCIONES DE USO
# ==============================================================================
"""
CÓMO USAR ESTOS CASOS DE PRUEBA:

1. Ejecuta el programa: python mian.py
2. Selecciona opción 1 (Ingresar problema manualmente)
3. Copia los valores de ENTRADA de cualquier caso
4. Compara el resultado con la SOLUCIÓN ESPERADA

NOTA: Los valores pueden tener pequeñas diferencias debido a:
- Precisión numérica (≈ 4 decimales)
- Método de resolución
- Redondeo de operaciones matriciales

Se considera correcto si la diferencia es menor a 0.01
"""

# ==============================================================================
# CASOS NO IMPLEMENTADOS (Requieren extensiones)
# ==============================================================================
"""
Los siguientes casos NO funcionarán con la versión actual:

1. PROBLEMA NO ACOTADO:
   max Z = x₁ + x₂
   s.a. -x₁ + x₂ ≤ 1
   (Nota: Requiere restricciones >= o coeficientes negativos especiales)

2. PROBLEMA INFACTIBLE:
   max Z = x₁ + x₂
   s.a. x₁ + x₂ ≤ 5
        x₁ + x₂ ≥ 10
   (Nota: Requiere soporte para >= nativo, no solo conversión)

3. MÉTODO DE DOS FASES:
   Problemas que requieren variables artificiales
   (No implementado en esta versión)
"""
