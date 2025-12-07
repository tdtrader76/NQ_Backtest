# Continuar con Backtesting - Progreso actual

## 📋 Estado del proyecto

### Última actualización: 2025-12-06

---

## 🎯 Pendiente

*Tareas actuales por realizar*

---

## ✅ Completado recientemente

### Sesión actual (2025-12-06):

**1. Comparación DN vs EM21 para el año 2025**
- Archivo generado: `Resultados/Fase1/2025.xlsx`
- Script: `Scripts/comparar_niveles_DN_vs_EM21.py` (v1.0)
- 221 registros analizados (año 2025 completo)
- 4 hojas de análisis:
  1. Datos_Completos (164 columnas combinadas)
  2. Resumen_Distancias
  3. Analisis_Q1
  4. Analisis_Q4

**Resultados clave:**

Distancias entre niveles:
- **Q1 (DN vs EM21)**: Distancia media de **193.52 puntos**
  - Máxima: 1,297.50 puntos
  - Mínima: 1.00 punto
  - DN más alto que EM21: 24.89% de días

- **Q4 (DN vs EM21)**: Distancia media de **163.98 puntos**
  - Máxima: 2,074.75 puntos
  - Mínima: 0.50 puntos
  - DN más alto que EM21: 66.06% de días

Comportamiento en Q1:
- 39.37% de días: precio entre ambos Q1
- 23.53% de días: rompe Q1 más alto
  - De estos, 57.69% cierran debajo del Q1 alto
  - Solo 42.31% cierran arriba (breakout real)
- De los que quedan entre Q1: 55.17% cierran debajo del Q1 bajo

Comportamiento en Q4:
- 23.08% de días: precio entre ambos Q4
- 23.08% de días: rompe Q4 más bajo
  - De estos, 60.78% cierran arriba (reversión)
  - Solo 39.22% cierran debajo del Q4 bajo
- De los que quedan entre Q4: 78.43% cierran arriba del Q4 alto

**2. Filtrado de distancias mínimas (≤50 puntos)**
- Archivo generado: `Resultados/Fase1/2025_actualizado.xlsx`
- Script: `Scripts/filtrar_distancias_minimas.py` (v1.0)
- 3 hojas adicionales creadas:
  1. Q1_Distancia_Minima
  2. Q4_Distancia_Minima
  3. Resumen_Distancias_Minimas

**Resultados clave:**

Días con distancia Q1 ≤ 50 puntos:
- **29 días encontrados** (13.12% del total)
- Distancia Q1 mínima: **1.00 punto**
- Distancia Q1 promedio (filtrados): **22.52 puntos**

Días con distancia Q4 ≤ 50 puntos:
- **40 días encontrados** (18.10% del total)
- Distancia Q4 mínima: **0.50 puntos**
- Distancia Q4 promedio (filtrados): **24.67 puntos**

Días que cumplen ambos criterios:
- **6 días** con Q1 y Q4 simultáneamente ≤50 puntos
- Representa **2.71%** del total de días en 2025

---

## ✅ Completado recientemente

### Sesión anterior (2025-12-04):

1. **Cálculo de niveles DN (Día Normal)** - One Day y Three Days
   - Archivo: `Datos_Diarios_DN_Niveles.xlsx`
   - 1,189 registros históricos procesados (2020-2025)
   - 96 columnas de niveles calculados
   - 16 hojas de análisis total

2. **Filtrado de datos 2025**
   - 221 registros del año 2025
   - 7 hojas adicionales con estadísticas específicas
   - Comparativas con promedios históricos

### Resultados clave:
- **Q1 = High del día anterior** (resistencia)
- **Q4 = Low del día anterior** (soporte)
- **68% de reversión** cuando toca Q1
- **81% de reversión** cuando toca Q4
- 2025 muestra **mayor volatilidad** que promedio histórico

---

## 📊 Archivos importantes

- **Datos principales:**
  - `Resultados/Fase1/Datos_Diarios_DN_Niveles.xlsx` (histórico DN 2020-2025)
  - `Resultados/Fase1/2025.xlsx` (comparación DN vs EM21)
  - `Resultados/Fase1/2025_actualizado.xlsx` (con filtros de distancias mínimas)
- **Scripts:**
  - `Scripts/calcular_niveles_DN.py` (v1.1)
  - `Scripts/filtrar_datos_2025_DN.py` (v1.0)
  - `Scripts/comparar_niveles_DN_vs_EM21.py` (v1.0)
  - `Scripts/filtrar_distancias_minimas.py` (v1.0)
- **Documentación anterior:** `Prueba/continuarold.md`

---

## 📝 Notas

*Agregar notas importantes aquí*
