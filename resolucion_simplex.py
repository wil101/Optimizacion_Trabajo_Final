"""
==================================================================================
MÓDULO DE RESOLUCIÓN SIMPLEX
==================================================================================
Implementación del Método Simplex Revisado con visualización mejorada.
==================================================================================
"""

import numpy as np
from utilidades import (
    Colores, 
    formatear_numero, 
    obtener_nombre_variable,
    mostrar_titulo,
    mostrar_caja
)


# ==================================================================================
# VALIDACIÓN DE FACTIBILIDAD
# ==================================================================================

def validar_factibilidad(A, b):
    """
    Valida si el problema es factible preliminarmente.
    
    Args:
        A: Matriz de restricciones
        b: Vector de lado derecho
    
    Returns:
        str: 'factible' o 'infactible'
    """
    mostrar_titulo("VALIDACIÓN DE FACTIBILIDAD")
    
    if np.any(b < 0):
        print("❌ PROBLEMA INFACTIBLE: Lado derecho con valores negativos")
        return 'infactible'
    
    if np.all(b >= 0):
        print("✅ El problema tiene al menos la solución trivial (todas las variables = 0)")
        print("✅ El problema es FACTIBLE")
        return 'factible'
    
    print("⚠️  Se requiere análisis adicional durante la ejecución del simplex")
    return 'factible'


# ==================================================================================
# TABLERO SIMPLEX REVISADO CON FORMATO MEJORADO
# ==================================================================================

def mostrar_tablero_revisado(iteracion, base, B_inv, A, c_B, c, x_B, Z, n, 
                            var_entrante=None, var_saliente=None):
    """
    Muestra el tablero simplex revisado con formato de 2 decimales y colores.
    
    Args:
        iteracion: Número de iteración
        base: Lista de índices de variables básicas
        B_inv: Matriz inversa de la base
        A: Matriz extendida de restricciones
        c_B: Vector de costos básicos
        c: Vector de costos extendido
        x_B: Solución básica actual
        Z: Valor de la función objetivo
        n: Número de variables de decisión
        var_entrante: Índice de variable entrante (opcional)
        var_saliente: Índice de variable saliente (opcional)
    """
    m = len(base)
    total_vars = len(c)
    
    mostrar_caja(f"TABLERO SIMPLEX REVISADO - ITERACIÓN {iteracion}")
    
    # Encabezados
    headers = ['Z'] + [obtener_nombre_variable(i, n) for i in range(total_vars)] + ['π'] + ['LD']
    
    # Calcular B_inv * A
    B_inv_A = B_inv @ A
    
    # Calcular variables duales π una sola vez
    pi = c_B @ B_inv
    
    # Primera fila: [ 1 | C_B * B⁻¹ * A - C | π | Z ]
    fila_Z = [1.0]
    
    # C_B * B⁻¹ * A - C para cada variable
    for j in range(total_vars):
        valor = c_B @ (B_inv @ A[:, j]) - c[j]
        fila_Z.append(-valor)
    
    # Agregar 0 para la columna π en la fila Z (no aplica para Z)
    fila_Z.append(0.0)
    
    # C_B * B⁻¹ * b (valor de Z)
    fila_Z.append(Z)
    
    # Filas de restricciones: [ 0 | B⁻¹ * A | valores de π para esta fila | valor de x_B ]
    filas_rest = []
    for i in range(m):
        fila = [0.0]
        fila.extend(B_inv_A[i, :])
        fila.append(pi[i])  # Solo el precio sombra para esta restricción
        fila.append(x_B[i])
        filas_rest.append(fila)
    
    # Construir tabla con formato y colores
    print("  Var. Base │ ", end="")
    for j, h in enumerate(headers):
        # Colorear encabezado de variable entrante en azul
        if var_entrante is not None and j > 0 and j-1 == var_entrante:
            h_coloreado = Colores.azul(h)
            espacios_extra = len(h_coloreado) - len(h)
            print(f"{h_coloreado:>{8+espacios_extra}}", end=" ")
        else:
            print(f"{h:>8}", end=" ")
    print()
    print("  " + "─"*10 + "┼" + "─"*(9 * len(headers)))
    
    # Fila Z
    print(f"  {'Z':^10}│ ", end="")
    for j, val in enumerate(fila_Z):
        val_formateado = formatear_numero(val)
        # Colorear columna de variable entrante en azul
        # var_entrante está en posición var_entrante+1 en fila_Z
        if var_entrante is not None and j == var_entrante + 1:
            val_coloreado = Colores.azul(val_formateado)
            espacios_extra = len(val_coloreado) - len(val_formateado)
            print(f"{val_coloreado:>{8+espacios_extra}}", end=" ")
        else:
            print(f"{val_formateado:>8}", end=" ")
    print()
    
    # Filas de restricciones con colores
    for i, fila in enumerate(filas_rest):
        var_base = obtener_nombre_variable(base[i], n)
        
        # Colorear variable saliente en rojo
        if var_saliente is not None and base[i] == var_saliente:
            var_base_mostrar = Colores.rojo(var_base)
        # Colorear variable entrante en azul (cuando ya está en la base)
        elif var_entrante is not None and base[i] == var_entrante:
            var_base_mostrar = Colores.azul(var_base)
        else:
            var_base_mostrar = var_base
        
        # Ajustar espaciado para códigos ANSI
        if var_base_mostrar != var_base:
            espacios_extra = len(var_base_mostrar) - len(var_base)
            print(f"  {var_base_mostrar:^{10+espacios_extra}}│ ", end="")
        else:
            print(f"  {var_base_mostrar:^10}│ ", end="")
        
        # Colorear toda la fila si es la variable saliente, o columna si es entrante
        if var_saliente is not None and base[i] == var_saliente:
            # Esta es la fila saliente - pintar en rojo, excepto intersección
            for j, val in enumerate(fila):
                val_formateado = formatear_numero(val)
                # Si también es la columna entrante, pintar en morado (intersección)
                if var_entrante is not None and j == var_entrante + 1:
                    val_coloreado = Colores.morado(val_formateado)
                    espacios_extra = len(val_coloreado) - len(val_formateado)
                    print(f"{val_coloreado:>{8+espacios_extra}}", end=" ")
                else:
                    # Resto de la fila en rojo
                    val_coloreado = Colores.rojo(val_formateado)
                    espacios_extra = len(val_coloreado) - len(val_formateado)
                    print(f"{val_coloreado:>{8+espacios_extra}}", end=" ")
        else:
            # No es fila saliente - revisar si hay columnas entrantes
            for j, val in enumerate(fila):
                val_formateado = formatear_numero(val)
                # Columna entrante: j-1 porque fila empieza con 0.0 en posición 0
                # La variable entrante está en posición var_entrante+1
                if var_entrante is not None and j == var_entrante + 1:
                    val_coloreado = Colores.azul(val_formateado)
                    espacios_extra = len(val_coloreado) - len(val_formateado)
                    print(f"{val_coloreado:>{8+espacios_extra}}", end=" ")
                else:
                    print(f"{val_formateado:>8}", end=" ")
        print()
    
    print("\n  Leyenda:")
    print(f"    Z: Función objetivo = {formatear_numero(Z)}")
    print(f"    π: Variables duales (precios sombra)")
    print(f"    LD: Lado derecho (valores de variables básicas)")
    
    # Mostrar base con colores
    base_nombres = []
    for v in base:
        nombre = obtener_nombre_variable(v, n)
        if var_entrante is not None and v == var_entrante:
            base_nombres.append(Colores.azul(nombre))
        elif var_saliente is not None and v == var_saliente:
            base_nombres.append(Colores.rojo(nombre))
        else:
            base_nombres.append(nombre)
    
    print(f"    Base actual: [" + ", ".join(base_nombres) + "]")


