# 📊 Solucionador de Programación Lineal - Método Simplex Revisado

## 🎯 Descripción

Aplicación completa en Python para resolver problemas de **Programación Lineal** usando el **Método Simplex Revisado**. La aplicación muestra paso a paso cada iteración del tablero simplex, valida la factibilidad del problema y ofrece visualización gráfica para problemas de 2 variables.

## ✨ Características Principales

### ✅ Funcionalidades Completas

1. **Interfaz de Usuario Sencilla (Consola)**
   - Ingreso manual de problemas
   - Generación automática de ejemplos (2 o 3 variables)
   - Validaciones de entrada robustas

2. **Validación de Factibilidad**
   - Detecta problemas factibles
   - Identifica problemas no acotados
   - Reconoce problemas infactibles

3. **Método Simplex Revisado**
   - Muestra cada iteración del tablero en formato estándar
   - Formato del tablero:
     ```
     [ 1 | C_B * B⁻¹ * A - C | C_B * B⁻¹ | C_B * B⁻¹ * b ]
     [ 0 |    B⁻¹ * A       |    B⁻¹    |    B⁻¹ * b    ]
     ```
   - Indica variable entrante y saliente
   - Muestra valor de Z en cada paso
   - Variables duales (precios sombra)

4. **Visualización Gráfica (2D)**
   - Gráfica de restricciones
   - Región factible sombreada
   - Vértices marcados
   - Punto óptimo destacado
   - Línea de nivel de la función objetivo

5. **Salida Clara y Educativa**
   - Explicaciones paso a paso
   - Resumen de solución óptima
   - Interpretación de resultados
   - Guardado de resultados en archivo .txt
   - Guardado de gráfica en .png

## 📋 Requisitos

### Dependencias

```bash
pip install numpy matplotlib
```

### Versión de Python
- Python 3.7 o superior

## 🚀 Instalación

1. **Clonar o descargar el archivo**
   ```bash
   # Navegar al directorio
   cd Optimización_trabajo_final
   ```

2. **Instalar dependencias**
   ```bash
   pip install numpy matplotlib
   ```

3. **Ejecutar la aplicación**
   ```bash
   python mian.py
   ```

## 📖 Uso

### Inicio Rápido

```bash
python mian.py
```

### Opciones del Menú

Al iniciar, verás:

```
📝 OPCIONES DE INGRESO:
  1. Ingresar problema manualmente
  2. Usar problema de ejemplo (2 o 3 variables aleatorio)
  3. Salir
```

### Opción 1: Ingreso Manual

Ejemplo de ingreso para el problema:
```
Maximizar Z = 3x₁ + 5x₂
Sujeto a:
  x₁ ≤ 4
  2x₂ ≤ 12
  3x₁ + 2x₂ ≤ 18
  x₁, x₂ ≥ 0
```

**Pasos:**
1. Seleccionar `max` o `min`
2. Ingresar número de variables: `2`
3. Ingresar coeficientes de función objetivo: `3 5`
4. Ingresar número de restricciones: `3`
5. Ingresar cada restricción:
   - `1 0 <= 4`
   - `0 2 <= 12`
   - `3 2 <= 18`

### Opción 2: Problema de Ejemplo

Genera automáticamente uno de estos problemas:

**Ejemplo 2D:**
```
Maximizar Z = 3x₁ + 5x₂
Restricciones:
  x₁ ≤ 4
  2x₂ ≤ 12
  3x₁ + 2x₂ ≤ 18
  x₁, x₂ ≥ 0
```

**Ejemplo 3D:**
```
Maximizar Z = 2x₁ + 3x₂ + 4x₃
Restricciones:
  x₁ + x₂ + x₃ ≤ 10
  2x₁ + x₂ ≤ 12
  x₂ + 2x₃ ≤ 14
  x₁, x₂, x₃ ≥ 0
```

## 📊 Ejemplo de Salida

### Tablero Simplex Revisado

