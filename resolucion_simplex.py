"""
==================================================================================
MÓDULO DE RESOLUCIÓN SIMPLEX
==================================================================================
Implementación del Método Simplex Revisado con el Método de Dos Fases para
resolver problemas de programación lineal con cualquier tipo de restricción.
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


def preparar_problema_estandar(c, A, b, tipos_restricciones, tipo_optimizacion, n_vars):
    """
    Convierte un problema de PL a la forma estándar, agregando variables de
    holgura, exceso y artificiales según sea necesario.
    """
    num_restricciones = len(b)
    
    # Asegurar que todos los b son positivos
    for i in range(num_restricciones):
        if b[i] < 0:
            b[i] *= -1
            A[i, :] *= -1
            tipos_restricciones[i] = '>=' if tipos_restricciones[i] == '<=' else '<='

    holgura_idx, exceso_idx, artificial_idx = [], [], []
    A_list = [A[:, i] for i in range(A.shape[1])]
    base_inicial = [-1] * num_restricciones
    var_idx = n_vars

    for i, tipo in enumerate(tipos_restricciones):
        if tipo == '<=':
            col = np.zeros(num_restricciones); col[i] = 1
            A_list.append(col); holgura_idx.append(var_idx)
            base_inicial[i] = var_idx; var_idx += 1
        elif tipo == '>=':
            col_ex = np.zeros(num_restricciones); col_ex[i] = -1
            A_list.append(col_ex); exceso_idx.append(var_idx); var_idx += 1
            
            col_art = np.zeros(num_restricciones); col_art[i] = 1
            A_list.append(col_art); artificial_idx.append(var_idx)
            base_inicial[i] = var_idx; var_idx += 1
        elif tipo == '=':
            col_art = np.zeros(num_restricciones); col_art[i] = 1
            A_list.append(col_art); artificial_idx.append(var_idx)
            base_inicial[i] = var_idx; var_idx += 1

    A_ext = np.array(A_list).T
    nombres_ext = [obtener_nombre_variable(i, n_vars, holgura_idx, exceso_idx, artificial_idx) for i in range(A_ext.shape[1])]
    
    return A_ext, b, base_inicial, holgura_idx, exceso_idx, artificial_idx, nombres_ext


def resolver_problema_general(problema):
    """
    Punto de entrada que orquesta la resolución del problema de PL
    utilizando el método de dos fases si es necesario.
    """
    c_np = np.array(problema['c'], dtype=float)
    A_np = np.array(problema['A'], dtype=float)
    b_np = np.array(problema['b'], dtype=float)
    tipo, n = problema['tipo'], problema['num_vars']
    tipos_rest = problema.get('tipos_restricciones', ['<='] * len(b_np))
    
    A_ext, b_prep, base, holgura, exceso, artificiales, nombres_ext = preparar_problema_estandar(
        c_np, A_np, b_np, tipos_rest, tipo, n)

    if not artificiales:
        mostrar_titulo("FASE ÚNICA (PROBLEMA ESTÁNDAR)")
        c_fase2 = np.hstack([c_np if tipo == 'max' else -c_np, np.zeros(A_ext.shape[1] - n)])
        resultado = resolver_simplex_revisado("FASE ÚNICA", c_np, A_ext, b_prep, tipo, n, c_fase2, base, artificiales, nombres_ext)
    else:
        # --- FASE 1 ---
        mostrar_titulo("INICIO DE LA FASE 1")
        print("Objetivo: Minimizar la suma de variables artificiales.\n")
        c_fase1 = np.array([-1.0 if i in artificiales else 0.0 for i in range(A_ext.shape[1])])
        
        fase1_resultado = resolver_simplex_revisado("FASE 1", np.zeros(n), A_ext, b_prep, 'max', n, c_fase1, base, artificiales, nombres_ext, es_fase_1=True)

        if fase1_resultado.get('estado') != 'optimo' or abs(fase1_resultado.get('valor', 0)) > 1e-6:
            print("\n❌ PROBLEMA INFACTIBLE: No se pudo eliminar las variables artificiales en la Fase 1.")
            return {'estado': 'infactible'}
        
        mostrar_titulo("FIN DE LA FASE 1: Solución Factible Encontrada")
        base = fase1_resultado['base']

        # --- FASE 2 ---
        mostrar_titulo("INICIO DE LA FASE 2")
        print("Objetivo: Optimizar la función objetivo original.\n")
        
        # Eliminar columnas de variables artificiales
        vars_no_artificiales = sorted(list(set(range(A_ext.shape[1])) - set(artificiales)))
        A_fase2 = A_ext[:, vars_no_artificiales]
        nombres_fase2 = [nombres_ext[i] for i in vars_no_artificiales]
        
        mapa_indices_f2 = {original: nuevo for nuevo, original in enumerate(vars_no_artificiales)}
        base_fase2 = [mapa_indices_f2[i] for i in base if i in mapa_indices_f2]

        c_orig_fase2 = np.hstack([c_np if tipo == 'max' else -c_np, np.zeros(len(holgura) + len(exceso))])
        
        resultado = resolver_simplex_revisado("FASE 2", c_np, A_fase2, b_prep, tipo, n, c_orig_fase2, base_fase2, [], nombres_fase2)

    # Finalización
    if resultado.get('estado') == 'optimo':
        mostrar_solucion_final(
            resultado['solucion'],
            resultado['valor'],
            tipo,
            problema['nombres_vars'],
            resultado.get('multiples_optimos', False)
        )
    elif resultado.get('estado') == 'no_acotado':
        mostrar_caja("\033[1;31mSOLUCIÓN NO ACOTADA\033[0m")
        print("El problema no tiene una solución finita porque el valor de la función objetivo puede aumentar (o disminuir) indefinidamente.")
    
    return resultado


def seleccionar_variable_entrante(costos_reducidos, base, nombres_vars):
    """Selecciona la variable entrante usando la regla de Bland para empates."""
    min_costo = np.min(costos_reducidos[costos_reducidos < -1e-9])
    candidatas = [i for i, costo in enumerate(costos_reducidos) if abs(costo - min_costo) < 1e-9 and i not in base]
    
    if len(candidatas) > 1:
        print(f"  {Colores.amarillo('CASO ESPECIAL:')} Empate para la variable entrante. Candidatas: {[nombres_vars[i] for i in candidatas]}.")
        print(f"  Usando la Regla de Bland, se elige la de menor índice: {nombres_vars[min(candidatas)]}")
    
    return min(candidatas)

def seleccionar_variable_saliente(x_B, y, base, nombres_vars):
    """
    Selecciona la variable saliente. Detecta casos de degeneración y solución no acotada.
    Retorna la variable saliente, su índice, el estado y el ratio mínimo.
    """
    if np.all(y <= 1e-9):
        print(f"  {Colores.rojo('CASO ESPECIAL:')} Solución no acotada. Todas las 'y' son <= 0.")
        return None, None, 'no_acotado', None

    ratios = [(x_B[i] / y[i]) if y[i] > 1e-9 else float('inf') for i in range(len(base))]
    min_ratio = min(ratios)

    if min_ratio == float('inf'):
        return None, None, 'no_acotado', None

    candidatas_idx = [i for i, ratio in enumerate(ratios) if abs(ratio - min_ratio) < 1e-9]

    if len(candidatas_idx) > 1:
        vars_candidatas = [nombres_vars[base[i]] for i in candidatas_idx]
        print(f"  {Colores.amarillo('CASO ESPECIAL:')} Empate para la variable saliente (Degeneración). Candidatas: {vars_candidatas}.")
        
        # Regla de Bland: Elegir la variable con el menor índice original.
        idx_elegido = min(candidatas_idx, key=lambda i: base[i])
        print(f"  Usando la Regla de Bland, se elige la de menor índice: {nombres_vars[base[idx_elegido]]}")
        
        return base[idx_elegido], idx_elegido, 'degenerado', min_ratio

    idx_saliente_en_base = ratios.index(min_ratio)
    var_saliente = base[idx_saliente_en_base]
    
    return var_saliente, idx_saliente_en_base, 'normal', min_ratio


def resolver_simplex_revisado(nombre_fase, c_original, A_extended, b, tipo, n, c_extended, base, 
                              vars_artificiales, nombres_vars_ext, es_fase_1=False):
    """Motor del algoritmo Simplex Revisado."""
    iteracion = 0
    while True:
        iteracion += 1
        print(f"\n{'─'*80}\n  {nombre_fase} - ITERACIÓN {iteracion}\n{'─'*80}\n")
        
        try:
            B_matrix = A_extended[:, base]
            B_inv = np.linalg.inv(B_matrix)
        except np.linalg.LinAlgError:
            return {'estado': 'error', 'mensaje': 'Matriz básica singular.'}
        
        c_B = c_extended[base]
        x_B = B_inv @ b
        Z = c_B @ x_B
        
        costos_reducidos = np.zeros(len(c_extended))
        for j in range(len(c_extended)):
            if j not in base:
                # Costo reducido z_j - c_j
                costos_reducidos[j] = c_B @ B_inv @ A_extended[:, j] - c_extended[j]
        
        if np.all(costos_reducidos >= -1e-9):
            print("✅ Condición de optimalidad alcanzada.")
            
            # Comprobar si hay múltiples soluciones óptimas
            multiples_optimos = False
            vars_no_basicas = [i for i in range(len(c_extended)) if i not in base]
            for j in vars_no_basicas:
                # Solo consideramos variables de decisión y de holgura/exceso, no artificiales
                if j not in vars_artificiales and abs(costos_reducidos[j]) < 1e-9:
                    multiples_optimos = True
                    break
            
            if multiples_optimos:
                print(f"  {Colores.verde('ℹ️  NOTA:')} Se ha encontrado una solución óptima, pero existen múltiples soluciones.")
                print(f"     El tablero final muestra un costo reducido de 0 para al menos una variable no básica.")

            mostrar_tablero_revisado(iteracion, nombre_fase, es_fase_1, base, B_inv, A_extended, c_B, c_extended, x_B, Z, n, nombres_vars_ext)

            solucion_completa = np.zeros(len(c_extended)); solucion_completa[base] = x_B
            valor_final = (c_original @ solucion_completa[:n])
            
            return {'estado': 'optimo', 'solucion': solucion_completa[:n], 'valor': Z if es_fase_1 else valor_final,
                    'base': base, 'solucion_completa': solucion_completa, 'A_ext': A_extended,
                    'c_ext': c_extended, 'b_preparado': b, 'nombres_ext': nombres_vars_ext,
                    'B_inv_optima': B_inv, 'multiples_optimos': multiples_optimos,
                    'c_original': c_original}
        
        var_entrante = seleccionar_variable_entrante(costos_reducidos, base, nombres_vars_ext)
        costo_entrante = costos_reducidos[var_entrante]
        y = B_inv @ A_extended[:, var_entrante]
        
        var_saliente, idx_saliente_en_base, estado_salida, min_ratio = seleccionar_variable_saliente(x_B, y, base, nombres_vars_ext)

        if estado_salida == 'no_acotado':
            mostrar_tablero_revisado(iteracion, nombre_fase, es_fase_1, base, B_inv, A_extended, c_B, c_extended, x_B, Z, n, nombres_vars_ext, var_entrante)
            print(f"\n🔵 Entra: {nombres_vars_ext[var_entrante]}, pero no hay variable saliente.")
            return {'estado': 'no_acotado'}
        
        # Preparar nueva base para mostrarla
        base_futura = base.copy()
        base_futura[idx_saliente_en_base] = var_entrante
        nombres_base_futura = [nombres_vars_ext[i] for i in base_futura]

        mostrar_tablero_revisado(iteracion, nombre_fase, es_fase_1, base, B_inv, A_extended, c_B, c_extended, x_B, Z, n, nombres_vars_ext, 
                                 var_entrante, var_saliente, costo_entrante, min_ratio, nombres_base_futura)
        
        base[idx_saliente_en_base] = var_entrante
        input("\n⏸️  Presione ENTER para la siguiente iteración...")
        
        if iteracion > 50: return {'estado': 'error', 'mensaje': 'Límite de iteraciones.'}


def mostrar_tablero_revisado(iteracion, nombre_fase, es_fase_1, base, B_inv, A, c_B, c, x_B, Z, n, nombres_vars_ext, 
                             var_entrante=None, var_saliente=None, costo_reducido_entrante=None, ratio_min=None, nueva_base_nombres=None):
    """Muestra el tablero simplex revisado con formato de 2 decimales y colores."""
    m = len(base)
    total_vars = len(c)
    
    mostrar_caja(f"TABLERO SIMPLEX ({nombre_fase}) - ITERACIÓN {iteracion}")
    
    headers = ['Z'] + nombres_vars_ext + ['π'] + ['LD']
    if es_fase_1: headers[0] = 'W'

    B_inv_A = B_inv @ A
    pi = c_B @ B_inv
    
    fila_Z = [1.0]
    for j in range(total_vars):
        # Mostramos c_j - z_j (negativo del costo reducido) para que coincida con el output deseado
        valor = -(c_B @ (B_inv @ A[:, j]) - c[j])
        fila_Z.append(valor)
    fila_Z.append(0.0) # Pi
    fila_Z.append(Z) 
    
    filas_rest = []
    for i in range(m):
        fila = [0.0]; fila.extend(B_inv_A[i, :]); fila.append(pi[i]); fila.append(x_B[i])
        filas_rest.append(fila)

    # Encabezados con colores
    print("  Var. Base │ ", end="")
    for j, h in enumerate(headers):
        h_coloreado = Colores.azul(h) if var_entrante is not None and j > 0 and (j-1) == var_entrante else h
        print(f"{h_coloreado:>{8 + (len(h_coloreado) - len(h))}}", end=" ")
    print("\n  " + "─"*10 + "┼" + "─"*(9 * len(headers)))

    # Fila Z/W
    nombre_obj = 'W' if es_fase_1 else 'Z'
    print(f"  {nombre_obj:^10}│ ", end="")
    for j, val in enumerate(fila_Z):
        val_f = formatear_numero(val)
        val_c = Colores.azul(val_f) if var_entrante is not None and j == var_entrante + 1 else val_f
        print(f"{val_c:>{8 + (len(val_c) - len(val_f))}}", end=" ")
    print()

    # Filas de restricciones
    for i, fila in enumerate(filas_rest):
        var_base_nombre = nombres_vars_ext[base[i]]
        es_fila_saliente = var_saliente is not None and base[i] == var_saliente
        
        var_b_most = Colores.rojo(var_base_nombre) if es_fila_saliente else var_base_nombre
        print(f"  {var_b_most:^{10 + (len(var_b_most) - len(var_base_nombre))}}│ ", end="")

        for j, val in enumerate(fila):
            val_f = formatear_numero(val)
            es_col_entrante = var_entrante is not None and j == var_entrante + 1
            
            if es_fila_saliente and es_col_entrante: val_c = Colores.morado(val_f)
            elif es_fila_saliente: val_c = Colores.rojo(val_f)
            elif es_col_entrante: val_c = Colores.azul(val_f)
            else: val_c = val_f
            print(f"{val_c:>{8+(len(val_c)-len(val_f))}}", end=" ")
        print()
    
    # --- LEYENDA DETALLADA ---
    print("\n  Leyenda:")
    if es_fase_1:
        print(f"    W: Función objetivo (Suma de Artificiales) = {formatear_numero(Z)}")
    else:
        print(f"    Z: Función objetivo = {formatear_numero(Z)}")
    print(f"    π: Variables duales (precios sombra)")
    print(f"    LD: Lado derecho (valores de variables básicas)")
    print(f"    Base actual: {[nombres_vars_ext[i] for i in base]}")

    if var_entrante is not None and costo_reducido_entrante is not None:
        print(f"\n🔵 Variable entrante: {nombres_vars_ext[var_entrante]}")
        # Se muestra el valor del tablero (c_j - z_j), que es el negativo del costo reducido (z_j - c_j)
        print(f"   Costo reducido: {formatear_numero(-costo_reducido_entrante)}")
    
    if var_saliente is not None and ratio_min is not None:
        try:
            pos_en_base = list(base).index(var_saliente)
            print(f"🔴 Variable saliente: {nombres_vars_ext[var_saliente]} (posición {pos_en_base} en base)")
        except ValueError:
            print(f"🔴 Variable saliente: {nombres_vars_ext[var_saliente]}")
        print(f"   Ratio mínimo: {formatear_numero(ratio_min)}")

    if nueva_base_nombres:
        print(f"\n📊 Nueva base: {nueva_base_nombres}")


def mostrar_solucion_final(solucion, valor, tipo, nombres_vars, multiples_optimos=False):
    """Muestra la solución óptima encontrada con formato detallado."""
    titulo = "SOLUCIÓN ÓPTIMA"
    if multiples_optimos:
        titulo += " (MÚLTIPLES SOLUCIONES EXISTEN)"
    mostrar_caja(titulo)
    
    print("  Variables de decisión:")
    punto_str = []
    for i, nombre in enumerate(nombres_vars):
        print(f"    {nombre} = {formatear_numero(solucion[i])}")
        punto_str.append(f"{nombre}={formatear_numero(solucion[i])}")

    objetivo_str = "Máximo" if tipo == 'max' else "Mínimo"
    print(f"\n  {objetivo_str} valor de Z = {formatear_numero(valor)}\n")
    
    print("  Interpretación:")
    print(f"    El valor {objetivo_str.lower()} de la función")
    print(f"    objetivo es {formatear_numero(valor)}, alcanzado en el punto:")
    print(f"    ({', '.join(punto_str)})")

    if multiples_optimos:
        print(f"\n  {Colores.verde('ℹ️  NOTA:')} Existen otras soluciones que también producen este mismo valor óptimo.")

def encontrar_siguiente_vertice_optimo(resultado_anterior, pivotes_usados=[]):
    """
    A partir de una solución óptima, realiza un pivote en una variable no básica
    con costo reducido cero para encontrar otra solución óptima.
    """
    # 1. Desempacar datos del resultado anterior
    base = resultado_anterior['base'][:] # Copia para no modificar el original
    A_ext = resultado_anterior['A_ext']
    c_ext = resultado_anterior['c_ext']
    b = resultado_anterior['b_preparado']
    nombres_ext = resultado_anterior['nombres_ext']
    n = resultado_anterior['solucion'].shape[0]
    c_original = resultado_anterior['c_original']
    tipo = 'max' if np.array_equal(c_original, c_ext[:n]) else 'min'

    # 2. Recalcular B_inv y costos reducidos para asegurar consistencia
    try:
        B_matrix = A_ext[:, base]
        B_inv = np.linalg.inv(B_matrix)
        c_B = c_ext[base]
    except np.linalg.LinAlgError:
        print("❌ Error: La matriz básica se volvió singular.")
        return None, pivotes_usados

    # 3. Encontrar variable entrante
    costos_reducidos = np.zeros(len(c_ext))
    vars_no_basicas = [i for i in range(len(c_ext)) if i not in base]
    var_entrante = -1

    # Ordenar por índice para consistencia (similar a Bland)
    vars_no_basicas.sort()

    for j in vars_no_basicas:
        costo_j = c_B @ B_inv @ A_ext[:, j] - c_ext[j]
        costos_reducidos[j] = costo_j
        # Buscar variable con costo reducido cero que no se haya usado ya para pivotar
        if abs(costo_j) < 1e-9 and j not in pivotes_usados:
            var_entrante = j
            break

    if var_entrante == -1:
        print("\nℹ️ No se encontraron más vértices óptimos alternativos.")
        return None, pivotes_usados

    print(f"\n*️⃣  Buscando siguiente solución óptima pivotando sobre '{nombres_ext[var_entrante]}'.")
    pivotes_usados.append(var_entrante)

    # 4. Realizar el pivote
    y = B_inv @ A_ext[:, var_entrante]
    x_B_actual = B_inv @ b
    
    var_saliente, idx_saliente_en_base, _, min_ratio = seleccionar_variable_saliente(x_B_actual, y, base, nombres_ext)

    if var_saliente is None:
        print("  ⚠️ No se pudo realizar el pivote (posiblemente una arista no acotada del poliedro óptimo).")
        return None, pivotes_usados

    print(f"   -> Entra: {nombres_ext[var_entrante]}, Sale: {nombres_ext[var_saliente]}")

    # 5. Actualizar base y recalcular la solución
    base[idx_saliente_en_base] = var_entrante
    
    try:
        B_matrix_nueva = A_ext[:, base]
        B_inv_nueva = np.linalg.inv(B_matrix_nueva)
    except np.linalg.LinAlgError:
        print("❌ Error: La nueva matriz básica es singular.")
        return None, pivotes_usados

    x_B_nuevo = B_inv_nueva @ b
    
    # 6. Empaquetar y devolver el nuevo resultado
    solucion_completa = np.zeros(len(c_ext))
    solucion_completa[base] = x_B_nuevo
    valor_final = c_original @ solucion_completa[:n]

    nuevo_resultado = {
        'estado': 'optimo',
        'solucion': solucion_completa[:n],
        'valor': valor_final,
        'base': base,
        'solucion_completa': solucion_completa,
        'A_ext': A_ext,
        'c_ext': c_ext,
        'b_preparado': b,
        'nombres_ext': nombres_ext,
        'B_inv_optima': B_inv_nueva,
        'multiples_optimos': True, # Sigue habiendo múltiples óptimos
        'c_original': c_original
    }
    
    return nuevo_resultado, pivotes_usados