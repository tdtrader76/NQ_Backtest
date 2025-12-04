"""
Script de Consolidación de Datos Intradiarios NQ
Versión: 1.0
Fecha: 2025-12-04
Autor: Sistema Backtesting NASDAQ

Descripción:
    Consolida todos los archivos de datos de minutos de NinjaTrader
    en un único archivo CSV limpio, validado y ordenado cronológicamente.

Formato de entrada: YYYYMMDD HHMMSS;Open;High;Low;Close;Volume
Formato de salida: DateTime,Open,High,Low,Close,Volume
"""

import pandas as pd
from pathlib import Path
import logging
from datetime import timedelta

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../Logs/consolidacion_minutos.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Constantes
DATOS_MINUTOS_PATH = Path("..") / "datos brutos" / "datos ninjatrader" / "Minutos"
OUTPUT_PATH = Path("..") / "Originales"
PROCESSED_PATH = Path("..") / "Procesados"

def cargar_archivo_minutos(filepath):
    """
    Carga un archivo de datos de minutos de NinjaTrader

    Args:
        filepath: Ruta al archivo .txt

    Returns:
        DataFrame con datos del archivo o None si hay error
    """
    try:
        # Leer archivo sin headers, separador ';'
        df = pd.read_csv(
            filepath,
            sep=';',
            header=None,
            names=['DateTimeStr', 'Open', 'High', 'Low', 'Close', 'Volume']
        )

        # Convertir 'YYYYMMDD HHMMSS' a datetime
        df['DateTime'] = pd.to_datetime(
            df['DateTimeStr'],
            format='%Y%m%d %H%M%S',
            errors='coerce'
        )

        # Eliminar columna temporal y reordenar
        df = df.drop(columns=['DateTimeStr'])
        df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]

        # Validar timestamps
        invalid_timestamps = df['DateTime'].isna().sum()
        if invalid_timestamps > 0:
            logger.warning(f"⚠️  {filepath.name}: {invalid_timestamps} timestamps inválidos")
            df = df.dropna(subset=['DateTime'])

        logger.info(f"✅ Archivo cargado: {filepath.name} ({len(df)} registros)")
        if len(df) > 0:
            logger.info(f"   Rango: {df['DateTime'].min()} a {df['DateTime'].max()}")

        return df

    except Exception as e:
        logger.error(f"❌ Error al cargar {filepath}: {str(e)}")
        return None

def consolidar_datos_minutos():
    """
    Consolida todos los archivos de datos de minutos en un solo DataFrame

    Returns:
        DataFrame consolidado con todos los datos de minutos
    """
    logger.info("="*80)
    logger.info("INICIANDO CONSOLIDACIÓN DE DATOS DE MINUTOS")
    logger.info("="*80)

    # Buscar todos los archivos .txt en la carpeta
    archivos = sorted(list(DATOS_MINUTOS_PATH.glob("*.txt")))
    logger.info(f"📂 Archivos encontrados: {len(archivos)}")

    # Lista para almacenar DataFrames
    dfs = []

    # Cargar cada archivo
    for archivo in archivos:
        df = cargar_archivo_minutos(archivo)
        if df is not None and len(df) > 0:
            dfs.append(df)

    # Consolidar todos los DataFrames
    if len(dfs) == 0:
        logger.error("❌ No se cargaron datos")
        return None

    df_consolidado = pd.concat(dfs, ignore_index=True)
    logger.info(f"\n📊 Total registros antes de limpieza: {len(df_consolidado):,}")

    # Ordenar por DateTime
    df_consolidado = df_consolidado.sort_values('DateTime').reset_index(drop=True)
    logger.info(f"✅ Datos ordenados cronológicamente")

    # Eliminar duplicados por DateTime (mantener el primero)
    registros_antes = len(df_consolidado)
    df_consolidado = df_consolidado.drop_duplicates(subset=['DateTime'], keep='first')
    duplicados_eliminados = registros_antes - len(df_consolidado)

    if duplicados_eliminados > 0:
        logger.warning(f"⚠️  {duplicados_eliminados:,} timestamps duplicados eliminados (keep='first')")

    logger.info(f"📊 Total registros después de eliminar duplicados: {len(df_consolidado):,}")

    return df_consolidado

