# 📐 ESTRUCTURA REFACTORIZADA DEL PROYECTO

## 🎯 Resumen de la Refactorización

Se ha reorganizado completamente el proyecto `mian.py` (800+ líneas) en una arquitectura modular, profesional y mantenible siguiendo principios SOLID y buenas prácticas de ingeniería de software.

---

## 📁 Nueva Estructura de Archivos

```
Optimización_trabajo_final/
│
├── main.py                          # Archivo principal (orquestador) - ~170 líneas
├── utilidades.py                    # Utilidades generales - ~150 líneas
├── manejo_consola.py                # Entrada/salida de consola - ~220 líneas
├── resolucion_simplex.py            # Algoritmo Simplex Revisado - ~280 líneas
├── visualizacion_grafica.py         # Gráficas 2D - ~180 líneas
├── exportacion_resultados.py        # Exportación a archivos - ~100 líneas
├── __init__.py                      # Configuración del paquete - ~40 líneas
│
├── mian.py                          # [LEGACY] Archivo original (mantener como respaldo)
│
└── [otros archivos de documentación]
```

**Total refactorizado:** ~1,140 líneas distribuidas en 7 archivos modulares
**Original:** ~800 líneas en 1 solo archivo

---

## 🏗️ Descripción de Cada Módulo

### 1. **`main.py`** - Orquestador Principal
**Responsabilidad:** Punto de entrada y coordinación del flujo principal.

**Contenido:**
- Clase `ProgramacionLineal` simplificada (solo coordinación)
- Función `main()` que orquesta todo el flujo
- Manejo de excepciones global

**Principios aplicados:**
- Alta cohesión: Solo coordina, no implementa lógica compleja
- Bajo acoplamiento: Usa funciones importadas de otros módulos

---

### 2. **`utilidades.py`** - Utilidades Generales
**Responsabilidad:** Funciones auxiliares de propósito general.

**Contenido:**
- `Colores`: Clase con códigos ANSI para colores en consola
  - `.rojo()`, `.azul()`, `.verde()`, etc.
- `formatear_numero()`: Formatea números con decimales específicos
- `formatear_matriz()`: Formatea matrices numpy
- `obtener_nombre_variable()`: Genera nombres de variables (x1, s1, etc.)
- Funciones de validación de entrada
- Funciones de presentación (separadores, títulos, cajas)

**Mejoras implementadas:**
- ✅ **Formato de 2 decimales** en todos los números mostrados
- ✅ **Colores ANSI** para resaltar información importante

---

### 3. **`manejo_consola.py`** - Interfaz de Usuario
**Responsabilidad:** Toda la interacción con el usuario por consola.

**Contenido:**
- Funciones de ingreso de datos:
  - `ingresar_tipo_optimizacion()`
  - `ingresar_numero_variables()`
  - `ingresar_coeficientes_objetivo()`
  - `ingresar_restriccion()`
  - `ingresar_problema_completo()`
- Generación de ejemplos:
  - `generar_problema_ejemplo_2d()`
  - `generar_problema_ejemplo_3d()`
- Menú y confirmaciones:
  - `mostrar_menu_principal()`
  - `confirmar_accion()`

**Ventajas:**
- Toda la lógica de entrada está centralizada
- Fácil modificar la interfaz sin tocar el algoritmo
- Validaciones robustas incorporadas

---

### 4. **`resolucion_simplex.py`** - Algoritmo Principal
**Responsabilidad:** Implementación del Método Simplex Revisado.

**Contenido:**
- `validar_factibilidad()`: Validación preliminar
- `resolver_simplex_revisado()`: Algoritmo completo
- `mostrar_tablero_revisado()`: Visualización del tablero con colores
- `mostrar_solucion_final()`: Presentación de resultados

**Mejoras destacadas:**
- ✅ **Variables entrantes en azul** 🔵
- ✅ **Variables salientes en rojo** 🔴
- ✅ **Formato de 2 decimales** en todas las iteraciones
- ✅ Tablero perfectamente alineado con colores

