"""
Script para Dividir Datos de Minutos por Año
Versión: 1.0
Fecha: 2025-12-04
Autor: Sistema Backtesting NASDAQ

Descripción:
    Divide el archivo consolidado de datos de minutos en archivos separados
    por año para facilitar el manejo y reducir el tamaño de los archivos.

Entrada: ../Procesados/NQ_1min_2020-2025_Limpio.csv
Salida: ../Procesados/YYYY/NQ_1min_YYYY.csv (un archivo por año)
"""

import pandas as pd
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../Logs/dividir_datos_minutos_por_anio.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Rutas
ARCHIVO_CONSOLIDADO = Path("..") / "Procesados" / "NQ_1min_2020-2025_Limpio.csv"
OUTPUT_BASE_PATH = Path("..") / "Procesados"

def cargar_datos_consolidados():
    """
    Carga el archivo consolidado de datos de minutos

    Returns:
        DataFrame con todos los datos de minutos
    """
    logger.info("="*80)
    logger.info("CARGANDO ARCHIVO CONSOLIDADO")
    logger.info("="*80)

    try:
        logger.info(f"Leyendo archivo: {ARCHIVO_CONSOLIDADO}")

        # Leer CSV con parsing de datetime
        df = pd.read_csv(
            ARCHIVO_CONSOLIDADO,
            parse_dates=['DateTime']
        )

        logger.info(f"Archivo cargado exitosamente: {len(df):,} registros")
        logger.info(f"Rango temporal: {df['DateTime'].min()} a {df['DateTime'].max()}")

        return df

    except Exception as e:
        logger.error(f"Error al cargar archivo: {str(e)}")
        return None

def dividir_por_anios(df):
    """
    Divide el DataFrame por años y guarda cada año en un archivo separado

    Args:
        df: DataFrame con todos los datos de minutos
    """
    logger.info("\n" + "="*80)
    logger.info("DIVIDIENDO DATOS POR AÑOS")
    logger.info("="*80)

    # Extraer el año de la columna DateTime
    df['Year'] = df['DateTime'].dt.year

    # Obtener lista de años únicos
    years = sorted(df['Year'].unique())
    logger.info(f"Años encontrados: {years}")

    # Procesar cada año
    for year in years:
        logger.info(f"\nProcesando año {year}...")

        # Filtrar datos del año
        df_year = df[df['Year'] == year].copy()

        # Eliminar columna Year antes de exportar
        df_year = df_year.drop(columns=['Year'])

        # Crear carpeta del año si no existe
        year_folder = OUTPUT_BASE_PATH / str(year)
        year_folder.mkdir(parents=True, exist_ok=True)

        # Ruta del archivo de salida
        output_file = year_folder / f"NQ_1min_{year}.csv"

        # Exportar a CSV
        df_year.to_csv(output_file, index=False, date_format='%Y-%m-%d %H:%M:%S')

        # Calcular tamaño del archivo
        file_size_mb = output_file.stat().st_size / (1024 * 1024)

        # Estadísticas del año
        logger.info(f"  Registros: {len(df_year):,}")
        logger.info(f"  Fecha inicio: {df_year['DateTime'].min()}")
        logger.info(f"  Fecha fin: {df_year['DateTime'].max()}")
        logger.info(f"  Archivo: {output_file}")
        logger.info(f"  Tamaño: {file_size_mb:.2f} MB")

    logger.info(f"\nTotal de archivos generados: {len(years)}")

def generar_resumen(df):
    """
    Genera un resumen de la división por años

    Args:
        df: DataFrame con todos los datos
    """
    logger.info("\n" + "="*80)
    logger.info("RESUMEN DE LA DIVISIÓN")
    logger.info("="*80)

    df['Year'] = df['DateTime'].dt.year

    resumen = df.groupby('Year').agg({
        'DateTime': ['count', 'min', 'max'],
        'Close': ['mean', 'min', 'max'],
        'Volume': 'sum'
    }).round(2)

    logger.info("\nEstadísticas por año:")
    logger.info(resumen.to_string())

    # Calcular porcentaje de datos por año
    total_registros = len(df)
    registros_por_anio = df.groupby('Year').size()
    porcentajes = (registros_por_anio / total_registros * 100).round(2)

    logger.info("\nDistribución de registros por año:")
    for year, pct in porcentajes.items():
        registros = registros_por_anio[year]
        logger.info(f"  {year}: {registros:,} registros ({pct:.2f}%)")

def main():
    """
    Función principal
    """
    try:
        logger.info("INICIO DEL PROCESO DE DIVISIÓN POR AÑOS")

        # 1. Cargar datos consolidados
        df = cargar_datos_consolidados()

        if df is None:
            logger.error("No se pudieron cargar los datos")
            return

        # 2. Dividir por años
        dividir_por_anios(df)

        # 3. Generar resumen
        generar_resumen(df)

        logger.info("\n" + "="*80)
        logger.info("DIVISIÓN COMPLETADA EXITOSAMENTE")
        logger.info("="*80)
        logger.info("\nArchivos generados en:")
        for year in sorted(df['Year'].unique()):
            output_file = OUTPUT_BASE_PATH / str(year) / f"NQ_1min_{year}.csv"
            logger.info(f"  {output_file}")

    except Exception as e:
        logger.error(f"Error en ejecución principal: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
