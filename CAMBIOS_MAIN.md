# 📋 CAMBIOS REALIZADOS EN `main.py`

## ✅ Modificaciones Implementadas

### 1. **Análisis de Sensibilidad Post-Óptimo** 🔍

Se agregó un análisis completo de sensibilidad que se ejecuta automáticamente después de encontrar la solución óptima. Incluye:

#### **A. Precios Sombra (Variables Duales π)**
- Calcula el valor marginal de cada recurso
- Indica cuánto cambia Z por cada unidad adicional del lado derecho
- **Interpretación con colores:**
  - 🟢 **Verde**: Aumentar el recurso MEJORA Z
  - 🔴 **Rojo**: Aumentar el recurso EMPEORA Z  
  - 🔵 **Azul**: Restricción NO activa (holgura disponible)

**Ejemplo de salida:**
```
π1 (Restricción 1): +2.50
   → Aumentar b1 en 1 unidad AUMENTA Z en 2.50

π2 (Restricción 2): 0.00
   → Restricción NO activa (holgura disponible)
```

#### **B. Rangos de Variación del Lado Derecho (b)**
- Calcula el intervalo en que puede variar cada `b_i` sin cambiar la base óptima
- Muestra valores mínimos y máximos
- Indica cuánto puede aumentar o disminuir cada recurso

**Ejemplo de salida:**
```
b1 (actualmente 4.00):
   Mínimo: 2.00 (puede disminuir hasta 2.00)
   Máximo: 6.00 (puede aumentar hasta 2.00)
   Rango: [2.00, 6.00]
```

#### **C. Rangos de Variación de Coeficientes Objetivo (c)**
- Calcula cuánto puede variar cada `c_j` manteniendo la solución óptima
- Solo para variables básicas (en la solución)
- Ayuda a evaluar robustez de la solución ante cambios en precios/costos

**Ejemplo de salida:**
```
x1 (actualmente c = 3.00):
   Mínimo: 2.50
   Máximo: 4.00
   Rango: [2.50, 4.00]
```

#### **D. Estado de las Restricciones**
- Identifica restricciones **ACTIVAS** (saturadas, holgura = 0)
- Identifica restricciones **NO ACTIVAS** (con holgura disponible)
- Código de colores visual

**Ejemplo de salida:**
```
Restricción 1 (s1): ACTIVA - Holgura = 0.00 (saturada)
Restricción 2 (s2): NO ACTIVA - Holgura = 3.50
```

---

### 2. **Formato de Dos Decimales** 📊

- **Todos los números** se muestran con exactamente **2 decimales**
- Utiliza la función `formatear_numero()` de `utilidades.py`
- Aplicado en:
  - Tableros simplex
  - Solución final
  - Análisis de sensibilidad
  - Rangos de variación
  - Precios sombra

**Antes:**
```
x1 = 2.000000
Z = 36.000000
```

**Ahora:**
```
x1 = 2.00
Z = 36.00
```

---

### 3. **Colores en Consola** 🎨

#### **Variables en Iteraciones:**
- 🔵 **AZUL**: Variable que **ENTRA** a la base
- 🔴 **ROJO**: Variable que **SALE** de la base

**Ejemplo en tablero:**
```
🔵 Variable entrante: x2 (columna 1)
   Costo reducido: 5.00

🔴 Variable saliente: s3 (posición 2 en base)
   Ratio mínimo: 6.00

📊 Nueva base: [s1, s2, x2]
```

#### **Colores en Análisis de Sensibilidad:**
- 🟢 **Verde**: Mejoras/aumentos positivos
- 🔴 **Rojo**: Decrementos/restricciones activas
- 🔵 **Azul**: Valores actuales/restricciones no activas

**Implementación técnica:**
```python
# Códigos ANSI desde utilidades.py
Colores.azul("texto")    # Variable entrante
Colores.rojo("texto")    # Variable saliente
Colores.verde("texto")   # Mejoras
```

---

## 🔧 Cambios Técnicos en el Código

### Nuevas Importaciones
```python
import numpy as np  # Para cálculos de sensibilidad
from utilidades import (
    mostrar_titulo, 
    mostrar_caja, 
    formatear_numero, 
    obtener_nombre_variable, 
    Colores
)
```

