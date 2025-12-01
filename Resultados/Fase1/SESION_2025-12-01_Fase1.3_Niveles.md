# 📊 Documentación Sesión - Fase 1.3: Cálculo de Niveles con Expected Move

**Fecha:** 2025-12-01  
**Fase:** 1.3 - Cálculo de Niveles  
**Estado:** ✅ Completado

---

## 🎯 Objetivo de la Sesión

Implementar el cálculo del Expected Move (EM) para cada día de trading y calcular todos los niveles con ajuste de Skew según la metodología definida en `calculos.md`.

---

## 📋 Tareas Realizadas

### 1. Cálculo del Expected Move (EM)

#### 1.1 Fórmula Implementada (basada en RyFHEM.cs)

```
EMH (Expected Move High) = Open + (avgBullishMove × 0.682)
EML (Expected Move Low) = Open - (avgBearishMove × 0.682)
ExpRange = EMH - EML

Donde:
- avgBullishMove = promedio de rangos (High-Low) de días alcistas (Close > Open)
- avgBearishMove = promedio de rangos (High-Low) de días bajistas (Close <= Open)
- 0.682 = multiplicador de desviación estándar (68.2%)
- Lookback = período de días históricos para calcular promedios
```

#### 1.2 Script Creado

**Archivo:** `Scripts/fase1_agregar_expected_move_excel.py`

**Funcionalidad:**
- Carga datos diarios limpios desde `Procesados/NQ_Daily_2020-2025_Limpio.csv`
- Calcula Expected Move para cada día usando ventana histórica (lookback)
- Actualiza archivo Excel `Datos_Diarios_por_Año.xlsx` agregando columnas:
  - **EMH**: Expected Move High
  - **EML**: Expected Move Low
  - **ExpRange**: Rango esperado (EMH - EML)
- Redondea valores al cuarto más cercano (.00, .25, .50, .75)

#### 1.3 Archivos Generados con EM

**A. Expected Move con 21 días de lookback:**
- `Resultados/Fase1/Datos_Diarios_por_Año.xlsx` (archivo principal)
  - Días válidos: 1,168 de 1,189
  - EMH promedio: 16,864.48
  - EML promedio: 16,440.79
  - ExpRange promedio: 423.69

**B. Expected Move con 9 días de lookback:**
- `Resultados/Fase1/Datos_Diarios_por_Año_EM9.xlsx` (archivo comparativo)
  - Días válidos: 1,180 de 1,189
  - EMH promedio: 16,827.01
  - EML promedio: 16,404.36
  - ExpRange promedio: 422.66

**Observaciones:**
- Con 9 días hay más días válidos (necesita menos datos históricos)
- ExpRange promedio muy similar entre ambos períodos (diferencia de ~1 punto)
- Valores ligeramente más bajos con 9 días (reacciona más rápido a cambios recientes)

---

### 2. Extracción de Datos del Año 2025

#### 2.1 Archivos Creados

Se extrajeron los datos del año 2025 de ambos archivos principales:

**Expected Move 21 días:**
- `Resultados/Fase1/Datos_2025_EM21.xlsx`
- `Resultados/Fase1/Datos_2025_EM21.csv`

**Expected Move 9 días:**
- `Resultados/Fase1/Datos_2025_EM9.xlsx`
- `Resultados/Fase1/Datos_2025_EM9.csv`

**Registros:** 221 días de trading del año 2025

#### 2.2 Limpieza de Columnas

Se eliminaron las columnas de validación:
- Columna I: `H>=L` (validación High >= Low)
- Columna J: `Valid_Range` (validación de rangos)

**Columnas finales:**
1. Date
2. Open
3. High
4. Low
5. Close
6. Volume
7. Range
8. Return_%
9. EMH
10. EML
11. ExpRange

---

### 3. Cálculo de Niveles con Skew

#### 3.1 Metodología Implementada

Basada en el documento `C:\Users\oscar\Documents\Proyecto-Trading\Pruebaniveles\calculos.md`

**Conceptos clave:**
- **Q1 (Quartile 1)**: Nivel superior del rango (EMH)
- **Q4 (Quartile 4)**: Nivel inferior del rango (EML)
- **NR2**: Nivel de referencia (Open del día)
- **Skew**: Asimetría de la distribución respecto al Open

**Cálculo del Skew:**
```
PctAboveNR2 = ((Q1 - NR2) / RangoTotal) × 100
PctBelowNR2 = ((NR2 - Q4) / RangoTotal) × 100
SkewMayor = max(PctAboveNR2, PctBelowNR2)
DiferenciaSkew = |SkewMayor - 50%|
```