# ==================================================================================
# ALGORITMO SIMPLEX REVISADO
# ==================================================================================

def resolver_simplex_revisado(c_original, A, b, tipo, n):
    """
    Resuelve el problema usando el Método Simplex Revisado.
    
    Args:
        c_original: Vector de coeficientes de función objetivo original
        A: Matriz de restricciones
        b: Vector de lado derecho
        tipo: 'max' o 'min'
        n: Número de variables de decisión
    
    Returns:
        dict: Resultado con solución, estado, etc.
    """
    mostrar_titulo("RESOLUCIÓN POR MÉTODO SIMPLEX REVISADO")
    
    # Convertir minimización a maximización
    c = c_original.copy()
    if tipo == 'min':
        c = -c
        print("🔄 Convirtiendo minimización a maximización (c = -c)\n")
    
    # Configuración inicial
    m = len(b)
    
    # Agregar variables de holgura
    A_extended = np.hstack([A, np.eye(m)])
    c_extended = np.hstack([c, np.zeros(m)])
    
    # Base inicial: variables de holgura
    base = list(range(n, n + m))
    
    iteracion = 0
    
    print("📋 Configuración Inicial:")
    print(f"   Variables de decisión: {n}")
    print(f"   Restricciones: {m}")
    print(f"   Variables de holgura: {m}")
    print(f"   Total de variables: {n + m}")
    print(f"   Base inicial: s1 a s{m} (variables de holgura)\n")
    
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
            return {'estado': 'infactible'}
        
        # Vector de costos básicos
        c_B = c_extended[base]
        
        # Solución básica actual
        x_B = B_inv @ b
        
        # Verificar factibilidad
        if np.any(x_B < -1e-9):
            print("❌ PROBLEMA INFACTIBLE: Solución básica con valores negativos")
            return {'estado': 'infactible'}
        
        # Valor de Z
        Z = c_B @ x_B
        
        # Calcular costos reducidos
        costos_reducidos = np.zeros(n + m)
        for j in range(n + m):
            if j not in base:
                costos_reducidos[j] = c_extended[j] - c_B @ (B_inv @ A_extended[:, j])
        
        # Test de optimalidad
        if np.all(costos_reducidos <= 1e-9):
            print("\n" + "="*80)
            print("  ✅ \033[1;30;42m ¡SOLUCIÓN ÓPTIMA ENCONTRADA!\033[0m")
            print("="*80)
            
            # Mostrar tablero final (sin variable entrante/saliente)
            mostrar_tablero_revisado(iteracion, base, B_inv, A_extended, 
                                    c_B, c_extended, x_B, Z, n)
            
            # Guardar solución
            solucion = np.zeros(n + m)
            solucion[base] = x_B
            solucion_optima = solucion[:n]
            valor_optimo = Z if tipo == 'max' else -Z
            
            return {
                'estado': 'optimo',
                'solucion': solucion_optima,
                'valor': valor_optimo,
                'base': base
            }
        
        # Seleccionar variable entrante
        idx_entrante = np.argmax(costos_reducidos)
        if costos_reducidos[idx_entrante] <= 1e-9:
            solucion = np.zeros(n + m)
            solucion[base] = x_B
            valor_optimo = Z if tipo == 'max' else -Z
            return {
                'estado': 'optimo',
                'solucion': solucion[:n],
                'valor': valor_optimo,
                'base': base
            }
        
        var_entrante = idx_entrante
        
        # Calcular dirección
        y = B_inv @ A_extended[:, var_entrante]
        
        # Test de acotamiento
        if np.all(y <= 1e-9):
            print("\n" + "="*80)
            print("  ⚠️  PROBLEMA NO ACOTADO")
            print("="*80)
            print("\nTodas las componentes de la dirección son ≤ 0")
            print("La función objetivo puede crecer indefinidamente")
            return {'estado': 'no_acotado'}
        
        # Calcular ratios
        ratios = []
        for i in range(m):
            if y[i] > 1e-9:
                ratios.append((x_B[i] / y[i], i))
            else:
                ratios.append((float('inf'), i))
        
        # Seleccionar variable saliente
        ratio_min, idx_saliente = min(ratios)
        
        if ratio_min == float('inf'):
            print("\n⚠️  PROBLEMA NO ACOTADO")
            return {'estado': 'no_acotado'}
        
        var_saliente = base[idx_saliente]
        
        # Mostrar tablero CON variables entrante y saliente coloreadas
        mostrar_tablero_revisado(iteracion, base, B_inv, A_extended, 
                                c_B, c_extended, x_B, Z, n, var_entrante, var_saliente)
        
        nombre_entrante = obtener_nombre_variable(var_entrante, n)
        nombre_saliente = obtener_nombre_variable(var_saliente, n)
        
        print(f"\n🔵 Variable entrante: " + Colores.azul(nombre_entrante) + 
              f" (columna {var_entrante})")
        print(f"   Costo reducido: {formatear_numero(costos_reducidos[var_entrante])}")
        
        print(f"🔴 Variable saliente: " + Colores.rojo(nombre_saliente) + 
              f" (posición {idx_saliente} en base)")
        print(f"   Ratio mínimo: {formatear_numero(ratio_min)}")
        
        # Actualizar base
        base[idx_saliente] = var_entrante
        
        print(f"\n📊 Nueva base: [" + ", ".join([
            Colores.azul(obtener_nombre_variable(v, n)) if v == var_entrante 
            else obtener_nombre_variable(v, n) 
            for v in base
        ]) + "]")
        
        # Pausa para visualización
        input("\n⏸️  Presione ENTER para continuar a la siguiente iteración...")
        
        # Límite de iteraciones
        if iteracion > 50:
            print("\n⚠️  Límite de iteraciones alcanzado")
            break
    
    return {'estado': 'error'}


# ==================================================================================
# PRESENTACIÓN DE RESULTADOS
# ==================================================================================

def mostrar_solucion_final(solucion, valor, tipo, nombres_vars):
    """
    Muestra la solución óptima encontrada.
    
    Args:
        solucion: Vector solución
        valor: Valor óptimo de Z
        tipo: 'max' o 'min'
        nombres_vars: Lista de nombres de variables
    """
    mostrar_caja("\033[1;30;42mSOLUCIÓN ÓPTIMA\033[0m")
    
    print("  Variables de decisión:")
    for i, nombre in enumerate(nombres_vars):
        print(f"    {nombre} = {formatear_numero(solucion[i])}")
    
    objetivo = "Máximo" if tipo == 'max' else "Mínimo"
    print(f"\n  {objetivo} valor de Z = {formatear_numero(valor)}")
    
    print("\n  Interpretación:")
    print(f"    El valor {'máximo' if tipo == 'max' else 'mínimo'} de la función")
    print(f"    objetivo es {formatear_numero(valor)}, alcanzado en el punto:")
    punto = ', '.join([f"{nombres_vars[i]}={formatear_numero(solucion[i])}" 
                      for i in range(len(nombres_vars))])
    print(f"    ({punto})")
