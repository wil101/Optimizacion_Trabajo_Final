"""
==================================================================================
PAQUETE: SOLUCIONADOR DE PROGRAMACIÓN LINEAL
==================================================================================
Método Simplex Revisado con visualización mejorada.
==================================================================================
"""

__version__ = '2.0.0'
__author__ = 'Wilmar Osorio y Santiago Alexander Losada'

# Importaciones principales para facilitar el uso del paquete
from .utilidades import Colores, formatear_numero
from .manejo_consola import (
    mostrar_menu_principal,
    ingresar_problema_completo,
    confirmar_accion
)
from .resolucion_simplex import (
    resolver_simplex_revisado,
    validar_factibilidad,
    mostrar_solucion_final
)
from .visualizacion_grafica import graficar_solucion_2d
from .exportacion_resultados import guardar_resultado_txt

__all__ = [
    'Colores',
    'formatear_numero',
    'mostrar_menu_principal',
    'ingresar_problema_completo',
    'confirmar_accion',
    'resolver_simplex_revisado',
    'validar_factibilidad',
    'mostrar_solucion_final',
    'graficar_solucion_2d',
    'guardar_resultado_txt'
]
