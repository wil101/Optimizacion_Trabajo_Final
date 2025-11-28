# 📋 DOCUMENTACIÓN TÉCNICA DEL PROYECTO

## 🎯 INFORMACIÓN GENERAL

**Nombre del Proyecto:** Solucionador de Programación Lineal - Método Simplex Revisado
**Lenguaje:** Python 3.7+
**Tipo:** Aplicación de consola educativa
**Propósito:** Resolver problemas de PL paso a paso con visualización didáctica

---

## 📁 ESTRUCTURA DEL PROYECTO

```
Optimización_trabajo_final/
│
├── mian.py                      # Programa principal (1000+ líneas)
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Documentación para usuarios
├── INICIO_RAPIDO.txt           # Guía de inicio rápido
├── ejemplos_casos_prueba.py    # Casos de prueba documentados
├── instalar.bat                # Script de instalación (Windows)
├── ejecutar.bat                # Script de ejecución (Windows)
└── DOCUMENTACION_TECNICA.md    # Este archivo
```

---

## 🔧 COMPONENTES TÉCNICOS

### 1. Clase Principal: `ProgramacionLineal`

#### Atributos:
- `c`: Vector de coeficientes de función objetivo (numpy.array)
- `A`: Matriz de restricciones (numpy.array)
- `b`: Vector de lado derecho (numpy.array)
- `tipo`: 'max' o 'min'
- `num_vars`: Número de variables de decisión
- `num_restricciones`: Número de restricciones
- `nombres_vars`: Lista de nombres de variables
- `solucion_optima`: Vector solución (numpy.array)
- `valor_optimo`: Valor óptimo de Z
- `estado`: 'optimo', 'no_acotado' o 'infactible'

#### Métodos Principales:

**1. `generar_problema_ejemplo(num_vars=None)`**
- Genera automáticamente un problema de 2 o 3 variables
- Usa problemas clásicos conocidos
- Útil para demostración y pruebas

**2. `ingresar_problema_manual()`**
- Interfaz de consola para entrada manual
- Validación de entrada robusta
- Soporte para diferentes tipos de restricciones
- Retorna: bool (éxito/cancelación)

**3. `validar_factibilidad()`**
- Verificación preliminar de factibilidad
- Detecta casos trivialmente infactibles
- Retorna: str ('factible' o 'infactible')

**4. `resolver_simplex_revisado()`**
- Algoritmo principal del Método Simplex Revisado
- Iteración hasta encontrar solución o determinar no acotamiento
- Muestra tablero en cada iteración
- Actualiza base y calcula costos reducidos
- Maneja casos especiales (infactible, no acotado)

**5. `mostrar_tablero_revisado(...)`**
- Formato visual del tablero simplex
- Estructura estándar: [1 | C_B*B⁻¹*A-C | C_B*B⁻¹ | C_B*B⁻¹*b]
- Incluye variables duales (π)
- Formato tabular alineado

**6. `graficar_solucion_2d()`**
- Visualización gráfica para problemas 2D
- Usa matplotlib
- Muestra región factible, vértices y punto óptimo
- Guarda imagen PNG de alta resolución

**7. `guardar_resultado(nombre_archivo)`**
- Exporta resultado a archivo de texto
- Formato legible y completo
- Incluye problema original y solución

#### Métodos Auxiliares:

- `obtener_nombre_variable(idx, n_decision)`: Genera nombres (x1, s1, etc.)
- `mostrar_solucion_final()`: Presentación formateada de resultados
- `encontrar_vertices_region_factible()`: Cálculo de vértices (2D)
- `interseccion_lineas(i, j)`: Intersección de dos restricciones
- `es_factible(x1, x2)`: Verifica factibilidad de un punto
- `ordenar_vertices(vertices)`: Ordena vértices para polígono

---

## 🧮 ALGORITMO DEL MÉTODO SIMPLEX REVISADO

### Pseudocódigo:

```
1. INICIALIZACIÓN:
   - Convertir min a max (c = -c)
   - Agregar variables de holgura
   - Base inicial = variables de holgura
   
2. MIENTRAS no_optimo:
   a. Calcular B⁻¹ (inversa de matriz básica)
   b. Calcular solución básica: x_B = B⁻¹ * b
   c. Verificar factibilidad: si x_B < 0 → INFACTIBLE
   d. Calcular valor Z: Z = c_B * x_B
   e. Calcular costos reducidos: r_j = c_j - c_B * B⁻¹ * A_j
   
   f. SI todos r_j ≤ 0:
      → SOLUCIÓN ÓPTIMA ENCONTRADA
      
   g. SINO:
      - Seleccionar variable entrante: j = argmax(r_j > 0)
      - Calcular dirección: y = B⁻¹ * A_j
      
      - SI todos y_i ≤ 0:
         → PROBLEMA NO ACOTADO
         
      - SINO:
         - Calcular ratios: θ_i = x_B[i] / y_i para y_i > 0
         - Seleccionar variable saliente: i = argmin(θ_i)
         - Actualizar base
         
3. RETORNAR solución o estado
```

