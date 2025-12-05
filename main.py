"""
==================================================================================
SOLUCIONADOR DE PROGRAMACIÓN LINEAL - MÉTODO SIMPLEX REVISADO
==================================================================================
Aplicación completa para resolver problemas de PL paso a paso.
Autores: Wilmar Osorio y Santiago Alexander Losada
Fecha: Noviembre 2025
==================================================================================
"""

import numpy as np
from manejo_consola import (
    mostrar_menu_principal,
    mostrar_menu_problemas_definidos,
    ingresar_problema_completo,
    generar_problema_ejemplo_2d,
    generar_problema_complejo,
    confirmar_accion
)
from resolucion_simplex import (
    resolver_problema_general,
    encontrar_siguiente_vertice_optimo
)
from visualizacion_grafica import graficar_solucion_2d
from exportacion_resultados import (
    guardar_resultado_txt,
    obtener_nombre_archivo_valido
)
from problema_definido import (
    obtener_problema_dos_fases,
    obtener_problema_grafico_grande,
    obtener_problema_multiples_variables,
    obtener_problema_personalizado,
    obtener_problema_infactible,
    obtener_problema_no_acotado,
    obtener_problema_multiples_optimos
)
from utilidades import mostrar_titulo, mostrar_caja, formatear_numero, Colores

# ==================================================================================
# CLASE PRINCIPAL: PROBLEMA DE PROGRAMACIÓN LINEAL
# ==================================================================================