**Ejemplo de salida:**
```
┌──────────────────────────────────────────────────────────────────────────────┐
│              TABLERO SIMPLEX REVISADO - ITERACIÓN 2                          │
└──────────────────────────────────────────────────────────────────────────────┘

  Var. Base │        Z       x1       x2       s1       s2       s3        π       LD
  ──────────┼─────────────────────────────────────────────────────────────────────────
  Z         │     1.00    -3.00     0.00     0.00     2.50     0.00     2.50    30.00
  s1        │     0.00     1.00     0.00     1.00     0.00     0.00     0.00     4.00
  x2        │     0.00     0.00     1.00     0.00     0.50     0.00     0.50     6.00  [AZUL]
  s3        │     0.00     3.00     0.00     0.00    -1.00     1.00    -1.00     6.00  [ROJO]

🔵 Variable entrante: x1 (columna 0)
   Costo reducido: 3.00
🔴 Variable saliente: s3 (posición 2 en base)
   Ratio mínimo: 2.00
```

---

### 5. **`visualizacion_grafica.py`** - Gráficas 2D
**Responsabilidad:** Generación de gráficas para problemas 2D.

**Contenido:**
- `encontrar_interseccion_lineas()`: Cálculo de intersecciones
- `verificar_factibilidad_punto()`: Verifica si un punto es factible
- `encontrar_vertices_region_factible()`: Encuentra vértices
- `ordenar_vertices()`: Ordena vértices para polígono
- `graficar_solucion_2d()`: Genera la gráfica completa

**Características:**
- Región factible sombreada
- Vértices marcados
- Punto óptimo destacado
- Línea de nivel de función objetivo
- Formato de 2 decimales en etiquetas

---

### 6. **`exportacion_resultados.py`** - Guardado de Archivos
**Responsabilidad:** Exportación de resultados a archivos.

**Contenido:**
- `guardar_resultado_txt()`: Guarda en formato texto
- `obtener_nombre_archivo_valido()`: Valida nombre de archivo

**Formato de salida:**
```
================================================================================
 RESULTADO DE PROGRAMACIÓN LINEAL - MÉTODO SIMPLEX REVISADO
================================================================================

PROBLEMA ORIGINAL:
--------------------------------------------------------------------------------
Maximizar Z = 3.00x1 + 5.00x2

Sujeto a:
  1.00x1 + 0.00x2 ≤ 4.00
  0.00x1 + 2.00x2 ≤ 12.00
  3.00x1 + 2.00x2 ≤ 18.00
  x1, x2 ≥ 0

SOLUCIÓN ÓPTIMA:
--------------------------------------------------------------------------------
  x1 = 2.000000
  x2 = 6.000000

  Valor máximo de Z = 36.000000
```

---

### 7. **`__init__.py`** - Configuración del Paquete
**Responsabilidad:** Configuración para usar como paquete Python.

**Contenido:**
- Metadata del paquete (`__version__`, `__author__`)
- Importaciones principales
- Lista `__all__` para exportaciones

---

## 🎨 Mejoras Visuales Implementadas

### 1. **Formato Numérico Consistente**
```python
# Antes
print(f"{valor:.4f}")  # Inconsistente

# Ahora
from utilidades import formatear_numero
print(formatear_numero(valor))  # Siempre 2 decimales
```

### 2. **Colores en Variables Básicas**
```python
# Variable entrante (azul)
🔵 x2

# Variable saliente (rojo)
🔴 s3

# Implementación con ANSI
Colores.azul("x2")  # '\033[94mx2\033[0m'
Colores.rojo("s3")  # '\033[91ms3\033[0m'
```

### 3. **Tablero Mejorado**
- Todas las celdas alineadas correctamente
- Formato de 2 decimales uniforme
- Colores que no rompen el alineamiento
- Leyenda clara al final de cada tablero

---

## 🔧 Principios de Ingeniería Aplicados

### ✅ **1. Responsabilidad Única (SRP)**
Cada módulo tiene UNA responsabilidad clara:
- `utilidades.py` → Solo utilidades generales
- `manejo_consola.py` → Solo interacción con usuario
- `resolucion_simplex.py` → Solo algoritmo simplex
- etc.

### ✅ **2. Alto Cohesión**
Funciones relacionadas están agrupadas en el mismo módulo:
- Todas las funciones de colores están en `utilidades.py`
- Todas las funciones de gráficas están en `visualizacion_grafica.py`

### ✅ **3. Bajo Acoplamiento**
Los módulos son independientes:
- Puedes cambiar `visualizacion_grafica.py` sin afectar `resolucion_simplex.py`
- Puedes reemplazar `manejo_consola.py` por una GUI sin tocar el algoritmo

### ✅ **4. DRY (Don't Repeat Yourself)**
Código reutilizado está en funciones:
```python
# En lugar de repetir formateo en cada lugar
formatear_numero(valor)  # Función centralizada
```