**Niveles calculados:**

1. **Niveles base (sin ajuste de skew):**
   - TCH = Q1 - 12.5% del rango total
   - TCL = Q1 - 15.9% del rango total
   - TVH = Q1 - 87.5% del rango total
   - TVL = Q1 - 93.75% del rango total

2. **Niveles con ajuste de skew:**
   - Z2H = Q1 - (34.1% + DiferenciaSkew) del rango total → redondeado a 0.25
   - Z2L = Q1 - (37.5% + DiferenciaSkew) del rango total → redondeado a 0.25
   - Z3H = Q4 + (37.5% + DiferenciaSkew) del rango total → redondeado a 0.25
   - Z3L = Q4 + (34.1% + DiferenciaSkew) del rango total → redondeado a 0.25

3. **Niveles derivados:**
   - Q2 = (TCL + Z2H) / 2
   - Q3 = (TVH + Z3L) / 2

#### 3.2 Script Creado

**Archivo:** `Scripts/fase1_calcular_niveles_skew.py`

**Funcionalidad:**
- Calcula todos los niveles con ajuste de skew
- Procesa ambos archivos (EM21 y EM9)
- Genera archivos Excel y CSV con todos los niveles

#### 3.3 Archivos Finales Generados

**Expected Move 21 días con Niveles:**
- `Resultados/Fase1/Datos_2025_EM21_Niveles.xlsx`
- `Resultados/Fase1/Datos_2025_EM21_Niveles.csv`
  - Rango Total promedio: 552.58 puntos
  - Diferencia Skew promedio: 4.16%

**Expected Move 9 días con Niveles:**
- `Resultados/Fase1/Datos_2025_EM9_Niveles.xlsx`
- `Resultados/Fase1/Datos_2025_EM9_Niveles.csv`
  - Rango Total promedio: 550.16 puntos
  - Diferencia Skew promedio: 5.78%

**Columnas en archivos finales (29 columnas):**

| Grupo | Columnas |
|-------|----------|
| **Datos básicos** | Date, Open, High, Low, Close, Volume, Range, Return_% |
| **Niveles base** | Q1, Q4, NR2, RangoTotal |
| **Análisis Skew** | PctAboveNR2, PctBelowNR2, SkewMayor, DiferenciaSkew |
| **Niveles superiores** | TCH, TCL, Q2, Z2H, Z2L |
| **Niveles inferiores** | Z3H, Z3L, Q3, TVH, TVL |
| **Expected Move** | EMH, EML, ExpRange |

---

## 📊 Resultados y Estadísticas

### Comparación EM21 vs EM9

| Métrica | EM21 (21 días) | EM9 (9 días) | Diferencia |
|---------|----------------|--------------|------------|
| Días válidos (total) | 1,168 / 1,189 | 1,180 / 1,189 | +12 días |
| EMH promedio | 16,864.48 | 16,827.01 | -37.47 |
| EML promedio | 16,440.79 | 16,404.36 | -36.43 |
| ExpRange promedio | 423.69 | 422.66 | -1.03 |
| Rango Total 2025 | 552.58 | 550.16 | -2.42 |
| Diferencia Skew 2025 | 4.16% | 5.78% | +1.62% |

**Observaciones:**
- EM9 tiene mayor diferencia de skew (5.78% vs 4.16%), indicando mayor asimetría
- EM9 reacciona más rápido a cambios recientes (ventana más corta)
- Rangos muy similares entre ambos métodos
- EM21 más estable, EM9 más reactivo

---

## 🗂️ Estructura de Archivos Generada

```
NQ_Backtest/
├── Scripts/
│   ├── fase1_agregar_expected_move_excel.py  ✅ Nuevo
│   └── fase1_calcular_niveles_skew.py        ✅ Nuevo
│
├── Resultados/Fase1/
│   ├── Datos_Diarios_por_Año.xlsx            ✅ Actualizado (EM21)
│   ├── Datos_Diarios_por_Año_EM9.xlsx        ✅ Nuevo (EM9)
│   │
│   ├── Datos_2025_EM21.xlsx                  ✅ Nuevo
│   ├── Datos_2025_EM21.csv                   ✅ Nuevo
│   ├── Datos_2025_EM9.xlsx                   ✅ Nuevo
│   ├── Datos_2025_EM9.csv                    ✅ Nuevo
│   │
│   ├── Datos_2025_EM21_Niveles.xlsx          ✅ Nuevo (FINAL)
│   ├── Datos_2025_EM21_Niveles.csv           ✅ Nuevo (FINAL)
│   ├── Datos_2025_EM9_Niveles.xlsx           ✅ Nuevo (FINAL)
│   └── Datos_2025_EM9_Niveles.csv            ✅ Nuevo (FINAL)
│
└── Logs/
    ├── fase1_agregar_expected_move.log       ✅ Nuevo
    └── fase1_calcular_niveles_skew.log       ✅ Nuevo
```

