"""
Script de Consolidación de Datos Diarios NQ
Versión: 1.0
Fecha: 2025-01-26
Autor: Sistema Backtesting NASDAQ

Descripción:
    Consolida todos los archivos de datos diarios de NinjaTrader
    en un único archivo CSV limpio y validado.

Formato de entrada: YYYYMMDD;Open;High;Low;Close;Volume
Formato de salida: Date,Open,High,Low,Close,Volume
"""

import pandas as pd
import glob
import os
from pathlib import Path
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../Logs/consolidacion_diarios.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Constantes
DATOS_DIARIOS_PATH = Path("..") / "datos brutos" / "datos ninjatrader" / "Diarios"
OUTPUT_PATH = Path("..") / "Originales"
PROCESSED_PATH = Path("..") / "Procesados"

def cargar_archivo_diario(filepath):
    """
    Carga un archivo de datos diarios de NinjaTrader

    Args:
        filepath: Ruta al archivo .txt

    Returns:
        DataFrame con datos del archivo
    """
    try:
        # Leer archivo con formato NinjaTrader (sin headers)
        df = pd.read_csv(
            filepath,
            sep=';',
            header=None,
            names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        )

        # Convertir Date a datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

        # Extraer nombre de archivo para logging
        filename = os.path.basename(filepath)
        logger.info(f"✅ Archivo cargado: {filename} ({len(df)} registros)")

        return df

    except Exception as e:
        logger.error(f"❌ Error al cargar {filepath}: {str(e)}")
        return None

def consolidar_datos_diarios():
    """
    Consolida todos los archivos de datos diarios en un solo DataFrame

    Returns:
        DataFrame consolidado con todos los datos diarios
    """
    logger.info("="*80)
    logger.info("INICIANDO CONSOLIDACIÓN DE DATOS DIARIOS")
    logger.info("="*80)

    # Buscar todos los archivos .txt en la carpeta
    archivos = list(DATOS_DIARIOS_PATH.glob("*.txt"))
    logger.info(f"📂 Archivos encontrados: {len(archivos)}")

    # Lista para almacenar DataFrames
    dfs = []

    # Cargar cada archivo
    for archivo in sorted(archivos):
        df = cargar_archivo_diario(archivo)
        if df is not None and len(df) > 0:
            dfs.append(df)

    # Consolidar todos los DataFrames
    if len(dfs) == 0:
        logger.error("❌ No se cargaron datos")
        return None

    df_consolidado = pd.concat(dfs, ignore_index=True)
    logger.info(f"📊 Total registros antes de limpieza: {len(df_consolidado)}")

    # Eliminar duplicados por fecha
    df_consolidado = df_consolidado.drop_duplicates(subset=['Date'], keep='first')
    logger.info(f"📊 Total registros después de eliminar duplicados: {len(df_consolidado)}")

    # Ordenar por fecha
    df_consolidado = df_consolidado.sort_values('Date').reset_index(drop=True)

    return df_consolidado

def validar_datos(df):
    """
    Valida que los datos cumplan con las reglas de mercado

    Args:
        df: DataFrame con datos diarios

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

    # Identificar registros inválidos
    invalid = df[~df['Valid']]

    logger.info(f"✅ Registros válidos: {df['Valid'].sum()}")
    logger.info(f"❌ Registros inválidos: {len(invalid)}")

    if len(invalid) > 0:
        logger.warning("\n⚠️  REGISTROS INVÁLIDOS DETECTADOS:")
        for idx, row in invalid.iterrows():
            logger.warning(f"  Fecha: {row['Date']} | O:{row['Open']} H:{row['High']} L:{row['Low']} C:{row['Close']} V:{row['Volume']}")

    return df

def exportar_datos(df, filename):
    """
    Exporta datos a archivos CSV y Excel

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
    df.to_csv(output_file_orig, index=False)
    logger.info(f"✅ Archivo original guardado: {output_file_orig}")

    # Exportar versión limpia (solo datos válidos)
    df_limpio = df[df['Valid']].drop(columns=['Valid'])
    output_file_clean = PROCESSED_PATH / f"{filename}_Limpio.csv"
    df_limpio.to_csv(output_file_clean, index=False)
    logger.info(f"✅ Archivo limpio guardado: {output_file_clean}")

    # Estadísticas finales
    logger.info(f"\n📊 ESTADÍSTICAS FINALES:")
    logger.info(f"   Total registros: {len(df)}")
    logger.info(f"   Registros válidos: {len(df_limpio)}")
    logger.info(f"   Fecha inicio: {df_limpio['Date'].min()}")
    logger.info(f"   Fecha fin: {df_limpio['Date'].max()}")
    logger.info(f"   Días de datos: {(df_limpio['Date'].max() - df_limpio['Date'].min()).days}")

    return df_limpio

def main():
    """
    Función principal
    """
    try:
        # 1. Consolidar datos
        df = consolidar_datos_diarios()

        if df is None:
            logger.error("❌ No se pudieron consolidar los datos")
            return

        # 2. Validar datos
        df = validar_datos(df)

        # 3. Exportar datos
        df_limpio = exportar_datos(df, "NQ_Daily_2020-2025")

        logger.info("\n" + "="*80)
        logger.info("✅ CONSOLIDACIÓN COMPLETADA EXITOSAMENTE")
        logger.info("="*80)

    except Exception as e:
        logger.error(f"❌ Error en ejecución principal: {str(e)}")
        raise

if __name__ == "__main__":
    main()
