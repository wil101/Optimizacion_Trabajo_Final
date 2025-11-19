"""
==================================================================================
SOLUCIONADOR DE PROGRAMACIÓN LINEAL - MÉTODO SIMPLEX REVISADO
==================================================================================
Aplicación completa para resolver problemas de PL paso a paso.
Autor: Wilmar Osorio y Santiago Alexander Losada
Fecha: Noviembre 2025
==================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
import os
from typing import List, Tuple, Dict, Optional
import sys

np.set_printoptions(precision=4, suppress=True)


# ==================================================================================
# CLASE PRINCIPAL: PROBLEMA DE PROGRAMACIÓN LINEAL
# ==================================================================================

class ProgramacionLineal:
    """
    Clase que representa y resuelve un problema de programación lineal
    usando el Método Simplex Revisado.
    """
    
    def __init__(self):
        self.c = None  # Coeficientes de la función objetivo
        self.A = None  # Matriz de restricciones
        self.b = None  # Lado derecho de las restricciones
        self.tipo = 'max'  # 'max' o 'min'
        self.num_vars = 0  # Número de variables de decisión
        self.num_restricciones = 0
        self.nombres_vars = []
        self.historia_tableros = []  # Para guardar cada iteración
        self.solucion_optima = None
        self.valor_optimo = None
        self.estado = None  # 'optimo', 'no_acotado', 'infactible'
        
    def generar_problema_ejemplo(self, num_vars: int = None) -> None:
        """
        Genera un problema de ejemplo aleatorio.
        Si num_vars no se especifica, elige aleatoriamente entre 2 o 3 variables.
        """
        if num_vars is None:
            num_vars = random.choice([2, 3])
        
        print(f"\n{'='*80}")
        print(f"  GENERANDO PROBLEMA DE EJEMPLO CON {num_vars} VARIABLES")
        print(f"{'='*80}\n")
        
        if num_vars == 2:
            # Ejemplo clásico de 2 variables
            self.tipo = 'max'
            self.c = np.array([3.0, 5.0])
            self.A = np.array([
                [1.0, 0.0],
                [0.0, 2.0],
                [3.0, 2.0]
            ])
            self.b = np.array([4.0, 12.0, 18.0])
            self.nombres_vars = ['x1', 'x2']
            
            print("Función Objetivo: Maximizar Z = 3x₁ + 5x₂")
            print("\nRestricciones:")
            print("  x₁ ≤ 4")
            print("  2x₂ ≤ 12")
            print("  3x₁ + 2x₂ ≤ 18")
            print("  x₁, x₂ ≥ 0")
            
        else:  # 3 variables
            self.tipo = 'max'
            self.c = np.array([2.0, 3.0, 4.0])
            self.A = np.array([
                [1.0, 1.0, 1.0],
                [2.0, 1.0, 0.0],
                [0.0, 1.0, 2.0]
            ])
            self.b = np.array([10.0, 12.0, 14.0])
            self.nombres_vars = ['x1', 'x2', 'x3']
            
            print("Función Objetivo: Maximizar Z = 2x₁ + 3x₂ + 4x₃")
            print("\nRestricciones:")
            print("  x₁ + x₂ + x₃ ≤ 10")
            print("  2x₁ + x₂ ≤ 12")
            print("  x₂ + 2x₃ ≤ 14")
            print("  x₁, x₂, x₃ ≥ 0")
        
        self.num_vars = num_vars
        self.num_restricciones = len(self.b)
    
    def ingresar_problema_manual(self) -> bool:
        """
        Permite al usuario ingresar un problema manualmente desde consola.
        Retorna True si se ingresó correctamente, False si se cancela.
        """
        try:
            print(f"\n{'='*80}")
            print("  INGRESO MANUAL DE PROBLEMA DE PROGRAMACIÓN LINEAL")
            print(f"{'='*80}\n")
            
            # Tipo de optimización
            while True:
                tipo = input("¿Desea MAXIMIZAR o MINIMIZAR? (max/min): ").strip().lower()
                if tipo in ['max', 'min']:
                    self.tipo = tipo
                    break
                print("⚠️  Por favor ingrese 'max' o 'min'")
            
            # Número de variables
            while True:
                try:
                    num_vars = int(input("\n¿Cuántas variables tiene el problema? (2 o 3 recomendado): "))
                    if num_vars > 0:
                        self.num_vars = num_vars
                        self.nombres_vars = [f'x{i+1}' for i in range(num_vars)]
                        break
                    print("⚠️  Debe ser un número positivo")
                except ValueError:
                    print("⚠️  Por favor ingrese un número válido")
            
            # Coeficientes de la función objetivo
            print(f"\nIngrese los coeficientes de la función objetivo (separados por espacio):")
            print(f"Ejemplo para Z = 3x₁ + 5x₂: ingrese '3 5'")
            while True:
                try:
                    coef_str = input(f"Coeficientes ({' '.join(self.nombres_vars)}): ")
                    coef = [float(x) for x in coef_str.split()]
                    if len(coef) == num_vars:
                        self.c = np.array(coef)
                        break
                    print(f"⚠️  Debe ingresar exactamente {num_vars} coeficientes")
                except ValueError:
                    print("⚠️  Por favor ingrese números válidos separados por espacio")
            
            # Número de restricciones
            while True:
                try:
                    num_rest = int(input(f"\n¿Cuántas restricciones tiene el problema? "))
                    if num_rest > 0:
                        self.num_restricciones = num_rest
                        break
                    print("⚠️  Debe ser un número positivo")
                except ValueError:
                    print("⚠️  Por favor ingrese un número válido")
            
            # Ingresar cada restricción
            A_list = []
            b_list = []
            
            print(f"\nIngrese cada restricción en formato: coeficientes tipo valor")
            print(f"Ejemplo para 2x₁ + 3x₂ ≤ 10: ingrese '2 3 <= 10'")
            print(f"Tipos permitidos: <= (menor o igual), >= (mayor o igual), = (igual)\n")
            
            for i in range(num_rest):
                while True:
                    try:
                        rest_str = input(f"Restricción {i+1}: ")
                        partes = rest_str.split()
                        
                        # Buscar el tipo de desigualdad
                        tipo_idx = -1
                        tipo_rest = None
                        for idx, parte in enumerate(partes):
                            if parte in ['<=', '>=', '=']:
                                tipo_idx = idx
                                tipo_rest = parte
                                break
                        
                        if tipo_idx == -1:
                            print("⚠️  Debe incluir <=, >= o =")
                            continue
                        
                        coef = [float(x) for x in partes[:tipo_idx]]
                        valor = float(partes[tipo_idx + 1])
                        
                        if len(coef) != num_vars:
                            print(f"⚠️  Debe ingresar {num_vars} coeficientes")
                            continue
                        
                        # Por ahora solo soportamos <=
                        if tipo_rest == '<=':
                            A_list.append(coef)
                            b_list.append(valor)
                        elif tipo_rest == '>=':
                            # Multiplicamos por -1 para convertir a <=
                            A_list.append([-c for c in coef])
                            b_list.append(-valor)
                        else:  # =
                            # Por simplicidad, tratamos = como <=
                            print("⚠️  Nota: restricciones de igualdad se tratan como ≤ en esta versión")
                            A_list.append(coef)
                            b_list.append(valor)
                        
                        break
                        
                    except (ValueError, IndexError):
                        print("⚠️  Formato inválido. Intente nuevamente")
            
            self.A = np.array(A_list)
            self.b = np.array(b_list)
            
            print("\n✅ Problema ingresado correctamente!")
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Ingreso cancelado por el usuario")
            return False
    
    def validar_factibilidad(self) -> str:
        """
        Valida si el problema es factible, infactible o no acotado.
        Retorna: 'factible', 'infactible' o 'potencialmente_no_acotado'
        """
        print(f"\n{'='*80}")
        print("  VALIDACIÓN DE FACTIBILIDAD")
        print(f"{'='*80}\n")
        
        # Verificar si b tiene valores negativos (infactible obvio)
        if np.any(self.b < 0):
            print("❌ PROBLEMA INFACTIBLE: Lado derecho con valores negativos")
            return 'infactible'
        
        # Verificar si existe al menos una solución trivial (todas las variables en 0)
        if np.all(self.b >= 0):
            print("✅ El problema tiene al menos la solución trivial (todas las variables = 0)")
            print("✅ El problema es FACTIBLE")
            return 'factible'
        
        print("⚠️  Se requiere análisis adicional durante la ejecución del simplex")
        return 'factible'
    
    def resolver_simplex_revisado(self) -> None:
        """
        Resuelve el problema usando el Método Simplex Revisado.
        Muestra cada iteración del tablero paso a paso.
        """
        print(f"\n{'='*80}")
        print("  RESOLUCIÓN POR MÉTODO SIMPLEX REVISADO")
        print(f"{'='*80}\n")
        
        # Convertir minimización a maximización
        c = self.c.copy()
        if self.tipo == 'min':
            c = -c
            print("🔄 Convirtiendo minimización a maximización (c = -c)\n")
        
        # Configuración inicial
        m, n = self.A.shape  # m restricciones, n variables
        
        # Agregar variables de holgura
        A_extended = np.hstack([self.A, np.eye(m)])
        c_extended = np.hstack([c, np.zeros(m)])
        
        # Base inicial: variables de holgura
        base = list(range(n, n + m))
        no_base = list(range(n))
        
        iteracion = 0
        self.historia_tableros = []
        
        print("📋 Configuración Inicial:")
        print(f"   Variables de decisión: {n}")
        print(f"   Restricciones: {m}")
        print(f"   Variables de holgura: {m}")
        print(f"   Total de variables: {n + m}")
        print(f"   Base inicial: s{1} a s{m} (variables de holgura)\n")
        
        while True:
            iteracion += 1
            print(f"\n{'─'*80}")
            print(f"  ITERACIÓN {iteracion}")
            print(f"{'─'*80}\n")
            
            # Construir matriz B (matriz básica)
            B = A_extended[:, base]
            
            # Calcular B^(-1)
            try:
                B_inv = np.linalg.inv(B)
            except np.linalg.LinAlgError:
                print("❌ ERROR: Matriz básica singular")
                self.estado = 'infactible'
                return
            
            # Vector de costos básicos
            c_B = c_extended[base]
            
            # Solución básica actual
            x_B = B_inv @ self.b
            
            # Verificar factibilidad
            if np.any(x_B < -1e-9):
                print("❌ PROBLEMA INFACTIBLE: Solución básica con valores negativos")
                self.estado = 'infactible'
                return
            
            # Valor de Z
            Z = c_B @ x_B
            
            # Calcular costos reducidos para variables no básicas
            costos_reducidos = np.zeros(n + m)
            for j in range(n + m):
                if j not in base:
                    costos_reducidos[j] = c_extended[j] - c_B @ (B_inv @ A_extended[:, j])
            
            # Mostrar tablero simplex revisado
            self.mostrar_tablero_revisado(iteracion, base, no_base, B_inv, A_extended, 
                                         c_B, c_extended, x_B, Z, costos_reducidos, n)
            
            # Test de optimalidad
            if np.all(costos_reducidos <= 1e-9):
                print("\n" + "="*80)
                print("  ✅ ¡SOLUCIÓN ÓPTIMA ENCONTRADA!")
                print("="*80)
                self.estado = 'optimo'
                
                # Guardar solución
                solucion = np.zeros(n + m)
                solucion[base] = x_B
                self.solucion_optima = solucion[:n]  # Solo variables de decisión
                self.valor_optimo = Z if self.tipo == 'max' else -Z
                
                self.mostrar_solucion_final()
                break
            
            # Seleccionar variable entrante (mayor costo reducido positivo)
            idx_entrante = np.argmax(costos_reducidos)
            if costos_reducidos[idx_entrante] <= 1e-9:
                print("\n✅ Solución óptima alcanzada")
                self.estado = 'optimo'
                break
            
            var_entrante = idx_entrante
            nombre_entrante = self.obtener_nombre_variable(var_entrante, n)
            
            print(f"\n🔵 Variable entrante: {nombre_entrante} (columna {var_entrante})")
            print(f"   Costo reducido: {costos_reducidos[var_entrante]:.4f}")
            
            # Calcular dirección
            y = B_inv @ A_extended[:, var_entrante]
            
            # Test de acotamiento
            if np.all(y <= 1e-9):
                print("\n" + "="*80)
                print("  ⚠️  PROBLEMA NO ACOTADO")
                print("="*80)
                print("\nTodas las componentes de la dirección son ≤ 0")
                print("La función objetivo puede crecer indefinidamente")
                self.estado = 'no_acotado'
                return
            
            # Calcular ratios para test de la razón mínima
            ratios = []
            for i in range(m):
                if y[i] > 1e-9:
                    ratios.append((x_B[i] / y[i], i))
                else:
                    ratios.append((float('inf'), i))
            
            # Seleccionar variable saliente (menor ratio)
            ratio_min, idx_saliente = min(ratios)
            
            if ratio_min == float('inf'):
                print("\n⚠️  PROBLEMA NO ACOTADO")
                self.estado = 'no_acotado'
                return
            
            var_saliente = base[idx_saliente]
            nombre_saliente = self.obtener_nombre_variable(var_saliente, n)
            
            print(f"🔴 Variable saliente: {nombre_saliente} (posición {idx_saliente} en base)")
            print(f"   Ratio mínimo: {ratio_min:.4f}")
            
            # Actualizar base
            base[idx_saliente] = var_entrante
            
            # Actualizar lista de no básicas
            no_base = [i for i in range(n + m) if i not in base]
            
            print(f"\n📊 Nueva base: {[self.obtener_nombre_variable(v, n) for v in base]}")
            
            # Pausa para visualización
            input("\n⏸️  Presione ENTER para continuar a la siguiente iteración...")
            
            # Límite de iteraciones (seguridad)
            if iteracion > 50:
                print("\n⚠️  Límite de iteraciones alcanzado")
                break
    
    def mostrar_tablero_revisado(self, iteracion, base, no_base, B_inv, A, c_B, c, x_B, Z, 
                                costos_reducidos, n):
        """
        Muestra el tablero simplex revisado en el formato estándar:
        
        [ 1 | C_B * B⁻¹ * A - C | C_B * B⁻¹ | C_B * B⁻¹ * b ]
        [ 0 |    B⁻¹ * A       |    B⁻¹    |    B⁻¹ * b    ]
        """
        m = len(base)
        total_vars = len(c)
        
        print("┌" + "─"*78 + "┐")
        print(f"│ {'TABLERO SIMPLEX REVISADO - ITERACIÓN ' + str(iteracion):^76} │")
        print("└" + "─"*78 + "┘\n")
        
        # Encabezados
        headers = ['Z'] + [self.obtener_nombre_variable(i, n) for i in range(total_vars)] + \
                  ['π'] + ['LD']
        
        # Calcular B_inv * A
        B_inv_A = B_inv @ A
        
        # Primera fila: [ 1 | C_B * B⁻¹ * A - C | C_B * B⁻¹ | C_B * B⁻¹ * b ]
        fila_Z = [1]  # Z
        
        # C_B * B⁻¹ * A - C para cada variable
        for j in range(total_vars):
            valor = c_B @ (B_inv @ A[:, j]) - c[j]
            fila_Z.append(-valor)  # Negativo para mostrar costos reducidos correctamente
        
        # C_B * B⁻¹ (variables duales π)
        pi = c_B @ B_inv
        fila_Z.extend(pi)
        
        # C_B * B⁻¹ * b (valor de Z)
        fila_Z.append(Z)
        
        # Filas de restricciones: [ 0 | B⁻¹ * A | B⁻¹ | B⁻¹ * b ]
        filas_rest = []
        for i in range(m):
            fila = [0]  # Columna Z
            
            # B⁻¹ * A
            fila.extend(B_inv_A[i, :])
            
            # B⁻¹
            fila.extend(B_inv[i, :])
            
            # B⁻¹ * b
            fila.append(x_B[i])
            
            filas_rest.append(fila)
        
        # Construir tabla
        print("  Var. Base │ ", end="")
        for h in headers:
            print(f"{h:>8}", end=" ")
        print()
        print("  " + "─"*10 + "┼" + "─"*(9 * len(headers)))
        
        # Fila Z
        print(f"  {'Z':^10}│ ", end="")
        for val in fila_Z:
            print(f"{val:8.3f}", end=" ")
        print()
        
        # Filas de restricciones
        for i, fila in enumerate(filas_rest):
            var_base = self.obtener_nombre_variable(base[i], n)
            print(f"  {var_base:^10}│ ", end="")
            for val in fila:
                print(f"{val:8.3f}", end=" ")
            print()
        
        print("\n  Leyenda:")
        print(f"    Z: Función objetivo = {Z:.4f}")
        print(f"    π: Variables duales (precios sombra)")
        print(f"    LD: Lado derecho (valores de variables básicas)")
        print(f"    Base actual: {[self.obtener_nombre_variable(v, n) for v in base]}")
    
    def obtener_nombre_variable(self, idx: int, n_decision: int) -> str:
        """Retorna el nombre de una variable según su índice."""
        if idx < n_decision:
            return f"x{idx+1}"
        else:
            return f"s{idx - n_decision + 1}"
    
    def mostrar_solucion_final(self) -> None:
        """Muestra la solución óptima encontrada."""
        print("\n┌" + "─"*78 + "┐")
        print(f"│ {'SOLUCIÓN ÓPTIMA':^76} │")
        print("└" + "─"*78 + "┘\n")
        
        print("  Variables de decisión:")
        for i, nombre in enumerate(self.nombres_vars):
            print(f"    {nombre} = {self.solucion_optima[i]:.4f}")
        
        objetivo = "Máximo" if self.tipo == 'max' else "Mínimo"
        print(f"\n  {objetivo} valor de Z = {self.valor_optimo:.4f}")
        
        print("\n  Interpretación:")
        print(f"    El valor {'máximo' if self.tipo == 'max' else 'mínimo'} de la función")
        print(f"    objetivo es {self.valor_optimo:.4f}, alcanzado en el punto:")
        punto = ', '.join([f"{self.nombres_vars[i]}={self.solucion_optima[i]:.4f}" 
                          for i in range(len(self.nombres_vars))])
        print(f"    ({punto})")
    
    def graficar_solucion_2d(self) -> None:
        """
        Grafica la solución para problemas de 2 variables.
        Muestra restricciones, región factible y punto óptimo.
        """
        if self.num_vars != 2:
            print("\n⚠️  El método gráfico solo está disponible para problemas de 2 variables")
            return
        
        if self.solucion_optima is None:
            print("\n⚠️  No hay solución óptima para graficar")
            return
        
        print(f"\n{'='*80}")
        print("  SOLUCIÓN GRÁFICA")
        print(f"{'='*80}\n")
        print("📊 Generando gráfica...")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Rango de graficación
        x_max = max(10, self.b.max() * 1.5)
        y_max = max(10, self.b.max() * 1.5)
        
        x = np.linspace(0, x_max, 400)
        
        # Graficar cada restricción
        colores = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
        
        for i in range(self.num_restricciones):
            a1, a2 = self.A[i]
            b_val = self.b[i]
            
            # Calcular y desde la ecuación a1*x1 + a2*x2 = b
            if abs(a2) > 1e-9:
                y = (b_val - a1 * x) / a2
                label = f"{a1:.1f}x₁ + {a2:.1f}x₂ ≤ {b_val:.1f}"
                ax.plot(x, y, label=label, color=colores[i % len(colores)], linewidth=2)
                
                # Sombrear región factible
                ax.fill_between(x, 0, y, where=(y >= 0), alpha=0.1, 
                               color=colores[i % len(colores)])
            else:
                # Restricción vertical
                x_val = b_val / a1 if abs(a1) > 1e-9 else 0
                ax.axvline(x=x_val, label=f"{a1:.1f}x₁ ≤ {b_val:.1f}", 
                          color=colores[i % len(colores)], linewidth=2)
        
        # Encontrar vértices de la región factible
        vertices = self.encontrar_vertices_region_factible()
        
        if len(vertices) > 0:
            # Ordenar vértices para formar polígono
            vertices = self.ordenar_vertices(vertices)
            
            # Dibujar región factible
            if len(vertices) >= 3:
                poly = Polygon(vertices, alpha=0.3, facecolor='yellow', 
                             edgecolor='black', linewidth=2, label='Región Factible')
                ax.add_patch(poly)
            
            # Marcar vértices
            for v in vertices:
                ax.plot(v[0], v[1], 'ko', markersize=8)
        
        # Marcar punto óptimo
        if self.solucion_optima is not None:
            ax.plot(self.solucion_optima[0], self.solucion_optima[1], 
                   'r*', markersize=20, label=f'Óptimo ({self.solucion_optima[0]:.2f}, {self.solucion_optima[1]:.2f})',
                   zorder=5)
            
            # Línea de nivel de la función objetivo
            c1, c2 = self.c[:2]
            Z_opt = self.valor_optimo
            
            if abs(c2) > 1e-9:
                y_obj = (Z_opt - c1 * x) / c2
                ax.plot(x, y_obj, 'r--', linewidth=2, alpha=0.7,
                       label=f'Z = {c1:.1f}x₁ + {c2:.1f}x₂ = {Z_opt:.2f}')
        
        # Configuración de ejes
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, y_max)
        ax.set_xlabel('x₁', fontsize=12, fontweight='bold')
        ax.set_ylabel('x₂', fontsize=12, fontweight='bold')
        ax.set_title(f'Solución Gráfica - Programación Lineal\n{self.tipo.upper()}IMIZAR Z = {self.c[0]}x₁ + {self.c[1]}x₂',
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
    
    def encontrar_vertices_region_factible(self) -> List[Tuple[float, float]]:
        """
        Encuentra los vértices de la región factible para un problema 2D.
        """
        vertices = []
        
        # Intersección con ejes
        vertices.append((0, 0))
        
        # Intersecciones entre restricciones
        for i in range(self.num_restricciones):
            # Intersección con eje x (y=0)
            a1, a2 = self.A[i]
            if abs(a1) > 1e-9:
                x_int = self.b[i] / a1
                if x_int >= 0 and self.es_factible(x_int, 0):
                    vertices.append((x_int, 0))
            
            # Intersección con eje y (x=0)
            if abs(a2) > 1e-9:
                y_int = self.b[i] / a2
                if y_int >= 0 and self.es_factible(0, y_int):
                    vertices.append((0, y_int))
            
            # Intersección con otras restricciones
            for j in range(i+1, self.num_restricciones):
                punto = self.interseccion_lineas(i, j)
                if punto and self.es_factible(punto[0], punto[1]):
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
    
    def interseccion_lineas(self, i: int, j: int) -> Optional[Tuple[float, float]]:
        """
        Encuentra la intersección entre dos líneas de restricciones.
        """
        a1, a2 = self.A[i]
        b1 = self.b[i]
        a3, a4 = self.A[j]
        b2 = self.b[j]
        
        det = a1 * a4 - a2 * a3
        
        if abs(det) < 1e-9:
            return None  # Líneas paralelas
        
        x = (b1 * a4 - b2 * a2) / det
        y = (a1 * b2 - a3 * b1) / det
        
        return (x, y)
    
    def es_factible(self, x1: float, x2: float) -> bool:
        """
        Verifica si un punto (x1, x2) es factible.
        """
        if x1 < -1e-6 or x2 < -1e-6:
            return False
        
        punto = np.array([x1, x2])
        return np.all(self.A @ punto <= self.b + 1e-6)
    
    def ordenar_vertices(self, vertices: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Ordena los vértices en sentido antihorario para formar un polígono.
        """
        if len(vertices) < 3:
            return vertices
        
        # Calcular centroide
        cx = sum(v[0] for v in vertices) / len(vertices)
        cy = sum(v[1] for v in vertices) / len(vertices)
        
        # Ordenar por ángulo desde el centroide
        import math
        def angulo(v):
            return math.atan2(v[1] - cy, v[0] - cx)
        
        return sorted(vertices, key=angulo)
    
    def guardar_resultado(self, nombre_archivo: str = "resultado_pl.txt") -> None:
        """
        Guarda el resultado en un archivo de texto.
        """
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write(" RESULTADO DE PROGRAMACIÓN LINEAL - MÉTODO SIMPLEX REVISADO\n")
                f.write("="*80 + "\n\n")
                
                # Problema
                f.write("PROBLEMA ORIGINAL:\n")
                f.write("-"*80 + "\n")
                objetivo = "Maximizar" if self.tipo == 'max' else "Minimizar"
                f.write(f"{objetivo} Z = ")
                terminos = [f"{self.c[i]}{self.nombres_vars[i]}" for i in range(self.num_vars)]
                f.write(" + ".join(terminos) + "\n\n")
                
                f.write("Sujeto a:\n")
                for i in range(self.num_restricciones):
                    terminos = [f"{self.A[i,j]}{self.nombres_vars[j]}" 
                              for j in range(self.num_vars)]
                    f.write(f"  {' + '.join(terminos)} ≤ {self.b[i]}\n")
                
                f.write(f"  {', '.join(self.nombres_vars)} ≥ 0\n\n")
                
                # Solución
                if self.estado == 'optimo':
                    f.write("SOLUCIÓN ÓPTIMA:\n")
                    f.write("-"*80 + "\n")
                    for i, nombre in enumerate(self.nombres_vars):
                        f.write(f"  {nombre} = {self.solucion_optima[i]:.6f}\n")
                    f.write(f"\n  Valor {'máximo' if self.tipo == 'max' else 'mínimo'} de Z = {self.valor_optimo:.6f}\n")
                elif self.estado == 'no_acotado':
                    f.write("RESULTADO: Problema NO ACOTADO\n")
                elif self.estado == 'infactible':
                    f.write("RESULTADO: Problema INFACTIBLE\n")
                
                f.write("\n" + "="*80 + "\n")
            
            print(f"\n✅ Resultado guardado en: {nombre_archivo}")
        
        except Exception as e:
            print(f"\n❌ Error al guardar archivo: {e}")


