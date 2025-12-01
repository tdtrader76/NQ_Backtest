# 📊 PLAN DE BACKTESTING - FUTUROS NASDAQ
**Sistema de Backtesting en 4 Fases**

---

## 📋 ÍNDICE

1. [Visión General](#visión-general)
2. [Datos y Estructura](#datos-y-estructura)
3. [FASE 1: Preparación y Validación de Datos](#fase-1-preparación-y-validación-de-datos)
4. [FASE 2: Análisis de Comportamiento de Niveles](#fase-2-análisis-de-comportamiento-de-niveles)
5. [FASE 3: Análisis Intradiario Granular](#fase-3-análisis-intradiario-granular)
6. [FASE 4: Por Definir](#fase-4-por-definir)
7. [Stack Tecnológico](#stack-tecnológico)
8. [Estructura de Carpetas](#estructura-de-carpetas)

---

## 🎯 VISIÓN GENERAL

### Objetivo
Desarrollar un sistema robusto de backtesting para validar estrategias de trading basadas en niveles calculados a partir de datos históricos de futuros del NASDAQ.

### Alcance
- **Instrumento:** Futuros NASDAQ (NQ)
- **Periodo:** 5 años históricos
- **Timeframes:** Diario y 1 minuto
- **Metodología:** Análisis basado en niveles calculados

### Criterios de Éxito
- ✅ 100% de datos validados e íntegros
- ✅ Cálculos verificados manualmente en Excel
- ✅ Estadísticas con nivel de confianza ≥95%
- ✅ Sistema reproducible y documentado

---

## 📁 DATOS Y ESTRUCTURA

### Datos de Entrada

#### Datos Diarios
```
Formato: CSV
Columnas: Date, Open, High, Low, Close, Volume
Periodo: 5 años (~1,260 registros)
Ejemplo:
2020-01-02;9150,00;9200,50;9145,25;9195,75;125000
```

#### Datos de 1 Minuto
```
Formato: CSV
Columnas: Date, Time, Open, High, Low, Close, Volume
Periodo: 5 años (~491,400 registros)
Ejemplo:
2020-01-02; 20:01:00; 9150,00; 9200,50; 9145,25; 9195,75; 125000
```

### Archivos de Salida

```
📦 Proyecto-Trading/
├── 📂 C:\Users\oscar\Documents\Proyecto-Trading\Github\NQ_Backtest
│     │   
├     ├── 📂 Originales/
│     │   ├── NQ_Daily_2020-2024.csv
│     │   └── NQ_1min_2020-2024.csv
│     ├── 📂 Procesados/
│     │   ├── NQ_Daily_Limpio.csv
│     │   └── NQ_1min_Limpio.csv
│     └── 📂 Calculados/
│     │   ├── Niveles_Diarios.csv
│     │   ├── Niveles_Diarios.xlsx
│     │   └── Subniveles_Intradiarios.csv
│     └───📂 Resultados/
│     │    ├── 📂 Fase1/
│     │    ├── 📂 Fase2/
│     │    └── 📂 Fase3/ 
│     ├── 📂 Scripts/
│     │    ├── fase1_limpieza.py
│     │    ├── fase1_validacion.py
│     │    ├── fase1_calculos.py
│     │    ├── fase2_analisis_niveles.py
│     │    └── fase3_analisis_intradiario.py
│     │
│     └── 📂 Logs/
           ├── limpieza.log
           ├── validacion.log
           └── errores.log
    
```

---

## 🔷 FASE 1: PREPARACIÓN Y VALIDACIÓN DE DATOS

### Objetivo
Garantizar la integridad, corrección y organización de todos los datos antes de realizar cálculos o análisis.

---

### 📊 TAREA 1.1: Análisis Exploratorio de Datos Diarios

#### Pasos

**1.1.1 Carga Inicial**
```python
import pandas as pd

# Cargar datos
df_daily = pd.read_csv('NQ_Daily_2020-2024.csv')

# Inspección inicial
print(df_daily.info())
print(df_daily.describe())
print(df_daily.head(20))
```

**1.1.2 Validación Estructural**

- ✅ Verificar Precios Open, High, Low, Close, Volume tienen al menos 5 cifras y dos decimales, ejemplo: 20000,25 
     (Los decimales solo pueden ser: ,00 - ,25 - ,50 - ,75)
- ✅ Verificar columnas esperadas
- ✅ Verificar tipos de datos
- ✅ Identificar valores nulos
- ✅ Detectar duplicados

**Checklist de Validación:**
```
□ Columnas: Date, Open, High, Low, Close, Volume
□ Date es tipo datetime
□ OHLCV son tipo float/int
□ No hay valores nulos
□ No hay duplicados de fecha
□ Fechas en orden cronológico
```

**1.1.3 Validación de Lógica de Mercado**
```python
# Crear columna de validación
df_daily['Valid'] = (
    (df_daily['High'] >= df_daily['Low']) &
    (df_daily['High'] >= df_daily['Open']) &
    (df_daily['High'] >= df_daily['Close']) &
    (df_daily['Low'] <= df_daily['Open']) &
    (df_daily['Low'] <= df_daily['Close']) &
    (df_daily['Volume'] > 0)
)

# Identificar registros inválidos
invalid = df_daily[~df_daily['Valid']]
print(f"Registros inválidos: {len(invalid)}")
```

**1.1.4 Detección de Anomalías**
```python
# Calcular returns diarios
df_daily['Returns'] = df_daily['Close'].pct_change()

# Detectar outliers (Z-score > 4)
from scipy import stats
df_daily['Z_Score'] = np.abs(stats.zscore(df_daily['Returns'].dropna()))
outliers = df_daily[df_daily['Z_Score'] > 4]

**Salidas:**
- `Datos/Procesados/Daily_Report.xlsx` (resumen estadístico)
- `Datos/Procesados/Daily_Anomalies.csv` (anomalías detectadas)
- `Logs/fase1_exploracion_daily.log`

---

### 📊 TAREA 1.2: Organización en Excel por Años

#### Objetivo
Crear archivo Excel con hojas separadas por año para validación visual y manual.

#### Implementación

**Script: `crear_excel_anual.py`**
```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows

def crear_excel_anual(df, output_path):
    """
    Crea Excel con hojas por año y validación visual
    """
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    # Añadir columna de año
    df['Year'] = pd.to_datetime(df['Date']).dt.year

    # Crear hoja por cada año
    for year in sorted(df['Year'].unique()):
        df_year = df[df['Year'] == year].copy()

        # Agregar columnas de validación
        df_year['H>=L'] = df_year['High'] >= df_year['Low']
        df_year['Valid_Range'] = (
            (df_year['Open'].between(df_year['Low'], df_year['High'])) &
            (df_year['Close'].between(df_year['Low'], df_year['High']))
        )

        # Escribir en Excel
        df_year.to_excel(writer, sheet_name=str(year), index=False)

        # Obtener worksheet para formateo
        ws = writer.sheets[str(year)]

        # Aplicar formato condicional (resaltar errores en rojo)
        for row in range(2, len(df_year) + 2):
            if not df_year.iloc[row-2]['Valid_Range']:
                for col in range(1, 10):
                    ws.cell(row, col).fill = PatternFill(
                        start_color='FFCCCC',
                        end_color='FFCCCC',
                        fill_type='solid'
                    )

    # Crear hoja resumen
    summary = df.groupby('Year').agg({
        'Close': ['count', 'mean', 'std', 'min', 'max'],
        'Volume': ['sum', 'mean']
    }).round(2)
    summary.to_excel(writer, sheet_name='RESUMEN')

    writer.close()
    print(f"✅ Excel creado: {output_path}")

# Ejecutar
df = pd.read_csv('Datos/Procesados/NQ_Daily_Limpio.csv')
crear_excel_anual(df, 'Resultados/Fase1/Datos_Diarios_por_Año.xlsx')
```

**Estructura del Excel:**

```
📊 Datos_Diarios_por_Año.xlsx
├── 📄 RESUMEN (estadísticas generales)
├── 📄 2020 (252 registros)
├── 📄 2021 (252 registros)
├── 📄 2022 (251 registros)
├── 📄 2023 (251 registros)
└── 📄 2024 (252 registros)
```

**Columnas por año:**
| Date | Open | High | Low | Close | Volume | H>=L | Valid_Range |
|------|------|------|-----|-------|--------|------|-------------|

**Validación Manual:**
- [ ] Revisar registros resaltados en rojo
- [ ] Verificar primeros y últimos registros de cada año
- [ ] Comprobar que no hay gaps inesperados
- [ ] Validar que totales de RESUMEN son coherentes

---

### 🧮 TAREA 1.3: Cálculo de Niveles

#### Pendiente: Definición de Fórmulas

**Placeholder para fórmulas a proporcionar:**

Los niveles se calcularán según las fórmulas específicas que se proporcionen. El sistema está preparado para implementar cualquier tipo de cálculo:

**Ejemplos de niveles comunes (a confirmar):**

- Niveles personalizados
- Expected move

**Estructura Genérica del Script:**

```python
def calcular_niveles(df):
    """
    Calcula niveles según fórmulas proporcionadas

    Args:
        df: DataFrame con OHLCV diario

    Returns:
        DataFrame con columnas adicionales de niveles
    """
    df = df.copy()

    # FÓRMULAS A IMPLEMENTAR AQUÍ
    # Ejemplo de estructura:

    # Nivel Superior
    df['Nivel_R2'] = (df['High'] + df['Low']) / 2 + (df['High'] - df['Low'])
    df['Nivel_R1'] = (df['High'] + df['Low']) / 2 + (df['High'] - df['Low']) * 0.5

    # Nivel Medio
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3

    # Nivel Inferior
    df['Nivel_S1'] = (df['High'] + df['Low']) / 2 - (df['High'] - df['Low']) * 0.5
    df['Nivel_S2'] = (df['High'] + df['Low']) / 2 - (df['High'] - df['Low'])

    return df

# Aplicar cálculos
df_con_niveles = calcular_niveles(df_daily)

# Exportar
df_con_niveles.to_csv('Datos/Calculados/Niveles_Diarios.csv', index=False)
```

**Validación de Cálculos:**

Para asegurar que los cálculos son correctos:

1. **Validación en Excel:**
   - Crear hoja con fórmulas manuales
   - Comparar resultados con Python
   - Verificar en muestra aleatoria de 20 días

2. **Test unitarios:**
```python
def test_niveles():
    # Caso de prueba conocido
    test_data = pd.DataFrame({
        'High': [100],
        'Low': [90],
        'Close': [95]
    })

    result = calcular_niveles(test_data)

    # Verificar resultados esperados
    assert result['Pivot'][0] == 95.0  # Ejemplo
    assert result['Nivel_R1'][0] == 100.0  # Ejemplo
```

**Salidas:**
- `Datos/Calculados/Niveles_Diarios.csv`
- `Datos/Calculados/Niveles_Diarios.xlsx` (con formato visual)
- `Logs/fase1_calculos.log`

---

### 📊 TAREA 1.4: Análisis de Datos de 1 Minuto

#### Objetivo
Validar integridad y formato de datos intradiarios antes de usarlos en Fase 3.

**Consideraciones Especiales:**
- **Volumen:** ~491,400 registros (procesamiento por chunks)
- **Memoria:** Usar tipos de datos eficientes (float32 en lugar de float64)
- **Sesiones:** Identificar horarios de trading (9:30-16:00 ET)

#### Pasos

**1.4.1 Carga Eficiente**
```python
# Cargar por chunks para no saturar memoria
chunks = []
chunk_size = 50000

for chunk in pd.read_csv('NQ_1min_2020-2024.csv', chunksize=chunk_size):
    # Optimizar tipos
    chunk['Date'] = pd.to_datetime(chunk['Date'])
    chunk['Time'] = pd.to_datetime(chunk['Time'], format='%H:%M:%S').dt.time

    for col in ['Open', 'High', 'Low', 'Close']:
        chunk[col] = chunk[col].astype('float32')
    chunk['Volume'] = chunk[col].astype('int32')

    chunks.append(chunk)

df_1min = pd.concat(chunks, ignore_index=True)
```

**1.4.2 Validación de Sesiones**
```python
from datetime import time

# Definir horario de sesión regular
session_start = time(9, 30)
session_end = time(16, 0)

# Identificar registros fuera de sesión
df_1min['In_Session'] = df_1min['Time'].between(session_start, session_end)

# Analizar cobertura
coverage = df_1min.groupby(['Date', 'In_Session']).size().unstack(fill_value=0)
print("Registros por sesión:")
print(coverage)

# Esperado por día de sesión regular: 390 minutos
expected_bars = 390
actual_bars = df_1min[df_1min['In_Session']].groupby('Date').size()
missing_bars = expected_bars - actual_bars
```

**1.4.3 Validación de Continuidad Temporal**
```python
# Verificar que no haya saltos de tiempo mayores a 1 minuto
df_1min['DateTime'] = pd.to_datetime(
    df_1min['Date'].astype(str) + ' ' + df_1min['Time'].astype(str)
)
df_1min = df_1min.sort_values('DateTime')

df_1min['Time_Diff'] = df_1min['DateTime'].diff()

# Identificar gaps > 1 minuto (excluyendo fines de semana)
gaps = df_1min[df_1min['Time_Diff'] > pd.Timedelta(minutes=1)]
gaps_filtered = gaps[gaps['DateTime'].dt.dayofweek < 5]  # Lunes=0, Viernes=4
```

**1.4.4 Resumen Estadístico**
```python
# Crear resumen diario de datos de 1 minuto
daily_summary = df_1min.groupby('Date').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum',
    'DateTime': 'count'  # Número de barras
}).rename(columns={'DateTime': 'Num_Bars'})

# Comparar con datos diarios
comparison = pd.merge(
    df_daily[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']],
    daily_summary,
    on='Date',
    suffixes=('_Daily', '_1min')
)

# Calcular diferencias
comparison['High_Diff'] = abs(comparison['High_Daily'] - comparison['High_1min'])
comparison['Low_Diff'] = abs(comparison['Low_Daily'] - comparison['Low_1min'])

# Días con diferencias significativas (>0.5%)
discrepancies = comparison[
    (comparison['High_Diff'] / comparison['High_Daily'] > 0.005) |
    (comparison['Low_Diff'] / comparison['Low_Daily'] > 0.005)
]
```

**Salidas:**
- `Resultados/Fase1/1min_Validation_Report.xlsx`
- `Resultados/Fase1/1min_Gaps.csv`
- `Resultados/Fase1/1min_vs_Daily_Comparison.csv`
- `Logs/fase1_validacion_1min.log`

---

### ✅ CRITERIOS DE ACEPTACIÓN - FASE 1

**Para pasar a Fase 2, se debe cumplir:**

- [x] 100% de datos diarios validados
- [x] Excel por años creado y revisado manualmente
- [x] Cálculos de niveles implementados y verificados
- [x] Resultados de cálculos exportados en CSV y Excel
- [x] Datos de 1 minuto validados
- [x] Discrepancias documentadas y explicadas
- [x] Todos los logs generados y revisados

**Entregables:**
```
✅ Datos/Procesados/NQ_Daily_Limpio.csv
✅ Datos/Procesados/NQ_1min_Limpio.csv
✅ Datos/Calculados/Niveles_Diarios.csv
✅ Datos/Calculados/Niveles_Diarios.xlsx
✅ Resultados/Fase1/Datos_Diarios_por_Año.xlsx
✅ Resultados/Fase1/Informe_Validacion.pdf
```

---

## 🔶 FASE 2: ANÁLISIS DE COMPORTAMIENTO DE NIVELES

### Objetivo
Analizar estadísticamente cómo el precio del día siguiente (D+1) se comporta respecto a los niveles calculados el día anterior (D).

### Concepto Clave
```
Día D: Calculamos niveles basados en OHLC de ese día
Día D+1: Observamos cómo el precio reacciona a esos niveles
```

---

### 📊 TAREA 2.1: Preparación de Dataset de Análisis

#### Estructura de Datos

**Script: `preparar_dataset_analisis.py`**

```python
def preparar_dataset_analisis(df_niveles):
    """
    Crea dataset con niveles de día D y precios de día D+1
    """
    df = df_niveles.copy()

    # Shift para tener precios del día siguiente
    df['Next_Date'] = df['Date'].shift(-1)
    df['Next_Open'] = df['Open'].shift(-1)
    df['Next_High'] = df['High'].shift(-1)
    df['Next_Low'] = df['Low'].shift(-1)
    df['Next_Close'] = df['Close'].shift(-1)
    df['Next_Volume'] = df['Volume'].shift(-1)

    # Eliminar último registro (no tiene día siguiente)
    df = df[:-1].copy()

    # Verificar que Next_Date es efectivamente el día siguiente
    df['Days_Gap'] = (pd.to_datetime(df['Next_Date']) -
                      pd.to_datetime(df['Date'])).dt.days

    # Alertar si hay gaps > 3 días (fines de semana + festivo)
    large_gaps = df[df['Days_Gap'] > 3]
    if len(large_gaps) > 0:
        print(f"⚠️  {len(large_gaps)} gaps grandes detectados")

    return df

# Ejecutar
df_analisis = preparar_dataset_analisis(df_con_niveles)
df_analisis.to_csv('Datos/Calculados/Dataset_Analisis_Fase2.csv', index=False)
```

**Estructura del Dataset:**
| Date | Open | High | Low | Close | Nivel_R2 | Nivel_R1 | Pivot | Nivel_S1 | Nivel_S2 | Next_Date | Next_Open | Next_High | Next_Low | Next_Close |
|------|------|------|-----|-------|----------|----------|-------|----------|----------|-----------|-----------|-----------|----------|------------|

---

### 📊 TAREA 2.2: Análisis de Respeto a Niveles

#### Definición de Comportamientos

**Clasificación:**
1. **RESPETA**: El rango [Next_Low, Next_High] está completamente dentro del rango de niveles
2. **BREAKOUT ALCISTA**: Next_High supera el nivel superior
3. **BREAKOUT BAJISTA**: Next_Low rompe el nivel inferior
4. **PENETRACIÓN Y RETORNO**: Supera nivel pero cierra dentro del rango

#### Implementación

```python
def analizar_respeto_niveles(df, nivel_superior='Nivel_R1', nivel_inferior='Nivel_S1'):
    """
    Analiza cómo el precio del día siguiente respeta los niveles
    """
    df = df.copy()

    # 1. Clasificar comportamiento
    df['Breakout_Alcista'] = df['Next_High'] > df[nivel_superior]
    df['Breakout_Bajista'] = df['Next_Low'] < df[nivel_inferior]
    df['Respeta_Rango'] = (
        (df['Next_High'] <= df[nivel_superior]) &
        (df['Next_Low'] >= df[nivel_inferior])
    )

    # 2. Calcular excursión si hay breakout
    df['Excursion_Alcista'] = df['Next_High'] - df[nivel_superior]
    df['Excursion_Alcista'] = df['Excursion_Alcista'].where(df['Breakout_Alcista'], 0)

    df['Excursion_Bajista'] = df[nivel_inferior] - df['Next_Low']
    df['Excursion_Bajista'] = df['Excursion_Bajista'].where(df['Breakout_Bajista'], 0)

    # 3. Detectar retornos
    df['Retorno_Alcista'] = (
        df['Breakout_Alcista'] &
        (df['Next_Close'] <= df[nivel_superior])
    )

    df['Retorno_Bajista'] = (
        df['Breakout_Bajista'] &
        (df['Next_Close'] >= df[nivel_inferior])
    )

    # 4. Calcular penetración como % del rango
    rango_niveles = df[nivel_superior] - df[nivel_inferior]
    df['Penetracion_Alcista_Pct'] = (df['Excursion_Alcista'] / rango_niveles * 100)
    df['Penetracion_Bajista_Pct'] = (df['Excursion_Bajista'] / rango_niveles * 100)

    return df
```

---

### 📊 TAREA 2.3: Estadísticas y Métricas

#### Estadísticas Generales

```python
def calcular_estadisticas_respeto(df):
    """
    Genera estadísticas completas de respeto a niveles
    """
    total_dias = len(df)

    stats = {
        'Total_Dias': total_dias,
        'Dias_Respeta': df['Respeta_Rango'].sum(),
        'Dias_Breakout_Alcista': df['Breakout_Alcista'].sum(),
        'Dias_Breakout_Bajista': df['Breakout_Bajista'].sum(),
        'Pct_Respeta': df['Respeta_Rango'].sum() / total_dias * 100,
        'Pct_Breakout_Alcista': df['Breakout_Alcista'].sum() / total_dias * 100,
        'Pct_Breakout_Bajista': df['Breakout_Bajista'].sum() / total_dias * 100,
        'Tasa_Retorno_Alcista': (
            df['Retorno_Alcista'].sum() / df['Breakout_Alcista'].sum() * 100
            if df['Breakout_Alcista'].sum() > 0 else 0
        ),
        'Tasa_Retorno_Bajista': (
            df['Retorno_Bajista'].sum() / df['Breakout_Bajista'].sum() * 100
            if df['Breakout_Bajista'].sum() > 0 else 0
        ),
    }

    return pd.Series(stats)
```

#### Análisis de Excursiones

```python
def analizar_excursiones(df):
    """
    Análisis detallado de excursiones fuera de niveles
    """
    breakouts_alcistas = df[df['Breakout_Alcista']]
    breakouts_bajistas = df[df['Breakout_Bajista']]

    stats_alcista = {
        'Excursion_Media': breakouts_alcistas['Excursion_Alcista'].mean(),
        'Excursion_Mediana': breakouts_alcistas['Excursion_Alcista'].median(),
        'Excursion_StdDev': breakouts_alcistas['Excursion_Alcista'].std(),
        'Excursion_Max': breakouts_alcistas['Excursion_Alcista'].max(),
        'Penetracion_Media_Pct': breakouts_alcistas['Penetracion_Alcista_Pct'].mean(),
    }

    stats_bajista = {
        'Excursion_Media': breakouts_bajistas['Excursion_Bajista'].mean(),
        'Excursion_Mediana': breakouts_bajistas['Excursion_Bajista'].median(),
        'Excursion_StdDev': breakouts_bajistas['Excursion_Bajista'].std(),
        'Excursion_Max': breakouts_bajistas['Excursion_Bajista'].max(),
        'Penetracion_Media_Pct': breakouts_bajistas['Penetracion_Bajista_Pct'].mean(),
    }

    return {
        'Alcista': pd.Series(stats_alcista),
        'Bajista': pd.Series(stats_bajista)
    }
```

---

### 📊 TAREA 2.4: Análisis por Contexto

#### Segmentación por Volatilidad

```python
def analizar_por_volatilidad(df):
    """
    Segmenta análisis según régimen de volatilidad
    """
    # Calcular ATR 14 días
    df['TR'] = df[['High', 'Low', 'Close']].apply(
        lambda x: max(
            x['High'] - x['Low'],
            abs(x['High'] - df['Close'].shift(1)),
            abs(x['Low'] - df['Close'].shift(1))
        ),
        axis=1
    )
    df['ATR_14'] = df['TR'].rolling(14).mean()

    # Clasificar en terciles
    df['Volatilidad'] = pd.qcut(
        df['ATR_14'],
        q=3,
        labels=['Baja', 'Media', 'Alta']
    )

    # Analizar por régimen
    resultados = []
    for vol in ['Baja', 'Media', 'Alta']:
        df_vol = df[df['Volatilidad'] == vol]
        stats = calcular_estadisticas_respeto(df_vol)
        stats['Volatilidad'] = vol
        resultados.append(stats)

    return pd.DataFrame(resultados)
```

---

### ✅ CRITERIOS DE ACEPTACIÓN - FASE 2

- [ ] Dataset de análisis creado
- [ ] Estadísticas de respeto calculadas
- [ ] Análisis de excursiones completado
- [ ] Análisis por contexto realizado
- [ ] Dashboard Excel generado
- [ ] Insights documentados

**Entregables:**
```
✅ Datos/Calculados/Dataset_Analisis_Fase2.csv
✅ Resultados/Fase2/Dashboard_Analisis_Niveles.xlsx
✅ Resultados/Fase2/Distribucion_Excursiones.png
✅ Logs/fase2_analisis.log
```

---

## 🔷 FASE 3: ANÁLISIS INTRADIARIO GRANULAR

### Objetivo
Calcular subniveles dentro de los rangos diarios y analizar la reacción del precio en datos de 1 minuto.

---

### 📊 TAREA 3.1: Cálculo de Subniveles

#### División Equidistante

```python
def calcular_subniveles_equidistantes(df, num_subniveles=4):
    """
    Divide cada segmento entre niveles en subniveles equidistantes
    """
    df = df.copy()

    segmentos = [
        ('Nivel_R2', 'Nivel_R1', 'Sub_R2_R1'),
        ('Nivel_R1', 'Pivot', 'Sub_R1_P'),
        ('Pivot', 'Nivel_S1', 'Sub_P_S1'),
        ('Nivel_S1', 'Nivel_S2', 'Sub_S1_S2'),
    ]

    for nivel_superior, nivel_inferior, prefijo in segmentos:
        rango = df[nivel_superior] - df[nivel_inferior]
        paso = rango / (num_subniveles + 1)

        for i in range(1, num_subniveles + 1):
            df[f'{prefijo}_{i}'] = df[nivel_inferior] + (paso * i)

    return df
```

---

### 📊 TAREA 3.2: Detección de Reacciones

#### Definición de Reacción

Una reacción es significativa si:
1. **Toque**: Precio llega al subnivel (± tolerancia)
2. **Rechazo**: Precio rebota ≥ X puntos
3. **Consolidación**: Permanece cerca ≥ Y minutos

```python
def detectar_reacciones(df_1min, niveles_dia, tolerancia_puntos=2,
                       rechazo_minimo=10, tiempo_consolidacion=5):
    """
    Detecta reacciones a subniveles en datos de 1 minuto
    """
    reacciones = []

    # Obtener subniveles
    cols_subniveles = [col for col in niveles_dia.index
                       if 'Sub_' in col or 'Fib_' in col]

    for subnivel_col in cols_subniveles:
        nivel_precio = niveles_dia[subnivel_col]

        # Buscar toques
        df_1min['Distancia'] = df_1min.apply(
            lambda x: min(
                abs(x['High'] - nivel_precio),
                abs(x['Low'] - nivel_precio)
            ),
            axis=1
        )

        toques = df_1min[df_1min['Distancia'] <= tolerancia_puntos]

        for idx, toque in toques.iterrows():
            # Analizar rechazo en siguientes barras
            # (implementación completa en scripts)
            pass

    return pd.DataFrame(reacciones)
```

---

### 📊 TAREA 3.3: Análisis Estadístico

```python
def analizar_efectividad_subniveles(df_reacciones):
    """
    Evalúa qué subniveles generan más reacciones
    """
    stats = df_reacciones.groupby('Subnivel').agg({
        'Reaccion_Significativa': ['sum', 'count', 'mean'],
        'Magnitud_Rechazo': ['mean', 'median', 'std'],
        'Tiempo_Consolidacion': ['mean', 'median']
    })

    return stats.sort_values(('Reaccion_Significativa', 'mean'), ascending=False)
```

---

### ✅ CRITERIOS DE ACEPTACIÓN - FASE 3

- [ ] Subniveles calculados
- [ ] Detección de reacciones implementada
- [ ] Estadísticas de efectividad completadas
- [ ] Zonas clave identificadas

**Entregables:**
```
✅ Datos/Calculados/Subniveles_Intradiarios.csv
✅ Resultados/Fase3/Reacciones_Subniveles.csv
✅ Resultados/Fase3/Efectividad_Subniveles.xlsx
✅ Resultados/Fase3/Heatmap_Reacciones.png
```

---

## 🔸 FASE 4: BACKTESTING DE ESTRATEGIA COMPLETA

### Objetivo
Implementar y evaluar estrategias de trading basadas en los insights de las fases anteriores.

---

### 📊 COMPONENTES CLAVE

#### 1. Definición de Estrategia

**Ejemplo: Estrategia de Rebote en Niveles**

```python
class EstrategiaReboteNiveles:
    """
    Estrategia que opera rebotes en niveles de soporte/resistencia
    """

    def __init__(self, nivel_entrada, stop_loss_pts, take_profit_pts):
        self.nivel_entrada = nivel_entrada
        self.stop_loss = stop_loss_pts
        self.take_profit = take_profit_pts
        self.posicion = None

    def evaluar_entrada(self, precio_actual, nivel):
        """
        Lógica de entrada basada en aproximación al nivel
        """
        if abs(precio_actual - nivel) <= 5:  # Dentro de 5 puntos
            return True
        return False

    def evaluar_salida(self, precio_actual, precio_entrada):
        """
        Lógica de salida por TP o SL
        """
        ganancia = precio_actual - precio_entrada

        if ganancia >= self.take_profit:
            return 'TAKE_PROFIT'
        elif ganancia <= -self.stop_loss:
            return 'STOP_LOSS'

        return None
```

#### 2. Motor de Backtesting

```python
class BacktestEngine:
    """
    Motor principal de backtesting
    """

    def __init__(self, df_1min, df_niveles, estrategia, capital_inicial=100000):
        self.df_1min = df_1min
        self.df_niveles = df_niveles
        self.estrategia = estrategia
        self.capital = capital_inicial
        self.trades = []

    def ejecutar_backtest(self):
        """
        Ejecuta backtest completo
        """
        for fecha in self.df_niveles['Date'].unique():
            # Obtener niveles del día
            niveles_dia = self.df_niveles[
                self.df_niveles['Date'] == fecha
            ].iloc[0]

            # Obtener datos intradiarios
            df_dia = self.df_1min[self.df_1min['Date'] == fecha]

            # Simular trading del día
            self._simular_dia(df_dia, niveles_dia)

        return self._generar_reporte()

    def _simular_dia(self, df_dia, niveles_dia):
        """
        Simula operativa de un día
        """
        posicion_abierta = False

        for idx, bar in df_dia.iterrows():
            # Lógica de entrada si no hay posición
            if not posicion_abierta:
                # Verificar señal de entrada
                pass

            # Lógica de salida si hay posición
            else:
                # Verificar condiciones de salida
                pass

    def _generar_reporte(self):
        """
        Genera métricas de performance
        """
        df_trades = pd.DataFrame(self.trades)

        metricas = {
            'Total_Trades': len(df_trades),
            'Trades_Ganadores': len(df_trades[df_trades['PnL'] > 0]),
            'Trades_Perdedores': len(df_trades[df_trades['PnL'] < 0]),
            'Win_Rate': len(df_trades[df_trades['PnL'] > 0]) / len(df_trades) * 100,
            'PnL_Total': df_trades['PnL'].sum(),
            'PnL_Medio': df_trades['PnL'].mean(),
            'Mejor_Trade': df_trades['PnL'].max(),
            'Peor_Trade': df_trades['PnL'].min(),
            'Profit_Factor': (
                df_trades[df_trades['PnL'] > 0]['PnL'].sum() /
                abs(df_trades[df_trades['PnL'] < 0]['PnL'].sum())
            ),
            'Drawdown_Maximo': self._calcular_max_drawdown(df_trades),
            'Sharpe_Ratio': self._calcular_sharpe(df_trades),
        }

        return metricas
```

#### 3. Métricas de Performance

```python
def analizar_performance(df_trades):
    """
    Análisis completo de performance de la estrategia
    """

    # Métricas básicas
    total_trades = len(df_trades)
    ganadores = df_trades[df_trades['PnL'] > 0]
    perdedores = df_trades[df_trades['PnL'] < 0]

    # Win Rate
    win_rate = len(ganadores) / total_trades * 100

    # Expectancy (expectativa matemática)
    avg_win = ganadores['PnL'].mean()
    avg_loss = abs(perdedores['PnL'].mean())
    expectancy = (win_rate/100 * avg_win) - ((1-win_rate/100) * avg_loss)

    # Profit Factor
    gross_profit = ganadores['PnL'].sum()
    gross_loss = abs(perdedores['PnL'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

    # R-Múltiplo promedio
    df_trades['R_Multiple'] = df_trades['PnL'] / df_trades['Risk']
    avg_r_multiple = df_trades['R_Multiple'].mean()

    # Máximo drawdown
    df_trades['Capital_Acum'] = df_trades['PnL'].cumsum()
    df_trades['Peak'] = df_trades['Capital_Acum'].cummax()
    df_trades['Drawdown'] = df_trades['Peak'] - df_trades['Capital_Acum']
    max_drawdown = df_trades['Drawdown'].max()

    # Sharpe Ratio (anualizado)
    returns = df_trades['PnL'] / 100000  # Asumiendo capital base
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252)

    # Consecutive wins/losses
    df_trades['Win'] = df_trades['PnL'] > 0
    df_trades['Streak'] = df_trades['Win'].ne(df_trades['Win'].shift()).cumsum()
    streaks = df_trades.groupby('Streak')['Win'].agg(['first', 'count'])
    max_consecutive_wins = streaks[streaks['first']]['count'].max()
    max_consecutive_losses = streaks[~streaks['first']]['count'].max()

    metricas = {
        'Total_Trades': total_trades,
        'Win_Rate': win_rate,
        'Avg_Win': avg_win,
        'Avg_Loss': avg_loss,
        'Expectancy': expectancy,
        'Profit_Factor': profit_factor,
        'Avg_R_Multiple': avg_r_multiple,
        'Max_Drawdown': max_drawdown,
        'Sharpe_Ratio': sharpe,
        'Max_Consecutive_Wins': max_consecutive_wins,
        'Max_Consecutive_Losses': max_consecutive_losses,
    }

    return pd.Series(metricas)
```

#### 4. Optimización de Parámetros

```python
from itertools import product

def optimizar_parametros(df_1min, df_niveles, param_grid):
    """
    Grid search para optimizar parámetros de estrategia

    Args:
        param_grid: Dict con rangos de parámetros
        {
            'stop_loss': [10, 15, 20, 25],
            'take_profit': [20, 30, 40, 50],
            'tolerancia_entrada': [2, 3, 5]
        }
    """
    resultados = []

    # Generar todas las combinaciones
    keys = param_grid.keys()
    values = param_grid.values()

    for combination in product(*values):
        params = dict(zip(keys, combination))

        # Ejecutar backtest con estos parámetros
        estrategia = EstrategiaReboteNiveles(**params)
        engine = BacktestEngine(df_1min, df_niveles, estrategia)
        metricas = engine.ejecutar_backtest()

        # Guardar resultados
        resultado = {**params, **metricas}
        resultados.append(resultado)

    df_resultados = pd.DataFrame(resultados)

    # Ordenar por métrica objetivo (ej: Sharpe Ratio)
    df_resultados = df_resultados.sort_values('Sharpe_Ratio', ascending=False)

    return df_resultados
```

#### 5. Walk-Forward Analysis

```python
def walk_forward_analysis(df_1min, df_niveles, ventana_train=252, ventana_test=63):
    """
    Análisis walk-forward para evitar overfitting

    Args:
        ventana_train: Días para entrenar (1 año)
        ventana_test: Días para testear (3 meses)
    """
    resultados_wf = []

    fechas_unicas = sorted(df_niveles['Date'].unique())

    inicio_test = ventana_train

    while inicio_test + ventana_test <= len(fechas_unicas):
        # Período de entrenamiento
        fechas_train = fechas_unicas[inicio_test-ventana_train:inicio_test]

        # Período de test
        fechas_test = fechas_unicas[inicio_test:inicio_test+ventana_test]

        # Optimizar en training set
        df_train = df_niveles[df_niveles['Date'].isin(fechas_train)]
        mejores_params = optimizar_parametros(
            df_1min[df_1min['Date'].isin(fechas_train)],
            df_train,
            param_grid={'stop_loss': [10, 15, 20], 'take_profit': [20, 30, 40]}
        ).iloc[0]

        # Evaluar en test set
        df_test = df_niveles[df_niveles['Date'].isin(fechas_test)]
        estrategia = EstrategiaReboteNiveles(
            stop_loss_pts=mejores_params['stop_loss'],
            take_profit_pts=mejores_params['take_profit']
        )
        engine = BacktestEngine(
            df_1min[df_1min['Date'].isin(fechas_test)],
            df_test,
            estrategia
        )
        metricas_test = engine.ejecutar_backtest()

        resultados_wf.append({
            'Periodo_Test': f"{fechas_test[0]} - {fechas_test[-1]}",
            **metricas_test
        })

        # Avanzar ventana
        inicio_test += ventana_test

    return pd.DataFrame(resultados_wf)
```

---

### 📊 TAREA 4.1: Implementación de Estrategia Base

**Pasos:**
1. Definir reglas de entrada y salida
2. Implementar gestión de riesgo
3. Codificar lógica en motor de backtest
4. Ejecutar backtest completo
5. Analizar resultados

---

### 📊 TAREA 4.2: Optimización

**Pasos:**
1. Definir espacio de parámetros
2. Ejecutar grid search
3. Analizar superficie de optimización
4. Seleccionar parámetros óptimos
5. Validar con walk-forward

---

### 📊 TAREA 4.3: Análisis de Robustez

```python
def analisis_robustez(df_resultados_optimizacion):
    """
    Analiza qué tan robustos son los parámetros óptimos
    """

    # Identificar "meseta" de buenos resultados
    top_10_pct = df_resultados_optimizacion.nlargest(
        int(len(df_resultados_optimizacion) * 0.1),
        'Sharpe_Ratio'
    )

    # Analizar variabilidad de parámetros en top 10%
    param_variability = {
        'stop_loss': {
            'mean': top_10_pct['stop_loss'].mean(),
            'std': top_10_pct['stop_loss'].std(),
            'range': top_10_pct['stop_loss'].max() - top_10_pct['stop_loss'].min()
        },
        'take_profit': {
            'mean': top_10_pct['take_profit'].mean(),
            'std': top_10_pct['take_profit'].std(),
            'range': top_10_pct['take_profit'].max() - top_10_pct['take_profit'].min()
        }
    }

    # Baja variabilidad = Parámetros robustos
    # Alta variabilidad = Posible overfitting

    return param_variability
```

---

### ✅ CRITERIOS DE ACEPTACIÓN - FASE 4

- [ ] Estrategia base implementada
- [ ] Backtest completo ejecutado
- [ ] Métricas de performance calculadas
- [ ] Optimización de parámetros realizada
- [ ] Walk-forward analysis completado
- [ ] Análisis de robustez documentado
- [ ] Dashboard final creado

**Entregables:**
```
✅ Scripts/estrategia_base.py
✅ Resultados/Fase4/Backtest_Completo.xlsx
✅ Resultados/Fase4/Optimizacion_Parametros.csv
✅ Resultados/Fase4/Walk_Forward_Results.xlsx
✅ Resultados/Fase4/Equity_Curve.png
✅ Resultados/Fase4/Informe_Final.pdf
```

---

## 🛠️ STACK TECNOLÓGICO

### Lenguajes y Frameworks

```yaml
Python: 3.9+
  Librerías Core:
    - pandas: Manipulación de datos
    - numpy: Cálculos numéricos
    - scipy: Estadística avanzada

  Visualización:
    - matplotlib: Gráficos
    - seaborn: Gráficos estadísticos
    - plotly: Gráficos interactivos

  Machine Learning (opcional):
    - scikit-learn: Clustering, clasificación
    - statsmodels: Tests estadísticos

  Excel:
    - openpyxl: Lectura/escritura Excel
    - xlsxwriter: Formateo avanzado
```

### Estructura de Scripts

```
Scripts/
├── utils/
│   ├── data_loader.py          # Carga de datos
│   ├── data_validator.py       # Validaciones
│   ├── nivel_calculator.py     # Cálculo de niveles
│   └── export_utils.py         # Exportación
├── fase1_pipeline.py           # Pipeline completo Fase 1
├── fase2_analisis.py           # Análisis Fase 2
├── fase3_subniveles.py         # Subniveles Fase 3
├── fase4_backtest.py           # Backtesting Fase 4
└── main.py                     # Orquestador principal
```

---

## 📝 MEJORES PRÁCTICAS

### 1. Versionado de Datos

```python
from datetime import datetime

def guardar_con_version(df, nombre_base):
    """
    Guarda archivo con timestamp para trazabilidad
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{nombre_base}_{timestamp}.csv"
    df.to_csv(filename, index=False)

    # Guardar también versión "latest"
    df.to_csv(f"{nombre_base}_latest.csv", index=False)

    return filename
```

### 2. Logging Completo

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/backtesting.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usar en código
logger.info("Iniciando cálculo de niveles")
logger.warning(f"Detectados {n} outliers")
logger.error("Error en validación de datos")
```

### 3. Tests Unitarios

```python
import unittest

class TestNivelCalculator(unittest.TestCase):

    def setUp(self):
        self.test_data = pd.DataFrame({
            'High': [100, 110, 105],
            'Low': [90, 95, 92],
            'Close': [95, 105, 100]
        })

    def test_pivot_calculation(self):
        result = calcular_niveles(self.test_data)
        expected_pivot = (100 + 90 + 95) / 3
        self.assertAlmostEqual(result['Pivot'][0], expected_pivot)
```

---

## 🎯 ROADMAP DE EJECUCIÓN

### Semana 1-2: FASE 1
- [ ] Configurar entorno Python
- [ ] Cargar y validar datos diarios
- [ ] Crear Excel por años
- [ ] Implementar cálculos de niveles
- [ ] Validar datos de 1 minuto

### Semana 3-4: FASE 2
- [ ] Preparar dataset de análisis
- [ ] Calcular estadísticas de respeto
- [ ] Analizar excursiones
- [ ] Análisis por contexto
- [ ] Generar dashboard

### Semana 5-6: FASE 3
- [ ] Calcular subniveles
- [ ] Implementar detección de reacciones
- [ ] Análisis estadístico
- [ ] Identificar zonas clave

### Semana 7-8: FASE 4
- [ ] Implementar motor de backtest
- [ ] Definir estrategia base
- [ ] Ejecutar backtest
- [ ] Optimizar parámetros
- [ ] Walk-forward analysis
- [ ] Informe final

---

## 📊 MÉTRICAS DE ÉXITO GLOBAL

### Calidad de Datos
- ✅ 0 errores de validación
- ✅ 100% cobertura temporal
- ✅ Discrepancias < 0.1%

### Insights Estadísticos
- ✅ Intervalo de confianza ≥ 95%
- ✅ N > 1000 observaciones
- ✅ Resultados replicables

### Performance de Estrategia
- 🎯 Sharpe Ratio > 1.5
- 🎯 Win Rate > 50%
- 🎯 Profit Factor > 1.5
- 🎯 Max Drawdown < 20%

---

## 📚 RECURSOS ADICIONALES

### Libros Recomendados
- "Advances in Financial Machine Learning" - Marcos López de Prado
- "Evidence-Based Technical Analysis" - David Aronson
- "Quantitative Trading" - Ernest Chan

### Papers Académicos
- "The Profitability of Technical Analysis: A Review" (Park & Irwin, 2007)
- "Support and Resistance Levels" (Osler, 2000)

---

**Documento creado:** 2025-01-25
**Versión:** 1.0
**Autor:** Sistema de Backtesting NASDAQ