### Nuevos Atributos en `ProgramacionLineal`
```python
self.base_optima = None      # Base óptima para sensibilidad
self.B_inv_optima = None     # Inversa de base (no usado actualmente)
```

### Nuevo Método: `analisis_sensibilidad()`
- **Ubicación**: Después de `mostrar_grafica()`
- **Llamado**: Automáticamente al encontrar solución óptima
- **Interactivo**: Pregunta si desea realizar el análisis
- **Completo**: ~150 líneas de análisis detallado

### Modificaciones en `resolver()`
```python
if self.estado == 'optimo':
    self.solucion_optima = resultado['solucion']
    self.valor_optimo = resultado['valor']
    self.base_optima = resultado.get('base')  # NUEVO
    mostrar_solucion_final(...)
    
    # Análisis de sensibilidad automático
    if self.base_optima is not None:
        self.analisis_sensibilidad()  # NUEVO
```

---

## 📊 Flujo de Ejecución Actualizado

```
1. Menú Principal
   ↓
2. Ingresar/Generar Problema
   ↓
3. Validación de Factibilidad
   ↓
4. Método Simplex Revisado
   │  • Muestra cada iteración con COLORES
   │  • Variables entrantes en AZUL 🔵
   │  • Variables salientes en ROJO 🔴
   │  • Formato de 2 decimales en todos los números
   ↓
5. Solución Óptima
   │  • Variables con 2 decimales
   │  • Valor óptimo con 2 decimales
   ↓
6. ✨ ANÁLISIS DE SENSIBILIDAD ✨ (NUEVO)
   │  • Precios sombra con colores
   │  • Rangos de variación de b
   │  • Rangos de variación de c
   │  • Estado de restricciones
   ↓
7. Gráfica 2D (si aplica)
   ↓
8. Guardar Resultado
```

---

## 💡 Interpretación del Análisis de Sensibilidad

### **¿Qué son los Precios Sombra?**
- Valor marginal de cada recurso
- Indica cuánto vale "una unidad más" de cada restricción
- **π > 0**: El recurso es valioso (aumentarlo mejora Z)
- **π = 0**: El recurso sobra (no es cuello de botella)
- **π < 0**: Solo en minimización (menos común)

### **¿Para qué sirven los Rangos de Variación?**

**Rangos de b (recursos):**
- Determinan la **robustez** de la solución
- Indican cuánto puede cambiar la disponibilidad sin replantear
- Útil para negociaciones con proveedores

**Rangos de c (precios/costos):**
- Determinan la **sensibilidad** de la decisión óptima
- Indican cuánto puede variar un precio sin cambiar el plan
- Útil para análisis de mercado

### **¿Qué significa una Restricción Activa?**
- **ACTIVA**: Totalmente utilizada (holgura = 0)
  - Es un cuello de botella
  - Tiene precio sombra > 0
  - Aumentar su capacidad mejora Z
  
- **NO ACTIVA**: Con capacidad sobrante
  - No es limitante
  - Precio sombra = 0
  - Aumentar capacidad no cambia Z

---

## 🎯 Ventajas de las Mejoras

### **1. Mejor Visualización**
- ✅ Colores hacen más fácil seguir el algoritmo
- ✅ Variables entrantes/salientes se identifican al instante
- ✅ Formato consistente de 2 decimales más legible

### **2. Análisis Profesional**
- ✅ Información completa post-óptima
- ✅ Decisiones informadas sobre recursos
- ✅ Evaluación de robustez de la solución

### **3. Valor Educativo**
- ✅ Estudiantes entienden mejor el proceso
- ✅ Conexión teoría-práctica más clara
- ✅ Interpretación económica visible

### **4. Aplicabilidad Real**
- ✅ Información útil para toma de decisiones
- ✅ Análisis "what-if" sin resolver de nuevo
- ✅ Identificación de cuellos de botella

---

## 📝 Ejemplo Completo de Salida