class ProgramacionLineal:
    """
    Clase que representa y resuelve un problema de programación lineal
    usando el Método Simplex Revisado con la técnica de la Gran M.
    """
    
    def __init__(self):
        self.problema_datos = {}
        self.resultado_completo = {}
        self.soluciones_optimas = []  # Almacena todos los vértices óptimos encontrados
        self.pivotes_optimos_usados = [] # Variables no básicas ya usadas para pivotar
        self.estado = None

    @property
    def solucion_optima(self):
        return self.soluciones_optimas[0] if self.soluciones_optimas else None

    @property
    def valor_optimo(self):
        return self.resultado_completo.get('valor')

    def cargar_datos(self, datos):
        """Carga los datos del problema y resetea el estado."""
        self.problema_datos = datos
        self.resultado_completo = {}
        self.soluciones_optimas = []
        self.pivotes_optimos_usados = []
        self.estado = None
    
    def resolver(self):
        """Resuelve el problema de programación lineal."""
        if not self.problema_datos:
            print("\n❌ No hay datos de problema para resolver.")
            return

        input("\n⏸️  Presione ENTER para iniciar la resolución por Método Simplex...")
        
        self.resultado_completo = resolver_problema_general(self.problema_datos)
        self.estado = self.resultado_completo.get('estado')
        
        if self.estado == 'optimo':
            # Guardar la primera solución encontrada
            self.soluciones_optimas.append(self.resultado_completo['solucion'])
            
            # Realizar análisis de sensibilidad para la primera solución
            self.analisis_sensibilidad()

    def buscar_siguiente_optimo(self):
        """Busca y almacena un vértice óptimo adyacente."""
        nuevo_resultado, pivotes_usados = encontrar_siguiente_vertice_optimo(
            self.resultado_completo, 
            self.pivotes_optimos_usados
        )

        if nuevo_resultado:
            self.resultado_completo = nuevo_resultado
            self.pivotes_optimos_usados = pivotes_usados
            nueva_solucion = nuevo_resultado['solucion']
            self.soluciones_optimas.append(nueva_solucion)

            # Mostrar la nueva solución encontrada
            mostrar_caja("NUEVA SOLUCIÓN ÓPTIMA ENCONTRADA")
            print("  Variables de decisión:")
            for i, nombre in enumerate(self.problema_datos['nombres_vars']):
                print(f"    {nombre} = {formatear_numero(nueva_solucion[i])}")
            print(f"\n  Mismo valor {self.problema_datos['tipo']} de Z = {formatear_numero(self.valor_optimo)}")
            return True
        return False

    def analisis_sensibilidad(self):
        """
        Realiza el análisis de sensibilidad post-óptimo.
        Calcula precios sombra y rangos de variación para coeficientes.
        """
        print("\n" + "="*80)
        if not confirmar_accion("¿Desea realizar el análisis de sensibilidad?"):
            return
        
        mostrar_caja("ANÁLISIS DE SENSIBILIDAD POST-ÓPTIMO")
        
        # Extraer datos necesarios del resultado
        base_optima = self.resultado_completo['base']
        B_inv = self.resultado_completo['B_inv_optima']
        A_ext = self.resultado_completo['A_ext']
        c_ext = self.resultado_completo['c_ext']
        b_preparado = self.resultado_completo['b_preparado']
        nombres_ext = self.resultado_completo['nombres_ext']
        
        tipo = self.problema_datos['tipo']
        num_restricciones = self.problema_datos['num_restricciones']
        
        # 1. PRECIOS SOMBRA (Variables Duales)
        print("┌" + "─"*78 + "┐")
        print("│" + " "*20 + "1. PRECIOS SOMBRA (π)" + " "*36 + "│")
        print("└" + "─"*78 + "┘\n")
        
        c_B = c_ext[base_optima]
        precios_sombra = c_B @ B_inv
        
        if tipo == 'min':
            precios_sombra = -precios_sombra
        
        print("  Los precios sombra indican cuánto cambiaría Z por cada unidad adicional")
        print("  del lado derecho de cada restricción (manteniendo la base actual):\n")
        
        for i in range(num_restricciones):
            valor = precios_sombra[i]
            interpretacion = ""
            
            if abs(valor) < 1e-6:
                interpretacion = "→ Restricción " + Colores.azul("NO activa") + "."
            elif valor > 1e-6:
                interpretacion = f"→ Aumentar b{i+1} en 1 unidad " + Colores.verde("AUMENTA") + f" Z en {formatear_numero(abs(valor))}"
            else:
                interpretacion = f"→ Aumentar b{i+1} en 1 unidad " + Colores.rojo("DISMINUYE") + f" Z en {formatear_numero(abs(valor))}"
            
            print(f"    π{i+1} (Restricción {i+1}): {formatear_numero(valor)}")
            print(f"       {interpretacion}\n")
            
        # 2. RANGOS DE VARIACIÓN DEL LADO DERECHO (b)
        print("┌" + "─"*78 + "┐")
        print("│" + " "*15 + "2. RANGOS DE VARIACIÓN DEL LADO DERECHO (b)" + " "*14 + "│")
        print("└" + "─"*78 + "┘\n")
        print("  Indica cuánto puede variar cada b_i sin cambiar la base óptima:\n")

        solucion_basica = self.resultado_completo['solucion_completa'][base_optima]

        for i in range(num_restricciones):
            columna_b_inv = B_inv[:, i]
            aumentos = []
            disminuciones = []

            for k in range(len(solucion_basica)):
                if columna_b_inv[k] > 1e-9:
                    disminuciones.append(solucion_basica[k] / columna_b_inv[k])
                elif columna_b_inv[k] < -1e-9:
                    aumentos.append(-solucion_basica[k] / columna_b_inv[k])

            aumento_max = min(aumentos) if aumentos else float('inf')
            disminucion_max = min(disminuciones) if disminuciones else float('inf')

            b_actual = self.problema_datos['b'][i]
            lim_inf = b_actual - disminucion_max
            lim_sup = b_actual + aumento_max
            
            print(f"    b{i+1} (actualmente {formatear_numero(b_actual)}):")
            print(f"       Mínimo: {formatear_numero(lim_inf) if lim_inf > -float('inf') else '-∞'}")
            print(f"       Máximo: {formatear_numero(lim_sup) if lim_sup < float('inf') else '∞'}")
            print(f"       Rango: [{formatear_numero(lim_inf) if lim_inf > -float('inf') else '-∞'}, {formatear_numero(lim_sup) if lim_sup < float('inf') else '∞'}]\n")


        # 3. RANGOS DE VARIACIÓN DE COEFICIENTES OBJETIVO (c)
        print("┌" + "─"*78 + "┐")
        print("│" + " "*12 + "3. RANGOS DE VARIACIÓN DE COEFICIENTES OBJETIVO (c)" + " "*9 + "│")
        print("└" + "─"*78 + "┘\n")
        print("  Indica cuánto puede variar cada c_j sin cambiar la base óptima:\n")

        num_vars_decision = self.problema_datos['num_vars']
        vars_no_basicas = [i for i in range(A_ext.shape[1]) if i not in base_optima]
        
        # Fila Z del tablero final (costos reducidos * -1)
        c_B = c_ext[base_optima]
        fila_z_final = c_B @ B_inv @ A_ext - c_ext

        # Variables de decisión
        for j in range(num_vars_decision):
            c_actual = self.problema_datos['c'][j]
            nombre_var = self.problema_datos['nombres_vars'][j]
            
            if j in base_optima: # Variable básica
                idx_en_base = list(base_optima).index(j)
                # La fila 'j' del tablero final es la fila de B_inv donde está la var 'j' por A_ext
                fila_tablero_final = B_inv[idx_en_base, :] @ A_ext
                
                aumentos = []
                disminuciones = []
                
                for k in vars_no_basicas:
                    # El costo reducido en el tablero de maximización es Z_k - C_k
                    costo_reducido_k = fila_z_final[k]
                    
                    # El valor en el tablero es la entrada correspondiente en la fila de la variable basica
                    valor_tablero = fila_tablero_final[k]

                    if abs(valor_tablero) > 1e-9:
                        ratio = -costo_reducido_k / valor_tablero
                        if valor_tablero > 0: # Para maximización es al revés que la fórmula teórica de minimización
                            disminuciones.append(ratio)
                        else:
                            aumentos.append(ratio)
                
                # Para maximización, un aumento en Cj disminuye los costos reducidos de las no básicas
                # delta <= ratio
                aumento_max = min(aumentos) if aumentos else float('inf')
                # delta >= ratio
                disminucion_max = max(disminuciones) if disminuciones else -float('inf')
                
                lim_inf = c_actual + disminucion_max
                lim_sup = c_actual + aumento_max

            else: # Variable no básica
                costo_reducido = fila_z_final[j]
                
                # Para que la variable no básica siga siendo no óptima para entrar,
                # el nuevo costo reducido c_j_nuevo - z_j debe ser <= 0
                # c_j + delta - z_j <= 0  => delta <= z_j - c_j = -costo_reducido
                aumento_max = -costo_reducido
                
                lim_inf = -float('inf')
                lim_sup = c_actual + aumento_max

            print(f"    {nombre_var} (actualmente c = {formatear_numero(c_actual)}):")
            print(f"       Mínimo: {formatear_numero(lim_inf) if lim_inf > -float('inf') else '-∞'}")
            print(f"       Máximo: {formatear_numero(lim_sup) if lim_sup < float('inf') else '∞'}")
            # Corrección para rangos invertidos
            if lim_inf > lim_sup:
                print(f"       Rango: [{formatear_numero(lim_sup)}, {formatear_numero(lim_inf)}]\n")
            else:
                print(f"       Rango: [{formatear_numero(lim_inf) if lim_inf > -float('inf') else '-∞'}, {formatear_numero(lim_sup) if lim_sup < float('inf') else '∞'}]\n")

        # 4. ESTADO DE LAS RESTRICCIONES
        print("┌" + "─"*78 + "┐")
        print("│" + " "*20 + "4. ESTADO DE LAS RESTRICCIONES" + " "*27 + "│")
        print("└" + "─"*78 + "┘\n")

        solucion_completa = self.resultado_completo['solucion_completa']
        
        for i in range(len(nombres_ext)):
            nombre_var = nombres_ext[i]
            if nombre_var.startswith('s') or nombre_var.startswith('e'):
                valor_var = solucion_completa[i]
                if abs(valor_var) > 1e-6:
                    print(f"    - Restricción asociada a {nombre_var}: " + Colores.azul("NO ACTIVA") + f", Holgura/Exceso = {formatear_numero(valor_var)}")
                else:
                    print(f"    - Restricción asociada a {nombre_var}: " + Colores.rojo("ACTIVA") + " (Saturada)")

        print("\n" + "="*80)
        print("  ℹ️  INTERPRETACIÓN:")
        print("  • Restricciones ACTIVAS están completamente utilizadas.")
        print("  • Restricciones NO ACTIVAS tienen capacidad disponible (holgura).")
        print("  • Precios sombra positivos indican que aumentar el recurso de una restricción activa mejora Z.")
        print("  • Precios sombra cero se asocian a restricciones no activas (recurso no es limitante).")
        print("="*80)

    def mostrar_grafica(self):
        """Muestra la gráfica de la solución (solo 2D)."""
        if self.estado != 'optimo':
            print("\n⚠️  No hay solución óptima para graficar")
            return
        
        if self.problema_datos.get('num_vars') == 2:
            if confirmar_accion("¿Desea ver la solución gráfica?"):
                graficar_solucion_2d(
                    self.problema_datos['A'], self.problema_datos['b'], self.problema_datos['c'],
                    self.soluciones_optimas,  # Pasamos la lista de soluciones
                    self.valor_optimo,
                    self.problema_datos['tipo'],
                    self.problema_datos['num_vars'],
                    self.problema_datos['num_restricciones']
                )

    def guardar_resultado(self):
        """Guarda el resultado en un archivo."""
        if self.estado != 'optimo':
            print("\n⚠️  No hay solución que guardar.")
            return
            
        if confirmar_accion("¿Desea guardar el resultado en un archivo?"):
            nombre_archivo = obtener_nombre_archivo_valido()
            # Guardamos solo la primera solución encontrada en el txt por simplicidad
            guardar_resultado_txt(
                nombre_archivo,
                self.problema_datos['c'], self.problema_datos['A'], self.problema_datos['b'],
                self.problema_datos['tipo'],
                self.problema_datos['num_vars'],
                self.problema_datos['num_restricciones'],
                self.problema_datos['nombres_vars'],
                self.solucion_optima,
                self.valor_optimo,
                self.estado
            )