def validar_datos(df):
    """
    Valida que los datos cumplan con las reglas de mercado

    Args:
        df: DataFrame con datos de minutos

    Returns:
        DataFrame con columna 'Valid' indicando si cada registro es válido
    """
    logger.info("\n" + "="*80)
    logger.info("VALIDANDO DATOS")
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

    # Validación adicional: detectar saltos hacia atrás en el tiempo
    df['TimeDiff'] = df['DateTime'].diff()
    backward_jumps = (df['TimeDiff'] < timedelta(0)).sum()

    if backward_jumps > 0:
        logger.warning(f"⚠️  {backward_jumps} saltos hacia atrás en el tiempo detectados")
        df.loc[df['TimeDiff'] < timedelta(0), 'Valid'] = False

    # Identificar registros inválidos
    invalid = df[~df['Valid']]

    logger.info(f"✅ Registros válidos: {df['Valid'].sum():,}")
    logger.info(f"❌ Registros inválidos: {len(invalid):,}")

    if len(invalid) > 0 and len(invalid) <= 20:
        logger.warning("\n⚠️  REGISTROS INVÁLIDOS DETECTADOS:")
        for idx, row in invalid.head(20).iterrows():
            logger.warning(
                f"  {row['DateTime']} | O:{row['Open']} H:{row['High']} "
                f"L:{row['Low']} C:{row['Close']} V:{row['Volume']}"
            )
    elif len(invalid) > 20:
        logger.warning(f"\n⚠️  Demasiados registros inválidos para mostrar individualmente")

    # Limpiar columna temporal
    df = df.drop(columns=['TimeDiff'])

    return df

def detectar_gaps(df, reportar_log=True):
    """
    Detecta gaps temporales significativos en los datos

    Args:
        df: DataFrame con datos ordenados por DateTime
        reportar_log: Si True, escribe gaps en el log

    Returns:
        DataFrame con información de gaps detectados o None
    """
    logger.info("\n" + "="*80)
    logger.info("DETECTANDO GAPS TEMPORALES")
    logger.info("="*80)

    # Calcular diferencia entre timestamps consecutivos
    df['TimeDiff'] = df['DateTime'].diff()

    # Gaps > 5 minutos durante trading
    MAX_GAP_MINUTOS_TRADING = 5
    gaps = df[df['TimeDiff'] > timedelta(minutes=MAX_GAP_MINUTOS_TRADING)].copy()

    if len(gaps) > 0:
        logger.info(f"⚠️  {len(gaps):,} gaps detectados (> {MAX_GAP_MINUTOS_TRADING} minutos)")

        if reportar_log:
            # Convertir gaps a minutos
            gaps['GapMinutos'] = gaps['TimeDiff'].dt.total_seconds() / 60

            # Clasificar gaps
            gaps['Clasificacion'] = gaps['GapMinutos'].apply(
                lambda x: 'Cierre diario' if x <= 120  # 2 horas
                else 'Fin de semana' if x <= 4320  # 72 horas
                else 'Gap largo'
            )

            # Resumir por clasificación
            clasificacion_counts = gaps['Clasificacion'].value_counts()
            logger.info("\n📊 Clasificación de gaps:")
            for clasificacion, count in clasificacion_counts.items():
                logger.info(f"   {clasificacion}: {count:,}")

            # Mostrar los 10 gaps más largos
            logger.info("\n📋 Top 10 gaps más largos:")
            top_gaps = gaps.nlargest(10, 'GapMinutos')
            for idx, row in top_gaps.iterrows():
                logger.info(
                    f"   {row['DateTime']} - Gap: {row['GapMinutos']:.0f} min "
                    f"({row['Clasificacion']})"
                )
    else:
        logger.info("✅ No se detectaron gaps significativos")

    # Limpiar columna temporal del DataFrame original
    df = df.drop(columns=['TimeDiff'])

    return gaps if len(gaps) > 0 else None