### Detalles Técnicos:

**Matriz B (Base):**
```python
B = A_extended[:, base]
```
Donde `base` es una lista de índices de columnas básicas.

**Inversa de B:**
```python
B_inv = np.linalg.inv(B)
```
Usa descomposición LU de NumPy para estabilidad numérica.

**Costos Reducidos:**
```python
r_j = c[j] - c_B @ (B_inv @ A[:, j])
```
Calculado para cada variable no básica.

**Test de Razón Mínima:**
```python
ratios = [(x_B[i] / y[i], i) if y[i] > ε else (∞, i)]
ratio_min, idx_saliente = min(ratios)
```

---

## 📊 FORMATO DEL TABLERO SIMPLEX REVISADO

### Estructura:

```
┌──────────────────────────────────────────────────┐
│     TABLERO SIMPLEX REVISADO - ITERACIÓN k       │
└──────────────────────────────────────────────────┘

Var. Base │   Z    x1    x2   ...   s1   s2   ...   π    LD
──────────┼─────────────────────────────────────────────────
    Z     │   1   -r1   -r2  ...    0    0   ...  π1..πm  Z
   s1     │   0   a11   a12  ...  b11  b12  ... b1m   xB1
   s2     │   0   a21   a22  ...  b21  b22  ... b2m   xB2
   ...    │  ...  ...   ...  ...  ...  ...  ...  ...  ...
```

### Componentes:

- **Primera fila (Z):**
  - `1` en columna Z
  - `-r_j`: Negativos de costos reducidos
  - `π`: Variables duales (c_B * B⁻¹)
  - `Z`: Valor actual de función objetivo

- **Filas siguientes (restricciones):**
  - `0` en columna Z
  - `B⁻¹ * A`: Matriz transformada
  - `B⁻¹`: Matriz inversa de base
  - `x_B`: Valores de variables básicas

---

## 🎨 VISUALIZACIÓN GRÁFICA (2D)

### Componentes de la Gráfica:

1. **Restricciones:** Líneas con colores diferentes
2. **Región Factible:** Polígono amarillo semitransparente
3. **Vértices:** Puntos negros
4. **Punto Óptimo:** Estrella roja grande
5. **Línea de Nivel:** Línea punteada roja (Z = Z*)
6. **Ejes:** Etiquetados como x₁ y x₂
7. **Leyenda:** Todas las restricciones y elementos

### Algoritmo de Graficación:

```python
1. Para cada restricción a₁x₁ + a₂x₂ ≤ b:
   - Si a₂ ≠ 0: y = (b - a₁x) / a₂
   - Graficar línea y sombrear región

2. Encontrar vértices:
   - Origen (0,0)
   - Intersecciones con ejes
   - Intersecciones entre restricciones
   
3. Filtrar vértices factibles

4. Ordenar vértices (sentido antihorario)

5. Dibujar polígono de región factible

6. Marcar punto óptimo y línea de nivel
```

---

## 🔍 VALIDACIONES IMPLEMENTADAS

### 1. Validación de Entrada:

```python
# Tipo de optimización
tipo in ['max', 'min']

# Número de variables
num_vars > 0

# Coeficientes
len(coef) == num_vars
all(isinstance(c, float))

# Restricciones
tipo_restriccion in ['<=', '>=', '=']
len(coef_restriccion) == num_vars
```

### 2. Validación de Factibilidad:

```python
# Lado derecho negativo
if any(b < 0): return 'infactible'

# Solución básica negativa
if any(x_B < -ε): return 'infactible'
```

### 3. Validación de Acotamiento:

```python
# Dirección no positiva
if all(y <= ε): return 'no_acotado'

# Ratio infinito
if ratio_min == ∞: return 'no_acotado'
```

---

## ⚙️ CONFIGURACIÓN Y PARÁMETROS

### Tolerancia Numérica:
```python
ε = 1e-9  # Tolerancia para comparaciones
```

### Precisión de Salida:
```python
np.set_printoptions(precision=4, suppress=True)
```

### Límites de Seguridad:
```python
MAX_ITERACIONES = 50
```

### Formato de Números:
```python
f"{valor:8.3f}"  # 8 caracteres, 3 decimales
f"{valor:.4f}"   # 4 decimales
```

---

## 🧪 CASOS DE PRUEBA

### Problema de Ejemplo 2D:
```
max Z = 3x₁ + 5x₂
s.a.  x₁ ≤ 4
      2x₂ ≤ 12
      3x₁ + 2x₂ ≤ 18
      x₁, x₂ ≥ 0

Solución: x₁ = 2, x₂ = 6, Z = 36
```