---

## 🔧 Scripts Desarrollados

### 1. fase1_agregar_expected_move_excel.py

**Propósito:** Calcular Expected Move y actualizar Excel

**Parámetros configurables:**
- `EXCEL_PATH`: Ruta del archivo Excel a actualizar
- `DATA_PATH`: Ruta de datos diarios limpios
- `RANGE_MULTIPLIER`: 0.682 (constante)
- `DEFAULT_LOOKBACK`: 21 o 9 días

**Funciones principales:**
- `cargar_datos()`: Carga CSV de datos limpios
- `calcular_expected_move(df, lookback)`: Calcula EM para cada día
- `round_to_nearest_quarter(price)`: Redondea a cuartos
- `actualizar_excel(df)`: Actualiza hojas por año en Excel

### 2. fase1_calcular_niveles_skew.py

**Propósito:** Calcular todos los niveles con ajuste de Skew

**Funciones principales:**
- `round_to_quarter(value)`: Redondea a 0.25
- `calcular_niveles_skew(df)`: Calcula todos los niveles
- `procesar_archivo()`: Procesa archivo y guarda resultados
- `main()`: Procesa ambos archivos (EM21 y EM9)

---

## ✅ Validaciones Realizadas

1. **Cálculo de Expected Move:**
   - ✅ Fórmula coincide con RyFHEM.cs
   - ✅ Redondeo a cuartos implementado correctamente
   - ✅ Lookback de 21 y 9 días funcionando
   - ✅ Valores válidos para 1,168+ días

2. **Cálculo de Niveles con Skew:**
   - ✅ Fórmulas según calculos.md implementadas
   - ✅ Ajuste de skew aplicado correctamente
   - ✅ Redondeo de niveles Z2/Z3 a 0.25
   - ✅ Niveles Q2 y Q3 derivados correctamente

3. **Archivos generados:**
   - ✅ Excel y CSV creados correctamente
   - ✅ 29 columnas en archivos finales
   - ✅ 221 registros del año 2025
   - ✅ Datos numéricos con formato correcto

---

## 📝 Notas Importantes

1. **Lookback Period:**
   - 21 días ≈ 1 mes de trading (más estable)
   - 9 días ≈ 2 semanas de trading (más reactivo)
   - Ambos períodos disponibles para comparación

2. **Redondeo:**
   - Expected Move: redondeo hacia arriba (ceiling) a cuartos
   - Niveles Z2/Z3: redondeo al 0.25 más cercano (round)

3. **Skew:**
   - Diferencia promedio de 4-6% indica distribución ligeramente asimétrica
   - Skew mayor en EM9 sugiere mayor sensibilidad a movimientos recientes

4. **Archivos de trabajo:**
   - Archivos `*_Niveles.xlsx/csv` son los finales para análisis
   - Contienen todos los niveles calculados y listos para Fase 2

---

## 🎯 Próximos Pasos (Fase 2)

1. **Análisis de Comportamiento de Niveles:**
   - Validar precisión de niveles calculados
   - Analizar tasa de acierto de cada nivel
   - Comparar efectividad EM21 vs EM9

2. **Análisis Estadístico:**
   - Frecuencia de toque de niveles
   - Tiempo promedio hasta alcanzar niveles
   - Reversiones vs continuaciones en niveles

3. **Optimización:**
   - Determinar mejor período de lookback
   - Ajustar multiplicador de skew si necesario
   - Validar fórmulas con datos reales

---

## 📚 Referencias

- **Plan de Backtesting:** `C:\Users\oscar\Documents\Proyecto-Trading\PLAN_BACKTESTING_NASDAQ.md`
- **Fórmula Expected Move:** `C:\Users\oscar\Documents\Proyecto-Trading\Indicadores\RyF\RyFHEM.cs`
- **Metodología Niveles:** `C:\Users\oscar\Documents\Proyecto-Trading\Pruebaniveles\calculos.md`

---

## 🔍 Logs Generados

- `Logs/fase1_agregar_expected_move.log`: Cálculo de Expected Move
- `Logs/fase1_calcular_niveles_skew.log`: Cálculo de niveles con skew

---

**Fin de Documentación - Sesión 2025-12-01**

✅ Fase 1.3 completada exitosamente
