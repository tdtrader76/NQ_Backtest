# Guía Técnica: Procesamiento de Datos de Minutos

## Sistema de Backtesting NQ - Documentación Técnica

---

## 📑 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Formato de Datos](#formato-de-datos)
4. [Scripts Implementados](#scripts-implementados)
5. [Flujo de Procesamiento](#flujo-de-procesamiento)
6. [Validaciones](#validaciones)
7. [Manejo de Errores](#manejo-de-errores)
8. [Optimización y Performance](#optimización-y-performance)
9. [Troubleshooting](#troubleshooting)
10. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Introducción

### Propósito

Este documento describe el sistema de procesamiento de datos intradiarios (minuto a minuto) para el proyecto de backtesting de futuros del NASDAQ (NQ).

### Alcance

- Consolidación de 20+ archivos de contratos trimestrales
- Validación de 1.6M+ registros de datos de minutos
- División por años para optimizar el manejo
- Preparación para análisis de Fase 3

### Tecnologías Utilizadas

- **Python 3.9+**
- **pandas**: Manipulación de datos
- **pathlib**: Manejo de rutas
- **logging**: Sistema de logs
- **datetime**: Manejo de timestamps

---

## Arquitectura del Sistema

### Estructura de Carpetas

```
NQ_Backtest/
├── datos brutos/
│   └── datos ninjatrader/
│       └── Minutos/          # Archivos .txt originales
│           ├── NQ 03-21.Last.txt
│           ├── NQ 06-21.Last.txt
│           └── ... (20 archivos)
├── Scripts/
│   ├── consolidar_datos_minutos.py
│   └── dividir_datos_minutos_por_anio.py
├── Procesados/
│   ├── 2020/
│   │   └── NQ_1min_2020.csv
│   ├── 2021/
│   │   └── NQ_1min_2021.csv
│   └── ... (hasta 2025)
│   └── NQ_1min_2020-2025_Limpio.csv
├── Originales/
│   └── NQ_1min_2020-2025.csv
└── Logs/
    ├── consolidacion_minutos.log
    └── dividir_datos_minutos_por_anio.log
```

### Flujo de Datos

```
[Archivos .txt]
     ↓
[consolidar_datos_minutos.py]
     ↓
[Validación + Limpieza]
     ↓
[NQ_1min_2020-2025_Limpio.csv]
     ↓
[dividir_datos_minutos_por_anio.py]
     ↓
[Archivos por año 2020-2025]
```

---

## Formato de Datos

### Formato de Entrada (NinjaTrader .txt)

**Sin headers, separador: `;`**

```
YYYYMMDD HHMMSS;Open;High;Low;Close;Volume
20201215 230100;12604;12608.5;12601.75;12607;214
20201215 230200;12607.5;12609.5;12602.5;12605.75;166
```

**Características:**
- Fecha y hora en un solo campo
- Formato: `YYYYMMDD HHMMSS` (sin separadores)
- Precios: decimales con punto
- Volumen: número entero
- Sin quotes en campos de texto

### Formato de Salida (CSV)

**Con headers, separador: `,`**

```csv
DateTime,Open,High,Low,Close,Volume
2020-12-15 23:01:00,12604.0,12608.5,12601.75,12607.0,214
2020-12-15 23:02:00,12607.5,12609.5,12602.5,12605.75,166
```

**Características:**
- DateTime en formato ISO: `YYYY-MM-DD HH:MM:SS`
- Precios: float con precisión de 2 decimales
- Volumen: entero
- Headers incluidos

---

## Scripts Implementados

### 1. consolidar_datos_minutos.py

#### Propósito
Consolidar todos los archivos .txt de contratos trimestrales en un único CSV validado.

#### Funciones Principales

##### `cargar_archivo_minutos(filepath)`

**Entrada:** Path al archivo .txt
**Salida:** DataFrame con datos del archivo

```python
def cargar_archivo_minutos(filepath):
    """
    Carga un archivo de datos de minutos de NinjaTrader

    Args:
        filepath (Path): Ruta al archivo .txt

    Returns:
        DataFrame: Datos cargados con columnas [DateTime, Open, High, Low, Close, Volume]
        None: Si hay error en la carga
    """
```

**Proceso:**
1. Lee CSV con `pandas.read_csv(sep=';', header=None)`
2. Convierte timestamp con `pd.to_datetime(format='%Y%m%d %H%M%S')`
3. Maneja errores con `errors='coerce'`
4. Elimina timestamps inválidos (NaT)
5. Reordena columnas
6. Registra estadísticas en log

##### `consolidar_datos_minutos()`

**Entrada:** Ninguna (lee de carpeta configurada)
**Salida:** DataFrame consolidado

```python
def consolidar_datos_minutos():
    """
    Consolida todos los archivos de minutos en un solo DataFrame

    Returns:
        DataFrame: Datos consolidados y ordenados cronológicamente
        None: Si no se cargaron datos
    """
```

**Proceso:**
1. Busca archivos .txt con `glob("*.txt")`
2. Carga cada archivo con `cargar_archivo_minutos()`
3. Concatena con `pd.concat(ignore_index=True)`
4. Ordena por DateTime con `sort_values('DateTime')`
5. Elimina duplicados con `drop_duplicates(subset=['DateTime'], keep='first')`
6. Registra estadísticas

**Estrategia de Duplicados:**
- `keep='first'`: Prioriza registros de contratos más antiguos
- Justificación: Mayor liquidez en contrato previo al rollover

##### `validar_datos(df)`

**Entrada:** DataFrame con datos
**Salida:** DataFrame con columna 'Valid' añadida

```python
def validar_datos(df):
    """
    Valida que los datos cumplan con las reglas de mercado

    Args:
        df (DataFrame): Datos a validar

    Returns:
        DataFrame: Mismo DataFrame con columna 'Valid' (bool)
    """
```

**Validaciones Aplicadas:**

| Validación | Expresión | Descripción |
|------------|-----------|-------------|
| High >= Low | `df['High'] >= df['Low']` | Máximo debe ser mayor o igual que mínimo |
| High >= Open | `df['High'] >= df['Open']` | Máximo debe incluir apertura |
| High >= Close | `df['High'] >= df['Close']` | Máximo debe incluir cierre |
| Low <= Open | `df['Low'] <= df['Open']` | Mínimo debe incluir apertura |
| Low <= Close | `df['Low'] <= df['Close']` | Mínimo debe incluir cierre |
| Volume > 0 | `df['Volume'] > 0` | Volumen positivo |
| Precios > 0 | `df['Open/High/Low/Close'] > 0` | Todos los precios positivos |
| Timestamps cronológicos | `df['DateTime'].diff() >= 0` | No retrocesos en el tiempo |

##### `detectar_gaps(df, reportar_log=True)`

**Entrada:** DataFrame ordenado, flag de reporte
**Salida:** DataFrame con gaps detectados (o None)

```python
def detectar_gaps(df, reportar_log=True):
    """
    Detecta gaps temporales significativos en los datos

    Args:
        df (DataFrame): Datos ordenados por DateTime
        reportar_log (bool): Si True, escribe gaps en el log

    Returns:
        DataFrame: Gaps detectados con clasificación
        None: Si no hay gaps
    """
```

**Clasificación de Gaps:**

| Tipo | Duración | Descripción | Ejemplo |
|------|----------|-------------|---------|
| Normal | ≤ 5 minutos | No se reporta | Actividad regular |
| Cierre diario | 5-120 minutos | Normal | 17:00-18:00 ET |
| Fin de semana | 120-4320 min (72h) | Normal | Viernes-Lunes |
| Gap largo | > 4320 minutos | Requiere investigación | Festivos, eventos |

##### `exportar_datos(df, filename)`

**Entrada:** DataFrame validado, nombre base
**Salida:** Archivos CSV generados

```python
def exportar_datos(df, filename):
    """
    Exporta datos a archivos CSV (original y limpio)

    Args:
        df (DataFrame): Datos a exportar
        filename (str): Nombre base del archivo (sin extensión)

    Returns:
        DataFrame: Datos limpios (solo válidos)
    """
```

**Archivos Generados:**
1. **Original**: `Originales/{filename}.csv`
   - Incluye columna 'Valid'
   - Para auditoría

2. **Limpio**: `Procesados/{filename}_Limpio.csv`
   - Solo registros válidos
   - Sin columna 'Valid'
   - Para análisis

**Estadísticas Reportadas:**
- Total de registros
- Registros válidos/inválidos
- Rango temporal (inicio/fin)
- Duración en días
- Cobertura temporal (%)
- Rangos de precios (min/max/promedio)
- Volumen total

##### `main()`

**Orquestador Principal**

```python
def main():
    """
    Función principal - Orquesta el flujo completo

    Pasos:
        1. Consolidar archivos
        2. Validar datos
        3. Detectar gaps
        4. Exportar datos
    """
```

**Flujo de Ejecución:**
```
[PASO 1/4: Consolidar archivos]
     ↓
[PASO 2/4: Validar datos]
     ↓
[PASO 3/4: Detectar gaps]
     ↓
[PASO 4/4: Exportar datos]
     ↓
[✅ CONSOLIDACIÓN COMPLETADA]
```

---

### 2. dividir_datos_minutos_por_anio.py

#### Propósito
Dividir el archivo consolidado en archivos más manejables organizados por año.

#### Funciones Principales

##### `cargar_datos_consolidados()`

```python
def cargar_datos_consolidados():
    """
    Carga el archivo consolidado de datos de minutos

    Returns:
        DataFrame: Datos consolidados con DateTime parseado
        None: Si hay error
    """
```

**Proceso:**
1. Lee CSV con `parse_dates=['DateTime']`
2. Valida carga exitosa
3. Muestra rango temporal
4. Retorna DataFrame

##### `dividir_por_anios(df)`

```python
def dividir_por_anios(df):
    """
    Divide el DataFrame por años y guarda cada año separado

    Args:
        df (DataFrame): Datos consolidados

    Side effects:
        - Crea carpetas por año
        - Genera archivos CSV individuales
        - Registra estadísticas en log
    """
```

**Proceso:**
1. Extrae año: `df['Year'] = df['DateTime'].dt.year`
2. Obtiene años únicos
3. Para cada año:
   - Filtra datos del año
   - Elimina columna 'Year'
   - Crea carpeta si no existe
   - Exporta a CSV
   - Calcula estadísticas
   - Registra en log

##### `generar_resumen(df)`

```python
def generar_resumen(df):
    """
    Genera un resumen estadístico de la división por años

    Args:
        df (DataFrame): Datos consolidados

    Side effects:
        - Registra tabla de estadísticas en log
        - Muestra distribución porcentual
    """
```

**Estadísticas Generadas:**
- Count, min, max por año
- Close: mean, min, max
- Volume: sum
- Porcentaje de registros por año

---

## Flujo de Procesamiento

### Flujo Completo

```
┌─────────────────────────────────────┐
│  1. CARGA DE ARCHIVOS               │
│  - Glob 20 archivos .txt            │
│  - Conversión timestamp             │
│  - Validación inicial               │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  2. CONSOLIDACIÓN                   │
│  - Concatenar DataFrames            │
│  - Ordenar cronológicamente         │
│  - Eliminar duplicados              │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  3. VALIDACIÓN                      │
│  - Reglas de mercado (OHLCV)        │
│  - Timestamps cronológicos          │
│  - Marcar registros inválidos       │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  4. DETECCIÓN DE GAPS               │
│  - Calcular diferencias temporales  │
│  - Clasificar gaps                  │
│  - Reportar top 10                  │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  5. EXPORTACIÓN                     │
│  - Archivo original (con Valid)     │
│  - Archivo limpio (solo válidos)    │
│  - Estadísticas completas           │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  6. DIVISIÓN POR AÑOS               │
│  - Extraer año del DateTime         │
│  - Crear carpetas                   │
│  - Exportar archivos individuales   │
└─────────────────────────────────────┘
```

---

## Validaciones

### Validaciones de Datos de Mercado

#### Precios OHLC

```python
# Validación High-Low
valid_hl = df['High'] >= df['Low']
# Contexto: El máximo debe ser >= mínimo por definición

# Validación High-Open-Close
valid_hoc = (
    (df['High'] >= df['Open']) &
    (df['High'] >= df['Close'])
)
# Contexto: El máximo debe contener apertura y cierre

# Validación Low-Open-Close
valid_loc = (
    (df['Low'] <= df['Open']) &
    (df['Low'] <= df['Close'])
)
# Contexto: El mínimo debe contener apertura y cierre
```

#### Volumen

```python
valid_volume = df['Volume'] > 0
# Contexto: Volumen debe ser positivo para trading real
```

#### Precios Positivos

```python
valid_prices = (
    (df['Open'] > 0) &
    (df['High'] > 0) &
    (df['Low'] > 0) &
    (df['Close'] > 0)
)
# Contexto: Precios negativos no tienen sentido en mercados de futuros
```

#### Timestamps Cronológicos

```python
df['TimeDiff'] = df['DateTime'].diff()
backward_jumps = (df['TimeDiff'] < timedelta(0)).sum()
if backward_jumps > 0:
    df.loc[df['TimeDiff'] < timedelta(0), 'Valid'] = False
# Contexto: El tiempo no puede retroceder
```

---

## Manejo de Errores

### Errores Durante la Carga

```python
try:
    df = pd.read_csv(filepath, sep=';', header=None, names=columns)
except Exception as e:
    logger.error(f"❌ Error al cargar {filepath}: {str(e)}")
    return None
```

**Tipos de Errores Manejados:**
- Archivo no encontrado
- Formato incorrecto
- Permisos insuficientes
- Memoria insuficiente

### Timestamps Inválidos

```python
df['DateTime'] = pd.to_datetime(
    df['DateTimeStr'],
    format='%Y%m%d %H%M%S',
    errors='coerce'  # Convierte inválidos a NaT
)

invalid_timestamps = df['DateTime'].isna().sum()
if invalid_timestamps > 0:
    logger.warning(f"⚠️  {invalid_timestamps} timestamps inválidos")
    df = df.dropna(subset=['DateTime'])
```

### Datos Vacíos

```python
if len(dfs) == 0:
    logger.error("❌ No se cargaron datos")
    return None
```

---

## Optimización y Performance

### Uso de Memoria

**Carga Completa vs Chunks:**

```python
# Actual: Carga completa
df = pd.read_csv(archivo)  # ~200-300 MB para 1.6M registros

# Alternativa si memoria es limitada:
chunks = []
for chunk in pd.read_csv(archivo, chunksize=100000):
    # Procesar chunk
    chunks.append(chunk)
df = pd.concat(chunks)
```

**Ventajas Carga Completa:**
- Más rápido
- Código más simple
- Suficiente para este volumen

**Cuándo Usar Chunks:**
- Datos > 5M registros
- Memoria RAM < 8GB
- Procesamiento en servidor limitado

### Operaciones Vectorizadas

```python
# Eficiente: Operaciones vectorizadas
df['Valid'] = (
    (df['High'] >= df['Low']) &  # pandas vectorizado
    (df['Volume'] > 0)
)

# Ineficiente: Loops
for idx, row in df.iterrows():  # EVITAR
    if row['High'] >= row['Low']:
        df.at[idx, 'Valid'] = True
```

### Ordenamiento y Duplicados

```python
# Optimizado
df = df.sort_values('DateTime').reset_index(drop=True)
df = df.drop_duplicates(subset=['DateTime'], keep='first')

# Alternativa con hash (si muchos duplicados)
df = df.drop_duplicates(subset=['DateTime'], keep='first', ignore_index=True)
```

---

## Troubleshooting

### Problemas Comunes

#### 1. Timestamps Inválidos

**Síntoma:**
```
⚠️  NQ 03-21.Last.txt: 150 timestamps inválidos
```

**Causa:**
- Formato incorrecto en archivo origen
- Caracteres no numéricos en fecha/hora
- Fechas imposibles (ej: 2021-02-30)

**Solución:**
```python
# El script maneja automáticamente con errors='coerce'
df['DateTime'] = pd.to_datetime(df['DateTimeStr'], errors='coerce')
df = df.dropna(subset=['DateTime'])
```

#### 2. Duplicados Excesivos

**Síntoma:**
```
⚠️  50,000 timestamps duplicados eliminados
```

**Causa:**
- Overlap largo entre contratos
- Datos repetidos en archivos origen

**Solución:**
- Verificar archivos origen
- Confirmar estrategia `keep='first'` es apropiada
- Revisar logs para identificar archivos problemáticos

#### 3. Gaps Largos Inesperados

**Síntoma:**
```
⚠️  Gap largo: 2021-05-15 - Gap: 150000 min
```

**Causa:**
- Datos faltantes en archivo origen
- Problema en recolección de datos
- Evento de mercado (suspensión)

**Solución:**
1. Verificar archivo origen correspondiente
2. Consultar calendario de mercado para el periodo
3. Si es error de datos, corregir archivo origen

#### 4. Memoria Insuficiente

**Síntoma:**
```
MemoryError: Unable to allocate array
```

**Causa:**
- RAM insuficiente
- Otros procesos consumiendo memoria

**Solución:**
```python
# Modificar script para usar chunks
chunks = []
for chunk in pd.read_csv(archivo, chunksize=50000):
    # Procesar chunk
    chunks.append(chunk)
df = pd.concat(chunks, ignore_index=True)
```

#### 5. Archivo CSV Corrupto

**Síntoma:**
```
❌ Error al cargar archivo: CParserError
```

**Causa:**
- Archivo dañado
- Formato inconsistente
- Caracteres especiales

**Solución:**
1. Abrir archivo en editor de texto
2. Verificar formato visual
3. Buscar líneas problemáticas
4. Corregir manualmente o contactar proveedor de datos

---

## Ejemplos de Uso

### Ejemplo 1: Ejecución Básica

```bash
cd "C:\Users\oscar\Documents\Proyecto-Trading\Github\NQ_Backtest\Scripts"
python consolidar_datos_minutos.py
```

**Output Esperado:**
```
2025-12-04 10:02:11 - INFO - PASO 1/4: Consolidando archivos...
2025-12-04 10:02:11 - INFO - Archivos encontrados: 20
2025-12-04 10:02:11 - INFO - Archivo cargado: NQ 03-21.Last.txt (88776 registros)
...
2025-12-04 10:02:36 - INFO - ✅ CONSOLIDACIÓN COMPLETADA EXITOSAMENTE
```

### Ejemplo 2: División por Años

```bash
cd "C:\Users\oscar\Documents\Proyecto-Trading\Github\NQ_Backtest\Scripts"
python dividir_datos_minutos_por_anio.py
```

**Output Esperado:**
```
2025-12-04 10:19:23 - INFO - Archivo cargado exitosamente: 1,612,055 registros
2025-12-04 10:19:25 - INFO - Años encontrados: [2020, 2021, 2022, 2023, 2024, 2025]
...
2025-12-04 10:19:29 - INFO - ✅ DIVISIÓN COMPLETADA EXITOSAMENTE
```

### Ejemplo 3: Verificación de Datos

```python
import pandas as pd

# Cargar datos consolidados
df = pd.read_csv('../Procesados/NQ_1min_2020-2025_Limpio.csv',
                 parse_dates=['DateTime'])

# Verificar rango temporal
print(f"Fecha inicio: {df['DateTime'].min()}")
print(f"Fecha fin: {df['DateTime'].max()}")
print(f"Total registros: {len(df):,}")

# Verificar datos por año
print("\nRegistros por año:")
print(df['DateTime'].dt.year.value_counts().sort_index())

# Verificar continuidad
df['Gap'] = df['DateTime'].diff()
gaps_grandes = df[df['Gap'] > pd.Timedelta(hours=24)]
print(f"\nGaps > 24 horas: {len(gaps_grandes)}")
```

### Ejemplo 4: Análisis Rápido de un Año

```python
import pandas as pd

# Cargar solo 2024
df_2024 = pd.read_csv('../Procesados/2024/NQ_1min_2024.csv',
                      parse_dates=['DateTime'])

# Estadísticas básicas
print("Estadísticas 2024:")
print(df_2024[['Open', 'High', 'Low', 'Close', 'Volume']].describe())

# Precio promedio por mes
df_2024['Mes'] = df_2024['DateTime'].dt.month
promedio_mensual = df_2024.groupby('Mes')['Close'].mean()
print("\nPrecio promedio por mes:")
print(promedio_mensual)
```

---

## Apéndices

### A. Configuración de Rutas

```python
# Archivo: consolidar_datos_minutos.py
DATOS_MINUTOS_PATH = Path("..") / "datos brutos" / "datos ninjatrader" / "Minutos"
OUTPUT_PATH = Path("..") / "Originales"
PROCESSED_PATH = Path("..") / "Procesados"

# Para modificar rutas, editar estas constantes
```

### B. Formato de Logs

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../Logs/consolidacion_minutos.log'),
        logging.StreamHandler()
    ]
)
```

**Niveles de Log:**
- `INFO`: Información general del proceso
- `WARNING`: Situaciones que requieren atención
- `ERROR`: Errores que impiden continuar

### C. Dependencias

```python
# requirements.txt
pandas>=1.3.0
numpy>=1.21.0
```

**Instalación:**
```bash
pip install pandas numpy
```

---

**Fin de la Guía Técnica**

*Última actualización: 2025-12-04*
*Versión: 1.0*