# ==================================================================================
# FUNCIÓN PRINCIPAL
# ==================================================================================

def main():
    """Función principal de la aplicación."""
    while True:
        opcion = mostrar_menu_principal()
        
        if opcion == '5':
            print("\n👋 ¡Hasta pronto!")
            break
        
        pl = ProgramacionLineal()
        datos = None
        continuar_al_menu = False

        if opcion == '1':
            datos = ingresar_problema_completo()
        
        elif opcion == '2':
            mostrar_titulo("GENERANDO PROBLEMA DE EJEMPLO")
            datos = generar_problema_ejemplo_2d()
            
        elif opcion == '3':
            mostrar_titulo("CARGANDO PROBLEMA COMPLEJO")
            datos = generar_problema_complejo()

        elif opcion == '4':
            opcion_submenu = mostrar_menu_problemas_definidos()
            if opcion_submenu == '1':
                datos = obtener_problema_personalizado()
            elif opcion_submenu == '2':
                datos = obtener_problema_dos_fases()
            elif opcion_submenu == '3':
                datos = obtener_problema_grafico_grande()
            elif opcion_submenu == '4':
                datos = obtener_problema_multiples_variables()
            elif opcion_submenu == '5':
                datos = obtener_problema_infactible()
            elif opcion_submenu == '6':
                datos = obtener_problema_no_acotado()
            elif opcion_submenu == '7':
                datos = obtener_problema_multiples_optimos()
            elif opcion_submenu == '8':
                continuar_al_menu = True
        
        if continuar_al_menu or datos is None:
            continue
        
        pl.cargar_datos(datos)
        pl.resolver()
        
        # Si se encontraron múltiples soluciones, preguntar al usuario si desea buscar más
        if pl.estado == 'optimo' and pl.resultado_completo.get('multiples_optimos'):
            while True:
                if not confirmar_accion("\n❓ Existen múltiples soluciones óptimas. ¿Desea buscar otro vértice óptimo?"):
                    break
                
                encontrado = pl.buscar_siguiente_optimo()
                if not encontrado:
                    break
        
        if pl.problema_datos and pl.problema_datos.get('num_vars') == 2 and pl.estado == 'optimo':
            print("\n" + "="*80)
            pl.mostrar_grafica()
        
        if pl.estado:
            print("\n" + "="*80)
            pl.guardar_resultado()
        
        print("\n\n" + "="*80)
        print("  ✅ PROCESO COMPLETADO. Presione ENTER para volver al menú principal...")
        print("="*80)
        input()


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
