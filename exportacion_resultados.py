"""
==================================================================================
MÓDULO DE EXPORTACIÓN DE RESULTADOS
==================================================================================
Funciones para guardar resultados en archivos.
==================================================================================
"""

from utilidades import formatear_numero


# ==================================================================================
# EXPORTACIÓN A ARCHIVO DE TEXTO
# ==================================================================================

def guardar_resultado_txt(nombre_archivo, c, A, b, tipo, num_vars, num_restricciones,
                         nombres_vars, solucion, valor, estado):
    """
    Guarda el resultado en un archivo de texto.
    
    Args:
        nombre_archivo: Nombre del archivo a crear
        c: Vector de coeficientes de función objetivo
        A: Matriz de restricciones
        b: Vector de lado derecho
        tipo: 'max' o 'min'
        num_vars: Número de variables
        num_restricciones: Número de restricciones
        nombres_vars: Lista de nombres de variables
        solucion: Vector solución (o None)
        valor: Valor óptimo de Z (o None)
        estado: Estado del problema ('optimo', 'no_acotado', 'infactible')
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write(" RESULTADO DE PROGRAMACIÓN LINEAL - MÉTODO SIMPLEX REVISADO\n")
            f.write("="*80 + "\n\n")
            
            # Problema original
            f.write("PROBLEMA ORIGINAL:\n")
            f.write("-"*80 + "\n")
            objetivo = "Maximizar" if tipo == 'max' else "Minimizar"
            f.write(f"{objetivo} Z = ")
            
            # Construir función objetivo
            terminos = []
            for i in range(num_vars):
                coef = formatear_numero(c[i], 2)
                terminos.append(f"{coef}{nombres_vars[i]}")
            f.write(" + ".join(terminos) + "\n\n")
            
            # Restricciones
            f.write("Sujeto a:\n")
            for i in range(num_restricciones):
                terminos = []
                for j in range(num_vars):
                    coef = formatear_numero(A[i,j], 2)
                    terminos.append(f"{coef}{nombres_vars[j]}")
                f.write(f"  {' + '.join(terminos)} ≤ {formatear_numero(b[i], 2)}\n")
            
            f.write(f"  {', '.join(nombres_vars)} ≥ 0\n\n")
            
            # Solución
            if estado == 'optimo':
                f.write("SOLUCIÓN ÓPTIMA:\n")
                f.write("-"*80 + "\n")
                for i, nombre in enumerate(nombres_vars):
                    f.write(f"  {nombre} = {formatear_numero(solucion[i], 6)}\n")
                f.write(f"\n  Valor {'máximo' if tipo == 'max' else 'mínimo'} de Z = {formatear_numero(valor, 6)}\n")
            elif estado == 'no_acotado':
                f.write("RESULTADO: Problema NO ACOTADO\n")
                f.write("-"*80 + "\n")
                f.write("La función objetivo puede crecer indefinidamente.\n")
            elif estado == 'infactible':
                f.write("RESULTADO: Problema INFACTIBLE\n")
                f.write("-"*80 + "\n")
                f.write("No existe solución que satisfaga todas las restricciones.\n")
            
            f.write("\n" + "="*80 + "\n")
        
        print(f"\n✅ Resultado guardado en: {nombre_archivo}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error al guardar archivo: {e}")
        return False


def obtener_nombre_archivo_valido(nombre_default="resultado_pl.txt"):
    """
    Solicita y valida el nombre de archivo para guardar.
    
    Args:
        nombre_default: Nombre por defecto
    
    Returns:
        str: Nombre de archivo válido
    """
    nombre = input(f"Nombre del archivo (Enter para '{nombre_default}'): ").strip()
    
    if not nombre:
        nombre = nombre_default
    
    if not nombre.endswith('.txt'):
        nombre += '.txt'
    
    return nombre