### ✅ **5. Nombres Autoexplicativos**
```python
# Antes
def f(x, y):  # ¿Qué hace?

# Ahora
def encontrar_interseccion_lineas(A, b, i, j):  # Clarísimo
```

### ✅ **6. Funciones Pequeñas**
Cada función hace UNA cosa:
- `ingresar_tipo_optimizacion()` → Solo pide tipo
- `ingresar_numero_variables()` → Solo pide número de variables
- etc.

---

## 🚀 Cómo Usar la Nueva Estructura

### Opción 1: Ejecutar como antes
```bash
python main.py
```

### Opción 2: Importar como paquete
```python
from resolucion_simplex import resolver_simplex_revisado
from utilidades import formatear_numero, Colores

# Usar funciones individualmente
resultado = resolver_simplex_revisado(c, A, b, 'max', 2)
print(Colores.azul("Solución encontrada!"))
```

### Opción 3: Usar módulos específicos
```python
# Solo usar las utilidades
from utilidades import Colores, formatear_numero

valor = 3.14159
print(formatear_numero(valor))  # "3.14"
print(Colores.rojo("¡Error!"))
```

---

## 📊 Comparación: Antes vs. Después

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Archivos** | 1 archivo (800 líneas) | 7 archivos (~1140 líneas) |
| **Responsabilidades** | Todo en uno | 1 responsabilidad por archivo |
| **Formato números** | Inconsistente (4 decimales) | Consistente (2 decimales) |
| **Colores** | Sin colores | Variables entrantes/salientes coloreadas |
| **Mantenibilidad** | Difícil | Fácil (módulos independientes) |
| **Testabilidad** | Difícil | Fácil (funciones pequeñas) |
| **Reutilización** | Limitada | Alta (importar módulos) |
| **Legibilidad** | Media | Alta (nombres claros) |

---

## 🎯 Ventajas de la Refactorización

### Para el Desarrollo:
1. ✅ **Fácil de mantener**: Cambios aislados en módulos específicos
2. ✅ **Fácil de testear**: Funciones pequeñas y puras
3. ✅ **Fácil de extender**: Agregar nuevas funcionalidades sin romper lo existente
4. ✅ **Fácil de documentar**: Cada módulo tiene propósito claro

### Para el Usuario:
1. ✅ **Mejor visualización**: Colores y formato consistente
2. ✅ **Más profesional**: Salida clara y organizada
3. ✅ **Más intuitivo**: Variables destacadas en cada paso

### Para el Equipo:
1. ✅ **Colaboración**: Varios desarrolladores pueden trabajar en módulos diferentes
2. ✅ **Code reviews**: Más fácil revisar archivos pequeños
3. ✅ **Onboarding**: Nuevos miembros entienden la estructura rápidamente

---

## 📝 Notas Importantes

### ⚠️ Archivo Original
- El archivo `mian.py` original se mantiene como respaldo
- **NO se eliminó** para preservar el historial
- Puedes comparar ambas versiones

### ✅ Sin Cambios en la Lógica
- El **algoritmo simplex** NO cambió
- Los **resultados** son idénticos
- Solo mejoró la **presentación** y **estructura**

### 🎨 Mejoras Visuales
- **Formato:** Todos los números con exactamente 2 decimales
- **Colores:** Variables entrantes (azul), salientes (rojo)
- **Alineación:** Tablas perfectamente alineadas incluso con colores

---

## 🔄 Migración del Código Original

Si necesitas migrar código que usaba `mian.py`:

```python
# Antes
from mian import ProgramacionLineal

# Ahora
from main import ProgramacionLineal
```

O mejor aún, usa las funciones modulares:

```python
# Más flexible
from resolucion_simplex import resolver_simplex_revisado
from visualizacion_grafica import graficar_solucion_2d
```

---

## 📚 Próximos Pasos Sugeridos

1. **Testing**: Agregar tests unitarios para cada módulo
2. **Logging**: Implementar sistema de logs
3. **GUI**: Crear interfaz gráfica (Tkinter/PyQt)
4. **CLI**: Agregar argumentos de línea de comandos
5. **Documentación**: Generar docs con Sphinx

---

## 👥 Contribuciones

Esta refactorización establece una base sólida para futuras mejoras.
Cada módulo puede evolucionar independientemente.

---

**Desarrollado con ❤️ siguiendo principios SOLID**
**Autores:** Wilmar Osorio y Santiago Alexander Losada
**Fecha:** Noviembre 2025