# ==================================================================================
# FUNCIÓN PRINCIPAL
# ==================================================================================

def menu_principal():
    """
    Menú principal de la aplicación.
    """
    print("\n")
    print("="*80)
    print(" "*20 + "SOLUCIONADOR DE PROGRAMACIÓN LINEAL")
    print(" "*25 + "Método Simplex Revisado")
    print("="*80)
    print("\n  Desarrollado para resolver problemas de PL paso a paso")
    print("  Muestra cada iteración del tablero simplex y solución gráfica (2D)\n")
    print("="*80)
    
    pl = ProgramacionLineal()
    
    # Opción de ingreso
    print("\n📝 OPCIONES DE INGRESO:")
    print("  1. Ingresar problema manualmente")
    print("  2. Usar problema de ejemplo (2 o 3 variables aleatorio)")
    print("  3. Salir")
    
    while True:
        opcion = input("\n Seleccione una opción (1-3): ").strip()
        
        if opcion == '1':
            if not pl.ingresar_problema_manual():
                continue
            break
        elif opcion == '2':
            pl.generar_problema_ejemplo()
            break
        elif opcion == '3':
            print("\n👋 ¡Hasta pronto!")
            return
        else:
            print("⚠️  Opción inválida. Intente nuevamente.")
    
    # Validar factibilidad
    estado = pl.validar_factibilidad()
    
    if estado == 'infactible':
        print("\n❌ No se puede resolver un problema infactible")
        return
    
    # Resolver
    input("\n⏸️  Presione ENTER para iniciar la resolución por Método Simplex...")
    pl.resolver_simplex_revisado()
    
    # Si hay solución óptima y es 2D, ofrecer gráfica
    if pl.estado == 'optimo' and pl.num_vars == 2:
        print("\n" + "="*80)
        resp = input("\n¿Desea ver la solución gráfica? (s/n): ").strip().lower()
        if resp == 's':
            pl.graficar_solucion_2d()
    
    # Guardar resultado
    print("\n" + "="*80)
    resp = input("\n¿Desea guardar el resultado en un archivo? (s/n): ").strip().lower()
    if resp == 's':
        nombre = input("Nombre del archivo (Enter para 'resultado_pl.txt'): ").strip()
        if not nombre:
            nombre = "resultado_pl.txt"
        if not nombre.endswith('.txt'):
            nombre += '.txt'
        pl.guardar_resultado(nombre)
    
    print("\n" + "="*80)
    print("  ✅ PROCESO COMPLETADO")
    print("="*80)
    print("\n  Gracias por usar el Solucionador de Programación Lineal")
    print("  Desarrollado con Python, NumPy y Matplotlib\n")


# ==================================================================================
# PUNTO DE ENTRADA
# ==================================================================================

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
        print("👋 ¡Hasta pronto!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