```
┌──────────────────────────────────────────────────────────────────────────────┐
│              TABLERO SIMPLEX REVISADO - ITERACIÓN 1                          │
└──────────────────────────────────────────────────────────────────────────────┘

  Var. Base │        Z       x1       x2       s1       s2       s3        π       LD
  ──────────┼─────────────────────────────────────────────────────────────────────────
  Z         │    1.000   -3.000   -5.000    0.000    0.000    0.000    0.000    0.000
  s1        │    0.000    1.000    0.000    1.000    0.000    0.000    0.000    4.000
  s2        │    0.000    0.000    2.000    0.000    1.000    0.000    0.000   12.000
  s3        │    0.000    3.000    2.000    0.000    0.000    1.000    0.000   18.000

  Leyenda:
    Z: Función objetivo = 0.0000
    π: Variables duales (precios sombra)
    LD: Lado derecho (valores de variables básicas)
    Base actual: ['s1', 's2', 's3']
```

### Solución Final

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          SOLUCIÓN ÓPTIMA                                     │
└──────────────────────────────────────────────────────────────────────────────┘

  Variables de decisión:
    x1 = 2.0000
    x2 = 6.0000

  Máximo valor de Z = 36.0000

  Interpretación:
    El valor máximo de la función
    objetivo es 36.0000, alcanzado en el punto:
    (x1=2.0000, x2=6.0000)
```

## 🎨 Visualización Gráfica

Para problemas de 2 variables, la aplicación genera:

- **Gráfica interactiva** con matplotlib
- **Región factible** en amarillo
- **Restricciones** en diferentes colores
- **Punto óptimo** marcado con estrella roja ⭐
- **Línea de nivel** de la función objetivo
- **Guardado automático** como `solucion_grafica_pl.png`

## 📁 Archivos Generados

### resultado_pl.txt
Contiene:
- Problema original completo
- Solución óptima con todas las variables
- Valor óptimo de Z
- Interpretación

### solucion_grafica_pl.png
- Gráfica de alta resolución (300 DPI)
- Solo para problemas 2D
- Visualización completa de la solución

## 🔧 Características Técnicas

### Validaciones Implementadas
- ✅ Entradas numéricas válidas
- ✅ Coherencia de dimensiones
- ✅ Factibilidad del problema
- ✅ Detección de problemas no acotados
- ✅ Manejo de errores robusto

### Algoritmo
- **Método Simplex Revisado** con matrices inversas
- Cálculo de costos reducidos
- Test de optimalidad
- Test de razón mínima
- Variables duales (π)

### Limitaciones
- Solo restricciones de tipo `≤` (se convierten `≥` a `≤` multiplicando por -1)
- Restricciones de igualdad se tratan como `≤`
- No incluye método de dos fases (para problemas más complejos)
- Límite de 50 iteraciones por seguridad

## 🎓 Uso Educativo

Esta aplicación es ideal para:
- 📚 Estudiantes de Investigación de Operaciones
- 👨‍🏫 Profesores de Optimización
- 💼 Profesionales que necesitan resolver PL
- 🔬 Investigadores en análisis de problemas

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'numpy'"
```bash
pip install numpy matplotlib
```

### Error: "Matriz básica singular"
- El problema puede ser infactible
- Revisar las restricciones ingresadas

### La gráfica no se muestra
- Verificar que el problema tenga exactamente 2 variables
- Asegurarse de que matplotlib esté instalado

## 📝 Notas Adicionales

### Formato de Tablero Simplex Revisado

El tablero sigue la estructura estándar:
- **Primera fila (Z)**: Costos reducidos y valor de Z
- **Filas siguientes**: Solución básica actual
- **Columna π**: Variables duales (precios sombra)
- **Columna LD**: Lado derecho (valores actuales)

### Interpretación de Resultados

- **Óptimo**: Se encontró la mejor solución
- **No Acotado**: La función objetivo puede crecer infinitamente
- **Infactible**: No existe solución que satisfaga todas las restricciones

## 👥 Contribuciones

Este es un proyecto educativo. Sugerencias de mejora:
- Método de dos fases
- Soporte para restricciones mixtas
- Exportación a PDF
- Interfaz gráfica con Tkinter
- Análisis de sensibilidad

## 📄 Licencia

Proyecto educativo - Uso libre para fines académicos

## 📧 Contacto

Para preguntas o sugerencias sobre el uso de esta aplicación en contextos educativos.

---

**Desarrollado con ❤️ usando Python, NumPy y Matplotlib**
