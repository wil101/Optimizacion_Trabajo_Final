"""
==================================================================================
MÓDULO DE UTILIDADES
==================================================================================
Funciones auxiliares para formato, colores y validaciones.
==================================================================================
"""


# ==================================================================================
# CÓDIGOS DE COLOR ANSI
# ==================================================================================

class Colores:
    """Códigos ANSI para colorear texto en consola."""
    ROJO = '\033[91m'
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BLANCO = '\033[97m'
    NEGRITA = '\033[1m'
    SUBRAYADO = '\033[4m'
    RESET = '\033[0m'
    
    @staticmethod
    def rojo(texto):
        """Retorna texto en rojo."""
        return f"{Colores.ROJO}{texto}{Colores.RESET}"
    
    @staticmethod
    def azul(texto):
        """Retorna texto en azul."""
        return f"{Colores.AZUL}{texto}{Colores.RESET}"
    
    @staticmethod
    def verde(texto):
        """Retorna texto en verde."""
        return f"{Colores.VERDE}{texto}{Colores.RESET}"
    
    @staticmethod
    def amarillo(texto):
        """Retorna texto en amarillo."""
        return f"{Colores.AMARILLO}{texto}{Colores.RESET}"
    
    @staticmethod
    def negrita(texto):
        """Retorna texto en negrita."""
        return f"{Colores.NEGRITA}{texto}{Colores.RESET}"


# ==================================================================================
# FUNCIONES DE FORMATO
# ==================================================================================

def formatear_numero(valor, decimales=2):
    """
    Formatea un número con cantidad específica de decimales.
    
    Args:
        valor: Número a formatear
        decimales: Cantidad de decimales (default: 2)
    
    Returns:
        str: Número formateado
    """
    return f"{valor:.{decimales}f}"


def formatear_matriz(matriz, decimales=2):
    """
    Formatea todos los elementos de una matriz con decimales específicos.
    
    Args:
        matriz: Matriz numpy a formatear
        decimales: Cantidad de decimales
    
    Returns:
        str: Representación formateada de la matriz
    """
    filas = []
    for fila in matriz:
        elementos = [formatear_numero(val, decimales) for val in fila]
        filas.append("  [" + ", ".join(elementos) + "]")
    return "[\n" + "\n".join(filas) + "\n]"


def obtener_nombre_variable(idx, n_decision):
    """
    Retorna el nombre de una variable según su índice.
    
    Args:
        idx: Índice de la variable
        n_decision: Número de variables de decisión
    
    Returns:
        str: Nombre de la variable (x1, x2, s1, s2, etc.)
    """
    if idx < n_decision:
        return f"x{idx+1}"
    else:
        return f"s{idx - n_decision + 1}"


# ==================================================================================
# FUNCIONES DE VALIDACIÓN
# ==================================================================================

def validar_numero_positivo(texto_prompt):
    """
    Solicita un número positivo al usuario con validación.
    
    Args:
        texto_prompt: Texto a mostrar al usuario
    
    Returns:
        int: Número positivo ingresado
    """
    while True:
        try:
            valor = int(input(texto_prompt))
            if valor > 0:
                return valor
            print("⚠️  Debe ser un número positivo")
        except ValueError:
            print("⚠️  Por favor ingrese un número válido")


def validar_lista_numeros(texto_prompt, cantidad_esperada):
    """
    Solicita una lista de números al usuario con validación.
    
    Args:
        texto_prompt: Texto a mostrar al usuario
        cantidad_esperada: Cantidad de números esperados
    
    Returns:
        list: Lista de números ingresados
    """
    while True:
        try:
            entrada = input(texto_prompt)
            numeros = [float(x) for x in entrada.split()]
            if len(numeros) == cantidad_esperada:
                return numeros
            print(f"⚠️  Debe ingresar exactamente {cantidad_esperada} números")
        except ValueError:
            print("⚠️  Por favor ingrese números válidos separados por espacio")


def validar_opcion(opciones_validas):
    """
    Valida que la entrada del usuario esté en las opciones válidas.
    
    Args:
        opciones_validas: Lista de opciones válidas
    
    Returns:
        str: Opción válida seleccionada
    """
    while True:
        opcion = input("\n Seleccione una opción: ").strip().lower()
        if opcion in opciones_validas:
            return opcion
        print(f"⚠️  Opción inválida. Opciones válidas: {', '.join(opciones_validas)}")


# ==================================================================================
# FUNCIONES DE PRESENTACIÓN
# ==================================================================================

def mostrar_separador(tipo='igual', ancho=80):
    """
    Muestra un separador en consola.
    
    Args:
        tipo: Tipo de separador ('igual', 'guion', 'punto')
        ancho: Ancho del separador
    """
    caracteres = {
        'igual': '=',
        'guion': '─',
        'punto': '·'
    }
    print(caracteres.get(tipo, '=') * ancho)


def mostrar_titulo(titulo, ancho=80):
    """
    Muestra un título centrado con separadores.
    
    Args:
        titulo: Texto del título
        ancho: Ancho total
    """
    print("\n" + "="*ancho)
    print(f"  {titulo}")
    print("="*ancho + "\n")


def mostrar_caja(titulo, ancho=78):
    """
    Muestra un título en una caja con bordes Unicode.
    
    Args:
        titulo: Texto a mostrar
        ancho: Ancho de la caja
    """
    print("┌" + "─"*ancho + "┐")
    print(f"│ {titulo:^{ancho-2}} │")
    print("└" + "─"*ancho + "┘\n")
