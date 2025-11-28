"""
==================================================================================
SOLUCIONADOR DE PROGRAMACIÓN LINEAL - MÉTODO SIMPLEX REVISADO
==================================================================================
Aplicación completa para resolver problemas de PL paso a paso.
Autores: Wilmar Osorio y Santiago Alexander Losada
Fecha: Noviembre 2025
==================================================================================
"""

import random
import numpy as np
from manejo_consola import (
    mostrar_menu_principal,
    ingresar_problema_completo,
    generar_problema_ejemplo_2d,
    generar_problema_ejemplo_3d,
    confirmar_accion
)
from resolucion_simplex import (
    validar_factibilidad,
    resolver_simplex_revisado,
    mostrar_solucion_final
)
from visualizacion_grafica import graficar_solucion_2d
from exportacion_resultados import (
    guardar_resultado_txt,
    obtener_nombre_archivo_valido
)
from utilidades import mostrar_titulo, mostrar_caja, formatear_numero, obtener_nombre_variable, Colores


# ==================================================================================
# CLASE PRINCIPAL: PROBLEMA DE PROGRAMACIÓN LINEAL
# ==================================================================================

class ProgramacionLineal:
    """
    Clase que representa y resuelve un problema de programación lineal
    usando el Método Simplex Revisado.
    """
    
    def __init__(self):
        self.c = None
        self.A = None
        self.b = None
        self.tipo = 'max'
        self.num_vars = 0
        self.num_restricciones = 0
        self.nombres_vars = []
        self.solucion_optima = None
        self.valor_optimo = None
        self.estado = None
        self.base_optima = None  # Para análisis de sensibilidad
        self.B_inv_optima = None  # Inversa de la base óptima
    
    def cargar_datos(self, datos):
        """
        Carga los datos del problema desde un diccionario.
        
        Args:
            datos: Diccionario con los datos del problema
        """
        self.tipo = datos['tipo']
        self.c = datos['c']
        self.A = datos['A']
        self.b = datos['b']
        self.num_vars = datos['num_vars']
        self.num_restricciones = datos['num_restricciones']
        self.nombres_vars = datos['nombres_vars']
    
    def resolver(self):
        """Resuelve el problema de programación lineal."""
        # Validar factibilidad
        estado_validacion = validar_factibilidad(self.A, self.b)
        
        if estado_validacion == 'infactible':
            self.estado = 'infactible'
            print("\n❌ No se puede resolver un problema infactible")
            return
        
        # Resolver
        input("\n⏸️  Presione ENTER para iniciar la resolución por Método Simplex...")
        resultado = resolver_simplex_revisado(
            self.c, self.A, self.b, self.tipo, self.num_vars
        )
        
        self.estado = resultado.get('estado')
        
        if self.estado == 'optimo':
            self.solucion_optima = resultado['solucion']
            self.valor_optimo = resultado['valor']
            self.base_optima = resultado.get('base')
            mostrar_solucion_final(
                self.solucion_optima,
                self.valor_optimo,
                self.tipo,
                self.nombres_vars
            )
            
            # Realizar análisis de sensibilidad
            if self.base_optima is not None:
                self.analisis_sensibilidad()
    
    def mostrar_grafica(self):
        """Muestra la gráfica de la solución (solo 2D)."""
        if self.estado != 'optimo':
            print("\n⚠️  No hay solución óptima para graficar")
            return
        
        if self.num_vars == 2:
            if confirmar_accion("¿Desea ver la solución gráfica?"):
                graficar_solucion_2d(
                    self.A, self.b, self.c,
                    self.solucion_optima,
                    self.valor_optimo,
                    self.tipo,
                    self.num_vars,
                    self.num_restricciones
                )
    
    def analisis_sensibilidad(self):
        """
        Realiza el análisis de sensibilidad post-óptimo.
        Calcula precios sombra y rangos de variación para coeficientes.
        """
        print("\n" + "="*80)
        if not confirmar_accion("¿Desea realizar el análisis de sensibilidad?"):
            return
        
        mostrar_caja("ANÁLISIS DE SENSIBILIDAD POST-ÓPTIMO")
        
        # Preparar datos extendidos
        m = self.num_restricciones
        n = self.num_vars
        A_extended = np.hstack([self.A, np.eye(m)])
        
        # Ajustar c según tipo de optimización
        c = self.c.copy()
        if self.tipo == 'min':
            c = -c
        c_extended = np.hstack([c, np.zeros(m)])
        
        # Calcular B y B_inv
        B = A_extended[:, self.base_optima]
        try:
            B_inv = np.linalg.inv(B)
        except:
            print("⚠️  No se puede calcular la inversa de la base óptima")
            return
        
        # 1. PRECIOS SOMBRA (Variables Duales)
        print("\n┌" + "─"*78 + "┐")
        print("│" + " "*20 + "1. PRECIOS SOMBRA (π)" + " "*36 + "│")
        print("└" + "─"*78 + "┘\n")
        
        c_B = c_extended[self.base_optima]
        precios_sombra = c_B @ B_inv
        
        if self.tipo == 'min':
            precios_sombra = -precios_sombra
        
        print("  Los precios sombra indican cuánto cambiaría Z por cada unidad adicional")
        print("  del lado derecho de cada restricción:\n")
        
        for i in range(m):
            valor = precios_sombra[i]
            interpretacion = ""
            
            if abs(valor) < 1e-6:
                color_valor = formatear_numero(valor)
                interpretacion = "→ Restricción " + Colores.azul("NO activa") + " (holgura disponible)"
            elif valor > 1e-6:
                color_valor = Colores.verde(f"+{formatear_numero(valor)}")
                interpretacion = f"→ Aumentar b{i+1} en 1 unidad " + Colores.verde("AUMENTA") + f" Z en {formatear_numero(abs(valor))}"
            else:
                color_valor = Colores.rojo(formatear_numero(valor))
                interpretacion = f"→ Aumentar b{i+1} en 1 unidad " + Colores.rojo("DISMINUYE") + f" Z en {formatear_numero(abs(valor))}"
            
            print(f"    π{i+1} (Restricción {i+1}): {color_valor}")
            print(f"       {interpretacion}\n")
        
        # 2. RANGOS DE VARIACIÓN DEL LADO DERECHO (b)
        print("┌" + "─"*78 + "┐")
        print("│" + " "*15 + "2. RANGOS DE VARIACIÓN DEL LADO DERECHO (b)" + " "*19 + "│")
        print("└" + "─"*78 + "┘\n")
        
        print("  Indica cuánto puede variar cada b_i sin cambiar la base óptima:\n")
        
        x_B = B_inv @ self.b
        
        for i in range(m):
            # Calcular límites
            delta_min = float('-inf')
            delta_max = float('inf')
            
            for k in range(m):
                if abs(B_inv[k, i]) > 1e-9:
                    if B_inv[k, i] > 0:
                        delta_max = min(delta_max, x_B[k] / B_inv[k, i])
                    else:
                        delta_min = max(delta_min, x_B[k] / B_inv[k, i])
            
            b_actual = self.b[i]
            b_min = b_actual + delta_min if delta_min > float('-inf') else float('-inf')
            b_max = b_actual + delta_max if delta_max < float('inf') else float('inf')
            
            print(f"    b{i+1} (actualmente {Colores.azul(formatear_numero(b_actual))}):")
            
            if b_min > float('-inf'):
                print(f"       Mínimo: {formatear_numero(b_min)} " + 
                      f"(puede " + Colores.rojo("disminuir") + f" hasta {formatear_numero(b_actual - b_min)})")
            else:
                print(f"       Mínimo: -∞ (sin límite inferior)")
            
            if b_max < float('inf'):
                print(f"       Máximo: {formatear_numero(b_max)} " +
                      f"(puede " + Colores.verde("aumentar") + f" hasta {formatear_numero(b_max - b_actual)})")
            else:
                print(f"       Máximo: +∞ (sin límite superior)")
            
            print(f"       Rango: [{formatear_numero(b_min) if b_min > float('-inf') else '-∞'}, " +
                  f"{formatear_numero(b_max) if b_max < float('inf') else '+∞'}]\n")
        
        # 3. RANGOS DE VARIACIÓN DE COEFICIENTES DE LA FUNCIÓN OBJETIVO (c)
        print("┌" + "─"*78 + "┐")
        print("│" + " "*10 + "3. RANGOS DE VARIACIÓN DE COEFICIENTES OBJETIVO (c)" + " "*15 + "│")
        print("└" + "─"*78 + "┘\n")
        
        print("  Indica cuánto puede variar cada c_j sin cambiar la base óptima:\n")
        
        # Solo para variables básicas
        for idx, var_idx in enumerate(self.base_optima):
            if var_idx < n:  # Solo variables de decisión
                nombre_var = obtener_nombre_variable(var_idx, n)
                c_actual = self.c[var_idx]
                
                # Calcular rangos (simplificado)
                # Para una variable básica: analizar costos reducidos
                
                c_min = float('-inf')
                c_max = float('inf')
                
                # Calcular límites basados en costos reducidos de variables no básicas
                for j in range(n + m):
                    if j not in self.base_optima:
                        col_j = A_extended[:, j]
                        y_j = B_inv @ col_j
                        
                        # Contribución de esta variable básica
                        if abs(y_j[idx]) > 1e-9:
                            # Costo reducido actual
                            costo_red = c_extended[j] - c_B @ y_j
                            
                            # Límite para mantener costo_red <= 0
                            if y_j[idx] > 1e-9:
                                limite = c_actual + costo_red / y_j[idx]
                                c_max = min(c_max, limite)
                            else:
                                limite = c_actual + costo_red / y_j[idx]
                                c_min = max(c_min, limite)
                
                print(f"    {Colores.azul(nombre_var)} (actualmente c = {formatear_numero(c_actual)}):")
                
                if c_min > float('-inf'):
                    print(f"       Mínimo: {formatear_numero(c_min)}")
                else:
                    print(f"       Mínimo: -∞")
                
                if c_max < float('inf'):
                    print(f"       Máximo: {formatear_numero(c_max)}")
                else:
                    print(f"       Máximo: +∞")
                
                print(f"       Rango: [{formatear_numero(c_min) if c_min > float('-inf') else '-∞'}, " +
                      f"{formatear_numero(c_max) if c_max < float('inf') else '+∞'}]\n")
        
        # 4. VARIABLES NO BÁSICAS (Holgura/Exceso)
        print("┌" + "─"*78 + "┐")
        print("│" + " "*20 + "4. ESTADO DE LAS RESTRICCIONES" + " "*27 + "│")
        print("└" + "─"*78 + "┘\n")
        
        for i in range(m):
            var_holgura = n + i
            nombre_holgura = obtener_nombre_variable(var_holgura, n)
            
            if var_holgura in self.base_optima:
                idx_en_base = self.base_optima.index(var_holgura)
                valor_holgura = x_B[idx_en_base]
                print(f"    Restricción {i+1} ({nombre_holgura}): " + 
                      Colores.azul("NO ACTIVA") + f" - Holgura = {formatear_numero(valor_holgura)}")
            else:
                print(f"    Restricción {i+1} ({nombre_holgura}): " + 
                      Colores.rojo("ACTIVA") + " - Holgura = 0.00 (saturada)")
        
        print("\n" + "="*80)
        print("  ℹ️  INTERPRETACIÓN:")
        print("  • Restricciones " + Colores.rojo("ACTIVAS") + " están completamente utilizadas")
        print("  • Restricciones " + Colores.azul("NO ACTIVAS") + " tienen capacidad disponible")
        print("  • Precios sombra positivos: aumentar recurso " + Colores.verde("mejora") + " Z")
        print("  • Precios sombra cero: recurso " + Colores.azul("sobra") + " (no es cuello de botella)")
        print("="*80)
    
    def guardar_resultado(self):
        """Guarda el resultado en un archivo."""
        if confirmar_accion("¿Desea guardar el resultado en un archivo?"):
            nombre_archivo = obtener_nombre_archivo_valido()
            guardar_resultado_txt(
                nombre_archivo,
                self.c, self.A, self.b,
                self.tipo,
                self.num_vars,
                self.num_restricciones,
                self.nombres_vars,
                self.solucion_optima,
                self.valor_optimo,
                self.estado
            )