### Problema de Ejemplo 3D:
```
max Z = 2x₁ + 3x₂ + 4x₃
s.a.  x₁ + x₂ + x₃ ≤ 10
      2x₁ + x₂ ≤ 12
      x₂ + 2x₃ ≤ 14
      x₁, x₂, x₃ ≥ 0
```

---

## 🚨 MANEJO DE ERRORES

### Excepciones Capturadas:

1. **KeyboardInterrupt:** Usuario cancela (Ctrl+C)
2. **ValueError:** Entrada inválida
3. **LinAlgError:** Matriz singular
4. **IndexError:** Acceso fuera de rango
5. **IOError:** Error al guardar archivo

### Mensajes de Error:

- ❌ "ERROR: Matriz básica singular" → Problema degenerado
- ❌ "PROBLEMA INFACTIBLE" → Sin solución
- ⚠️ "PROBLEMA NO ACOTADO" → Z → ∞
- ⚠️ "Límite de iteraciones alcanzado" → Posible ciclaje

---

## 📈 COMPLEJIDAD COMPUTACIONAL

### Complejidad Temporal:

- **Peor caso:** O(2ⁿ) donde n = número de variables
- **Caso promedio:** O(m²n) por iteración
  - m = restricciones
  - n = variables
- **Operación más costosa:** np.linalg.inv(B) → O(m³)

### Complejidad Espacial:

- **Matriz extendida:** O(m × (n+m))
- **Almacenamiento:** O(mn)

---

## 🔄 FLUJO DE EJECUCIÓN

```
┌─────────────────┐
│  INICIO         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Menú Principal │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│Manual  │ │Ejemplo   │
└───┬────┘ └────┬─────┘
    │           │
    └─────┬─────┘
          ▼
┌──────────────────┐
│Validar           │
│Factibilidad      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│Resolver Simplex  │
│(iterativo)       │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│Óptimo  │ │No Acotado│
│        │ │Infactible│
└───┬────┘ └────┬─────┘
    │           │
    └─────┬─────┘
          ▼
┌──────────────────┐
│Mostrar Solución  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│Gráfica (2D)      │
│[Opcional]        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│Guardar Resultado │
│[Opcional]        │
└────────┬─────────┘
         │
         ▼
    ┌────────┐
    │  FIN   │
    └────────┘
```

---

## 🎓 NOTAS PEDAGÓGICAS

### Conceptos Ilustrados:

1. **Método Simplex Revisado** vs Simplex Estándar
2. **Variables de Holgura** (slack variables)
3. **Variables Duales** (precios sombra)
4. **Costos Reducidos** (reduced costs)
5. **Test de Optimalidad**
6. **Test de Razón Mínima**
7. **Región Factible** (feasible region)
8. **Vértices** (extreme points)

### Ventajas Educativas:

- ✅ Visualización paso a paso
- ✅ Explicaciones en español
- ✅ Formato tabular claro
- ✅ Identificación explícita de variables
- ✅ Gráfica interactiva (2D)

---

## 🔮 POSIBLES EXTENSIONES

### Nivel 1 (Básico):
- [ ] Exportación a PDF
- [ ] Más casos de prueba
- [ ] Modo verbose/silencioso
- [ ] Historial de iteraciones guardado

### Nivel 2 (Intermedio):
- [ ] Método de Dos Fases
- [ ] Variables artificiales
- [ ] Restricciones mixtas (≤, ≥, =)
- [ ] Análisis de sensibilidad
- [ ] Rango de variación de coeficientes

### Nivel 3 (Avanzado):
- [ ] Interfaz gráfica (Tkinter)
- [ ] Problema Dual automático
- [ ] Detección de soluciones múltiples
- [ ] Problema de Transporte
- [ ] Problema de Asignación
- [ ] Programación Entera (Branch & Bound)

---

## 📚 REFERENCIAS BIBLIOGRÁFICAS

1. Bazaraa, M.S., Jarvis, J.J., & Sherali, H.D. (2010). *Linear Programming and Network Flows*. Wiley.

2. Hillier, F.S. & Lieberman, G.J. (2015). *Introduction to Operations Research*. McGraw-Hill.

3. Luenberger, D.G. & Ye, Y. (2016). *Linear and Nonlinear Programming*. Springer.

4. Nocedal, J. & Wright, S.J. (2006). *Numerical Optimization*. Springer.

5. NumPy Documentation: https://numpy.org/doc/

6. Matplotlib Documentation: https://matplotlib.org/

---

## 👨‍💻 INFORMACIÓN DEL DESARROLLADOR

**Lenguaje:** Python 3.7+
**Librerías:** numpy, matplotlib
**Paradigma:** Programación Orientada a Objetos
**Estilo:** PEP 8 (con docstrings en español)
**Líneas de código:** ~1000
**Comentarios:** Extensivos y educativos
**Fecha:** Noviembre 2025

---

## 📄 LICENCIA

Proyecto educativo de código abierto.
Uso libre para fines académicos y educativos.

---

**Fin de la Documentación Técnica**
