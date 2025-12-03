"""
==================================================================================
MÓDULO DE VISUALIZACIÓN GRÁFICA
==================================================================================
Funciones para crear gráficas de soluciones de problemas de PL.
==================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
from typing import List, Tuple, Optional
from utilidades import formatear_numero, mostrar_titulo


# ==================================================================================
# BÚSQUEDA DE VÉRTICES
# ==================================================================================

def encontrar_interseccion_lineas(A, b, i, j):
    """
    Encuentra la intersección entre dos líneas de restricciones.
    
    Args:
        A: Matriz de restricciones
        b: Vector de lado derecho
        i, j: Índices de las restricciones
    
    Returns:
        tuple: (x, y) o None si son paralelas
    """
    a1, a2 = A[i]
    b1 = b[i]
    a3, a4 = A[j]
    b2 = b[j]
    
    det = a1 * a4 - a2 * a3
    
    if abs(det) < 1e-9:
        return None  # Líneas paralelas
    
    x = (b1 * a4 - b2 * a2) / det
    y = (a1 * b2 - a3 * b1) / det
    
    return (x, y)


def verificar_factibilidad_punto(A, b, x1, x2):
    """
    Verifica si un punto (x1, x2) es factible.
    
    Args:
        A: Matriz de restricciones
        b: Vector de lado derecho
        x1, x2: Coordenadas del punto
    
    Returns:
        bool: True si es factible
    """
    if x1 < -1e-6 or x2 < -1e-6:
        return False
    
    punto = np.array([x1, x2])
    return np.all(A @ punto <= b + 1e-6)


def encontrar_vertices_region_factible(A, b, num_restricciones):
    """
    Encuentra los vértices de la región factible para un problema 2D.
    
    Args:
        A: Matriz de restricciones
        b: Vector de lado derecho
        num_restricciones: Número de restricciones
    
    Returns:
        list: Lista de vértices (tuplas)
    """
    vertices = [(0, 0)]
    
    # Intersecciones entre restricciones
    for i in range(num_restricciones):
        a1, a2 = A[i]
        
        # Intersección con eje x (y=0)
        if abs(a1) > 1e-9:
            x_int = b[i] / a1
            if x_int >= 0 and verificar_factibilidad_punto(A, b, x_int, 0):
                vertices.append((x_int, 0))
        
        # Intersección con eje y (x=0)
        if abs(a2) > 1e-9:
            y_int = b[i] / a2
            if y_int >= 0 and verificar_factibilidad_punto(A, b, 0, y_int):
                vertices.append((0, y_int))
        
        # Intersección con otras restricciones
        for j in range(i+1, num_restricciones):
            punto = encontrar_interseccion_lineas(A, b, i, j)
            if punto and verificar_factibilidad_punto(A, b, punto[0], punto[1]):
                vertices.append(punto)
    
    # Eliminar duplicados
    vertices_unicos = []
    for v in vertices:
        es_duplicado = False
        for vu in vertices_unicos:
            if abs(v[0] - vu[0]) < 1e-6 and abs(v[1] - vu[1]) < 1e-6:
                es_duplicado = True
                break
        if not es_duplicado:
            vertices_unicos.append(v)
    
    return vertices_unicos


def ordenar_vertices(vertices):
    """
    Ordena los vértices en sentido antihorario para formar un polígono.
    
    Args:
        vertices: Lista de vértices
    
    Returns:
        list: Vértices ordenados
    """
    if len(vertices) < 3:
        return vertices
    
    # Calcular centroide
    cx = sum(v[0] for v in vertices) / len(vertices)
    cy = sum(v[1] for v in vertices) / len(vertices)
    
    # Ordenar por ángulo desde el centroide
    def angulo(v):
        return math.atan2(v[1] - cy, v[0] - cx)
    
    return sorted(vertices, key=angulo)


# ==================================================================================
# GRAFICACIÓN
# ==================================================================================

def graficar_solucion_2d(A, b, c, solucion, valor, tipo, num_vars, num_restricciones):
    """
    Grafica la solución para problemas de 2 variables.
    
    Args:
        A: Matriz de restricciones
        b: Vector de lado derecho
        c: Vector de coeficientes de función objetivo
        solucion: Vector solución óptima
        valor: Valor óptimo de Z
        tipo: 'max' o 'min'
        num_vars: Número de variables
        num_restricciones: Número de restricciones
    """
    if num_vars != 2:
        print("\n⚠️  El método gráfico solo está disponible para problemas de 2 variables")
        return
    
    if solucion is None:
        print("\n⚠️  No hay solución óptima para graficar")
        return
    
    mostrar_titulo("SOLUCIÓN GRÁFICA")
    print("📊 Generando gráfica...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Encontrar vértices primero para calcular límites centrados
    vertices = encontrar_vertices_region_factible(A, b, num_restricciones)
    
    # Calcular límites basados en vértices y solución óptima
    if len(vertices) > 0:
        x_coords = [v[0] for v in vertices]
        y_coords = [v[1] for v in vertices]
        
        # Incluir solución óptima en el cálculo
        if solucion is not None:
            x_coords.append(solucion[0])
            y_coords.append(solucion[1])
        
        x_min_data = min(x_coords)
        x_max_data = max(x_coords)
        y_min_data = min(y_coords)
        y_max_data = max(y_coords)
        
        # Agregar margen del 20% para mejor visualización
        x_margin = (x_max_data - x_min_data) * 0.2
        y_margin = (y_max_data - y_min_data) * 0.2
        
        # Asegurar márgenes mínimos
        x_margin = max(x_margin, 1.0)
        y_margin = max(y_margin, 1.0)
        
        x_max = x_max_data + x_margin
        y_max = y_max_data + y_margin
        x_min = max(0, x_min_data - x_margin * 0.3)  # Pequeño margen izquierdo
        y_min = max(0, y_min_data - y_margin * 0.3)  # Pequeño margen inferior
    else:
        # Si no hay vértices, usar valores por defecto
        x_max = max(10, b.max() * 1.5)
        y_max = max(10, b.max() * 1.5)
        x_min = 0
        y_min = 0
    
    x = np.linspace(x_min, x_max, 400)
    
    # Colores para restricciones
    colores = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    # Graficar cada restricción
    for i in range(num_restricciones):
        a1, a2 = A[i]
        b_val = b[i]
        
        if abs(a2) > 1e-9:
            y = (b_val - a1 * x) / a2
            label = f"{formatear_numero(a1, 1)}x₁ + {formatear_numero(a2, 1)}x₂ ≤ {formatear_numero(b_val, 1)}"
            ax.plot(x, y, label=label, color=colores[i % len(colores)], linewidth=2)
            ax.fill_between(x, 0, y, where=(y >= 0), alpha=0.1, 
                           color=colores[i % len(colores)])
        else:
            # Restricción vertical
            x_val = b_val / a1 if abs(a1) > 1e-9 else 0
            ax.axvline(x=x_val, 
                      label=f"{formatear_numero(a1, 1)}x₁ ≤ {formatear_numero(b_val, 1)}", 
                      color=colores[i % len(colores)], linewidth=2)
    
    # Encontrar y dibujar región factible
    vertices = ordenar_vertices(vertices)
    
    if len(vertices) >= 3:
        poly = Polygon(vertices, alpha=0.3, facecolor='yellow', 
                     edgecolor='black', linewidth=2, label='Región Factible')
        ax.add_patch(poly)
    
    # Marcar vértices
    for v in vertices:
        ax.plot(v[0], v[1], 'ko', markersize=8)
    
    # Marcar punto óptimo
    if solucion is not None:
        ax.plot(solucion[0], solucion[1], 'r*', markersize=20, 
               label=f'Óptimo ({formatear_numero(solucion[0])}, {formatear_numero(solucion[1])})',
               zorder=5)
        
        # Línea de nivel de la función objetivo
        c1, c2 = c[:2]
        Z_opt = valor
        
        if abs(c2) > 1e-9:
            y_obj = (Z_opt - c1 * x) / c2
            ax.plot(x, y_obj, 'r--', linewidth=2, alpha=0.7,
                   label=f'Z = {formatear_numero(c1, 1)}x₁ + {formatear_numero(c2, 1)}x₂ = {formatear_numero(Z_opt)}')
    
    # Configuración de ejes con límites centrados
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('x₁', fontsize=12, fontweight='bold')
    ax.set_ylabel('x₂', fontsize=12, fontweight='bold')
    ax.set_title(f'Solución Gráfica - Programación Lineal\n{tipo.upper()}IMIZAR Z = {formatear_numero(c[0], 1)}x₁ + {formatear_numero(c[1], 1)}x₂',
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    
    plt.tight_layout()
    
    # Guardar gráfica
    nombre_archivo = 'solucion_grafica_pl.png'
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfica guardada como: {nombre_archivo}")
    
    plt.show()