# ==================================================================================
# FUNCIÓN PRINCIPAL
# ==================================================================================

def main():
    """Función principal de la aplicación."""
    # Mostrar menú y obtener opción
    opcion = mostrar_menu_principal()
    
    if opcion == '3':
        print("\n👋 ¡Hasta pronto!")
        return
    
    # Crear instancia del problema
    pl = ProgramacionLineal()
    
    # Cargar datos según opción
    if opcion == '1':
        datos = ingresar_problema_completo()
        if datos is None:
            return
        pl.cargar_datos(datos)
        
    elif opcion == '2':
        mostrar_titulo("GENERANDO PROBLEMA DE EJEMPLO")
        num_vars = random.choice([2, 3])
        
        if num_vars == 2:
            datos = generar_problema_ejemplo_2d()
        else:
            datos = generar_problema_ejemplo_3d()
        
        pl.cargar_datos(datos)
    
    # Resolver el problema
    pl.resolver()
    
    # Mostrar gráfica si aplica
    if pl.num_vars == 2 and pl.estado == 'optimo':
        print("\n" + "="*80)
        pl.mostrar_grafica()
    
    # Guardar resultado
    print("\n" + "="*80)
    pl.guardar_resultado()
    
    # Mensaje de finalización
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
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
        print("👋 ¡Hasta pronto!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