def exportar_datos(df, filename):
    """
    Exporta datos a archivos CSV

    Args:
        df: DataFrame a exportar
        filename: Nombre base del archivo (sin extensión)
    """
    logger.info("\n" + "="*80)
    logger.info("EXPORTANDO DATOS")
    logger.info("="*80)

    # Crear carpetas si no existen
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    # Exportar versión original (con todos los datos incluidos inválidos)
    output_file_orig = OUTPUT_PATH / f"{filename}.csv"
    df.to_csv(output_file_orig, index=False, date_format='%Y-%m-%d %H:%M:%S')
    logger.info(f"✅ Archivo original guardado: {output_file_orig}")
    logger.info(f"   ({len(df):,} registros, incluye columna 'Valid')")

    # Exportar versión limpia (solo datos válidos)
    df_limpio = df[df['Valid']].drop(columns=['Valid'])
    output_file_clean = PROCESSED_PATH / f"{filename}_Limpio.csv"
    df_limpio.to_csv(output_file_clean, index=False, date_format='%Y-%m-%d %H:%M:%S')
    logger.info(f"✅ Archivo limpio guardado: {output_file_clean}")
    logger.info(f"   ({len(df_limpio):,} registros)")

    # Estadísticas finales
    logger.info(f"\n📊 ESTADÍSTICAS FINALES:")
    logger.info(f"   Total registros: {len(df):,}")
    logger.info(f"   Registros válidos: {len(df_limpio):,}")
    logger.info(f"   Registros inválidos: {len(df) - len(df_limpio):,}")
    logger.info(f"   Fecha/hora inicio: {df_limpio['DateTime'].min()}")
    logger.info(f"   Fecha/hora fin: {df_limpio['DateTime'].max()}")

    # Calcular duración total
    duracion = df_limpio['DateTime'].max() - df_limpio['DateTime'].min()
    dias = duracion.days
    logger.info(f"   Duración: {dias} días ({dias/365:.1f} años)")

    # Calcular densidad de datos (cobertura temporal)
    minutos_esperados = duracion.total_seconds() / 60
    cobertura = (len(df_limpio) / minutos_esperados) * 100 if minutos_esperados > 0 else 0
    logger.info(f"   Cobertura temporal: {cobertura:.2f}% (considerando 24/7)")

    # Estadísticas de precios
    logger.info(f"\n📈 RANGOS DE PRECIOS:")
    logger.info(f"   Mínimo: {df_limpio['Low'].min():.2f}")
    logger.info(f"   Máximo: {df_limpio['High'].max():.2f}")
    logger.info(f"   Close promedio: {df_limpio['Close'].mean():.2f}")
    logger.info(f"   Volumen total: {df_limpio['Volume'].sum():,.0f}")

    return df_limpio

def main():
    """
    Función principal
    """
    try:
        # 1. Consolidar datos
        logger.info("PASO 1/4: Consolidando archivos...")
        df = consolidar_datos_minutos()

        if df is None:
            logger.error("❌ No se pudieron consolidar los datos")
            return

        # 2. Validar datos
        logger.info("\nPASO 2/4: Validando datos...")
        df = validar_datos(df)

        # 3. Detectar gaps
        logger.info("\nPASO 3/4: Detectando gaps temporales...")
        gaps = detectar_gaps(df, reportar_log=True)

        # 4. Exportar datos
        logger.info("\nPASO 4/4: Exportando datos...")
        df_limpio = exportar_datos(df, "NQ_1min_2020-2025")

        logger.info("\n" + "="*80)
        logger.info("✅ CONSOLIDACIÓN COMPLETADA EXITOSAMENTE")
        logger.info("="*80)

    except Exception as e:
        logger.error(f"❌ Error en ejecución principal: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
