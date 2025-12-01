"""
Script de Análisis Exploratorio de Datos Diarios - FASE 1 Tarea 1.1
Versión: 1.0
Fecha: 2025-01-26
Autor: Sistema Backtesting NASDAQ

Descripción:
    Realiza análisis exploratorio completo de los datos diarios consolidados.
    Incluye validaciones estructurales, lógica de mercado y detección de anomalías.

Según PLAN_BACKTESTING_NASDAQ.md:
    - Validación estructural
    - Validación de lógica de mercado
    - Detección de anomalías y outliers
    - Generación de reportes estadísticos
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../Logs/fase1_exploracion_daily.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Configurar estilo de gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Constantes
DATA_PATH = Path("..") / "Procesados" / "NQ_Daily_2020-2025_Limpio.csv"
OUTPUT_PATH = Path("..") / "Resultados" / "Fase1"

def cargar_datos():
    """
    Carga los datos diarios limpios

    Returns:
        DataFrame con datos diarios
    """
    logger.info("="*80)
    logger.info("1.1.1 CARGA INICIAL DE DATOS")
    logger.info("="*80)

    try:
        df = pd.read_csv(DATA_PATH)
        logger.info(f"OK Datos cargados: {len(df)} registros")

        # Convertir Date a datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Información general
        logger.info("\n--- INFORMACION GENERAL ---")
        logger.info(f"Columnas: {list(df.columns)}")
        logger.info(f"Tipos de datos:\n{df.dtypes}")
        logger.info(f"\nPrimeras 5 filas:\n{df.head()}")
        logger.info(f"\nUltimas 5 filas:\n{df.tail()}")

        return df

    except Exception as e:
        logger.error(f"ERROR al cargar datos: {str(e)}")
        raise

def validacion_estructural(df):
    """
    1.1.2 Validación Estructural

    Verifica:
    - Precios con formato correcto (5 cifras, decimales .00 .25 .50 .75)
    - Columnas esperadas
    - Tipos de datos
    - Valores nulos
    - Duplicados

    Args:
        df: DataFrame con datos diarios

    Returns:
        DataFrame con resultados de validación
    """
    logger.info("\n" + "="*80)
    logger.info("1.1.2 VALIDACION ESTRUCTURAL")
    logger.info("="*80)

    resultados = {}

    # 1. Verificar columnas esperadas
    columnas_esperadas = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    columnas_presentes = all(col in df.columns for col in columnas_esperadas)
    resultados['Columnas_OK'] = columnas_presentes

    if columnas_presentes:
        logger.info("OK Todas las columnas esperadas presentes")
    else:
        logger.warning(f"WARN Columnas faltantes: {set(columnas_esperadas) - set(df.columns)}")

    # 2. Verificar tipos de datos
    tipos_correctos = (
        df['Date'].dtype == 'datetime64[ns]' and
        df['Open'].dtype in ['float64', 'float32', 'int64'] and
        df['High'].dtype in ['float64', 'float32', 'int64'] and
        df['Low'].dtype in ['float64', 'float32', 'int64'] and
        df['Close'].dtype in ['float64', 'float32', 'int64'] and
        df['Volume'].dtype in ['int64', 'int32', 'float64']
    )
    resultados['Tipos_OK'] = tipos_correctos

    if tipos_correctos:
        logger.info("OK Tipos de datos correctos")
    else:
        logger.warning(f"WARN Tipos de datos: {df.dtypes.to_dict()}")

    # 3. Verificar valores nulos
    nulos = df.isnull().sum()
    resultados['Nulos_Total'] = nulos.sum()

    if nulos.sum() == 0:
        logger.info("OK No hay valores nulos")
    else:
        logger.warning(f"WARN Valores nulos encontrados:\n{nulos[nulos > 0]}")

    # 4. Verificar duplicados de fecha
    duplicados = df['Date'].duplicated().sum()
    resultados['Duplicados'] = duplicados

    if duplicados == 0:
        logger.info("OK No hay fechas duplicadas")
    else:
        logger.warning(f"WARN {duplicados} fechas duplicadas encontradas")
        logger.warning(f"Fechas duplicadas: {df[df['Date'].duplicated()]['Date'].tolist()}")

    # 5. Verificar orden cronológico
    ordenado = df['Date'].is_monotonic_increasing
    resultados['Orden_Cronologico'] = ordenado

    if ordenado:
        logger.info("OK Fechas en orden cronológico")
    else:
        logger.warning("WARN Fechas NO están en orden cronológico")

    # 6. Verificar formato de decimales (deben ser .00, .25, .50, .75)
    def verificar_decimales(precio):
        """Verifica que el decimal sea múltiplo de 0.25"""
        decimal = round((precio % 1) * 100) / 100
        return decimal in [0.00, 0.25, 0.50, 0.75]

    precios_invalidos = []
    for col in ['Open', 'High', 'Low', 'Close']:
        invalidos = df[~df[col].apply(verificar_decimales)]
        if len(invalidos) > 0:
            precios_invalidos.append({
                'columna': col,
                'cantidad': len(invalidos),
                'ejemplos': invalidos.head(3)[[col]].to_dict()
            })

    resultados['Decimales_Invalidos'] = len(precios_invalidos)

    if len(precios_invalidos) == 0:
        logger.info("OK Todos los precios tienen decimales correctos (.00, .25, .50, .75)")
    else:
        logger.warning(f"WARN {len(precios_invalidos)} columnas con decimales inválidos:")
        for inv in precios_invalidos:
            logger.warning(f"  {inv['columna']}: {inv['cantidad']} precios inválidos")

    # Resumen
    logger.info("\n--- RESUMEN VALIDACION ESTRUCTURAL ---")
    for key, value in resultados.items():
        logger.info(f"{key}: {value}")

    return pd.Series(resultados)

def validacion_logica_mercado(df):
    """
    1.1.3 Validación de Lógica de Mercado

    Verifica:
    - High >= Low
    - High >= Open, Close
    - Low <= Open, Close
    - Volume > 0

    Args:
        df: DataFrame con datos diarios

    Returns:
        DataFrame con columna 'Valid' y registros inválidos
    """
    logger.info("\n" + "="*80)
    logger.info("1.1.3 VALIDACION DE LOGICA DE MERCADO")
    logger.info("="*80)

    # Crear columna de validación
    df['Valid'] = (
        (df['High'] >= df['Low']) &
        (df['High'] >= df['Open']) &
        (df['High'] >= df['Close']) &
        (df['Low'] <= df['Open']) &
        (df['Low'] <= df['Close']) &
        (df['Volume'] > 0) &
        (df['Open'] > 0) &
        (df['High'] > 0) &
        (df['Low'] > 0) &
        (df['Close'] > 0)
    )

    # Identificar registros inválidos
    invalid = df[~df['Valid']]

    logger.info(f"Registros validos: {df['Valid'].sum()}")
    logger.info(f"Registros invalidos: {len(invalid)}")
    logger.info(f"Porcentaje validez: {df['Valid'].sum() / len(df) * 100:.2f}%")

    if len(invalid) > 0:
        logger.warning("\nWARN REGISTROS INVALIDOS DETECTADOS:")
        for idx, row in invalid.iterrows():
            logger.warning(
                f"  {row['Date']}: O={row['Open']:.2f} H={row['High']:.2f} "
                f"L={row['Low']:.2f} C={row['Close']:.2f} V={row['Volume']}"
            )

    return df, invalid

def deteccion_anomalias(df):
    """
    1.1.4 Detección de Anomalías

    Calcula returns y detecta outliers usando Z-score

    Args:
        df: DataFrame con datos diarios

    Returns:
        DataFrame con returns y Z-scores, DataFrame con outliers
    """
    logger.info("\n" + "="*80)
    logger.info("1.1.4 DETECCION DE ANOMALIAS")
    logger.info("="*80)

    # Calcular returns diarios (variación porcentual)
    df['Returns'] = df['Close'].pct_change() * 100
    df['Returns_Abs'] = df['Returns'].abs()

    # Calcular Z-score de los returns (inicializar con NaN)
    df['Z_Score'] = np.nan
    returns_clean = df['Returns'].dropna()

    # Calcular Z-score solo para los valores no-NaN
    if len(returns_clean) > 0:
        z_scores = np.abs(stats.zscore(returns_clean))
        df.loc[returns_clean.index, 'Z_Score'] = z_scores

    # Detectar outliers (Z-score > 4)
    outliers = df[df['Z_Score'] > 4].copy()

    logger.info(f"\n--- ESTADISTICAS DE RETURNS ---")
    logger.info(f"Media: {returns_clean.mean():.4f}%")
    logger.info(f"Mediana: {returns_clean.median():.4f}%")
    logger.info(f"Desv. Estandar: {returns_clean.std():.4f}%")
    logger.info(f"Min: {returns_clean.min():.4f}%")
    logger.info(f"Max: {returns_clean.max():.4f}%")

    logger.info(f"\n--- OUTLIERS DETECTADOS ---")
    logger.info(f"Total outliers (Z-score > 4): {len(outliers)}")

    if len(outliers) > 0:
        logger.info("\nOutliers encontrados:")
        for idx, row in outliers.iterrows():
            logger.info(
                f"  {row['Date']}: Return={row['Returns']:.2f}%, "
                f"Z-score={row['Z_Score']:.2f}, Close={row['Close']:.2f}"
            )

    # Estadísticas adicionales
    logger.info(f"\n--- DISTRIBUCION DE RETURNS ---")
    percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    for p in percentiles:
        val = np.percentile(returns_clean, p)
        logger.info(f"Percentil {p:2d}%: {val:7.2f}%")

    return df, outliers

def generar_reporte_estadistico(df):
    """
    Genera reporte estadístico completo

    Args:
        df: DataFrame con datos diarios
    """
    logger.info("\n" + "="*80)
    logger.info("REPORTE ESTADISTICO COMPLETO")
    logger.info("="*80)

    # Estadísticas descriptivas
    logger.info("\n--- ESTADISTICAS DESCRIPTIVAS ---")
    logger.info(f"\n{df[['Open', 'High', 'Low', 'Close', 'Volume']].describe()}")

    # Rangos diarios
    df['Range'] = df['High'] - df['Low']
    df['Range_Pct'] = (df['Range'] / df['Close']) * 100

    logger.info("\n--- RANGOS DIARIOS ---")
    logger.info(f"Rango promedio: {df['Range'].mean():.2f} puntos")
    logger.info(f"Rango mediano: {df['Range'].median():.2f} puntos")
    logger.info(f"Rango minimo: {df['Range'].min():.2f} puntos")
    logger.info(f"Rango maximo: {df['Range'].max():.2f} puntos")
    logger.info(f"Rango promedio %: {df['Range_Pct'].mean():.2f}%")

    # Información temporal
    logger.info("\n--- INFORMACION TEMPORAL ---")
    logger.info(f"Fecha inicio: {df['Date'].min()}")
    logger.info(f"Fecha fin: {df['Date'].max()}")
    logger.info(f"Dias totales: {len(df)}")
    logger.info(f"Periodo: {(df['Date'].max() - df['Date'].min()).days} dias calendario")

    # Años completos
    df['Year'] = df['Date'].dt.year
    logger.info(f"\n--- REGISTROS POR AÑO ---")
    registros_por_ano = df.groupby('Year').size()
    for year, count in registros_por_ano.items():
        logger.info(f"  {year}: {count} dias de trading")

    return df

def exportar_resultados(df, invalid, outliers, validacion_struct):
    """
    Exporta resultados del análisis a archivos

    Args:
        df: DataFrame completo con análisis
        invalid: Registros inválidos
        outliers: Outliers detectados
        validacion_struct: Resultados validación estructural
    """
    logger.info("\n" + "="*80)
    logger.info("EXPORTANDO RESULTADOS")
    logger.info("="*80)

    # Crear carpeta si no existe
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    # 1. Exportar resumen estadístico a Excel
    output_excel = OUTPUT_PATH / "Daily_Report.xlsx"

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        # Hoja 1: Estadísticas descriptivas
        stats_df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Range', 'Range_Pct', 'Returns']].describe()
        stats_df.to_excel(writer, sheet_name='Estadisticas')

        # Hoja 2: Registros inválidos
        if len(invalid) > 0:
            invalid[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_excel(
                writer, sheet_name='Invalidos', index=False
            )

        # Hoja 3: Outliers
        if len(outliers) > 0:
            outliers[['Date', 'Close', 'Returns', 'Z_Score']].to_excel(
                writer, sheet_name='Outliers', index=False
            )

        # Hoja 4: Validación estructural
        validacion_struct.to_frame(name='Resultado').to_excel(
            writer, sheet_name='Validacion'
        )

        # Hoja 5: Por año
        yearly_stats = df.groupby('Year').agg({
            'Close': ['count', 'mean', 'std', 'min', 'max'],
            'Volume': ['sum', 'mean'],
            'Range': 'mean',
            'Returns': ['mean', 'std']
        }).round(2)
        yearly_stats.to_excel(writer, sheet_name='Por_Año')

    logger.info(f"OK Excel creado: {output_excel}")

    # 2. Exportar anomalías a CSV
    if len(invalid) > 0:
        output_invalid = OUTPUT_PATH / "Daily_Anomalies.csv"
        invalid.to_csv(output_invalid, index=False)
        logger.info(f"OK Anomalias exportadas: {output_invalid}")

    # 3. Exportar outliers a CSV
    if len(outliers) > 0:
        output_outliers = OUTPUT_PATH / "Daily_Outliers.csv"
        outliers.to_csv(output_outliers, index=False)
        logger.info(f"OK Outliers exportados: {output_outliers}")

def main():
    """
    Función principal
    """
    try:
        logger.info("\n" + "="*80)
        logger.info("FASE 1 - TAREA 1.1: ANALISIS EXPLORATORIO DE DATOS DIARIOS")
        logger.info("="*80)

        # 1. Cargar datos
        df = cargar_datos()

        # 2. Validación estructural
        validacion_struct = validacion_estructural(df)

        # 3. Validación lógica de mercado
        df, invalid = validacion_logica_mercado(df)

        # 4. Detección de anomalías
        df, outliers = deteccion_anomalias(df)

        # 5. Reporte estadístico
        df = generar_reporte_estadistico(df)

        # 6. Exportar resultados
        exportar_resultados(df, invalid, outliers, validacion_struct)

        logger.info("\n" + "="*80)
        logger.info("ANALISIS EXPLORATORIO COMPLETADO EXITOSAMENTE")
        logger.info("="*80)

    except Exception as e:
        logger.error(f"ERROR en analisis exploratorio: {str(e)}")
        raise

if __name__ == "__main__":
    main()