### **Solución Óptima:**
```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            SOLUCIÓN ÓPTIMA                                   │
└──────────────────────────────────────────────────────────────────────────────┘

  Variables de decisión:
    x1 = 2.00
    x2 = 6.00

  Máximo valor de Z = 36.00

  Interpretación:
    El valor máximo de la función
    objetivo es 36.00, alcanzado en el punto:
    (x1=2.00, x2=6.00)
```

### **Análisis de Sensibilidad:**
```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      1. PRECIOS SOMBRA (π)                                   │
└──────────────────────────────────────────────────────────────────────────────┘

  π1 (Restricción 1): 0.00
     → Restricción NO activa (holgura disponible)

  π2 (Restricción 2): +2.50
     → Aumentar b2 en 1 unidad AUMENTA Z en 2.50

  π3 (Restricción 3): +0.50
     → Aumentar b3 en 1 unidad AUMENTA Z en 0.50

┌──────────────────────────────────────────────────────────────────────────────┐
│               2. RANGOS DE VARIACIÓN DEL LADO DERECHO (b)                    │
└──────────────────────────────────────────────────────────────────────────────┘

  b1 (actualmente 4.00):
     Mínimo: 2.00 (puede disminuir hasta 2.00)
     Máximo: +∞ (sin límite superior)
     Rango: [2.00, +∞]

  b2 (actualmente 12.00):
     Mínimo: 6.00 (puede disminuir hasta 6.00)
     Máximo: 24.00 (puede aumentar hasta 12.00)
     Rango: [6.00, 24.00]

[... más análisis ...]
```

---

## ⚠️ Notas Importantes

### **Lo que NO se modificó:**
- ❌ NO se cambiaron otros archivos (utilidades.py, resolucion_simplex.py, etc.)
- ❌ NO se modificó el algoritmo simplex (solo visualización)
- ❌ NO se cambiaron las funciones de entrada/salida
- ❌ NO se alteró la estructura de módulos

### **Lo que SÍ se modificó:**
- ✅ Solo el archivo `main.py`
- ✅ Solo se agregaron funcionalidades nuevas
- ✅ Código existente se mantiene funcional
- ✅ Compatibilidad total con módulos originales

---

## 🚀 Cómo Usar las Nuevas Funcionalidades

### **1. Ejecutar el Programa:**
```bash
python main.py
```

### **2. Seleccionar Opción:**
- Opción 1: Ingresar problema manualmente
- Opción 2: Usar ejemplo (recomendado para ver análisis)

### **3. Observar las Iteraciones:**
- Variables entrantes aparecen en **AZUL** 🔵
- Variables salientes aparecen en **ROJO** 🔴
- Todos los números con **2 decimales**

### **4. Análisis de Sensibilidad:**
- Al encontrar solución óptima, se pregunta si desea análisis
- Presionar 's' para ver análisis completo
- Presionar 'n' para omitir

### **5. Interpretar Resultados:**
- Identificar restricciones activas (cuellos de botella)
- Revisar precios sombra (recursos valiosos)
- Evaluar rangos (robustez de la solución)

---

## 📚 Referencias Técnicas

### **Fórmulas Implementadas:**

**Precios Sombra:**
```
π = C_B × B⁻¹
```

**Rangos de b:**
```
b_i_min = b_i + δ_min
b_i_max = b_i + δ_max

donde δ se calcula de: x_B_k / B⁻¹_ki
```

**Costos Reducidos:**
```
r_j = c_j - C_B × B⁻¹ × A_j
```

---

## ✅ Checklist de Implementación

- [x] Análisis de sensibilidad completo
- [x] Formato de 2 decimales en toda la aplicación
- [x] Colores azul/rojo en variables entrantes/salientes
- [x] Precios sombra con interpretación
- [x] Rangos de variación de b
- [x] Rangos de variación de c
- [x] Estado de restricciones (activas/no activas)
- [x] Código con colores en análisis
- [x] Sin modificar otros archivos
- [x] Compatibilidad total con módulos existentes
- [x] Documentación completa

---

**Desarrollado con ❤️ por Wilmar Osorio y Santiago Alexander Losada**  
**Fecha:** Noviembre 2025  
**Versión:** 2.0 con Análisis de Sensibilidad
