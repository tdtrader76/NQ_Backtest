"""
Script de Cálculo de Niveles - FASE 1 Tarea 1.3
Versión: 1.0
Fecha: 2025-01-26
Autor: Sistema Backtesting NASDAQ

Descripción:
    Calcula Expected Move High (EMH) y Expected Move Low (EML) usando
    la misma fórmula del indicador RyFEM.cs de NinjaTrader.

Fórmula RyFEM (Expected Move):
    1. Clasificar días históricos:
       - Días alcistas: Close > Open
       - Días bajistas: Close <= Open

    2. Calcular promedios de rangos:
       - Rango alcista promedio = promedio(High - Low) de días alcistas
       - Rango bajista promedio = promedio(High - Low) de días bajistas

    3. Aplicar multiplicador de desviación estándar:
       - RANGE_MULTIPLIER = 0.682 (68.2%)

    4. Calcular niveles esperados:
       - EMH = Open + (Rango_Alcista_Promedio * 0.682)
       - EML = Open - (Rango_Bajista_Promedio * 0.682)
       - EM_Range = EMH - EML

    5. Redondear a cuartos (.00, .25, .50, .75):
       - Redondeo hacia arriba (ceiling)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../Logs/fase1_calcular_niveles.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Constantes
DATA_PATH = Path("..") / "Procesados" / "NQ_Daily_2020-2025_Limpio.csv"
OUTPUT_PATH_CSV = Path("..") / "Calculados" / "Niveles_Diarios.csv"
OUTPUT_PATH_EXCEL = Path("..") / "Calculados" / "Niveles_Diarios.xlsx"

# Constantes de la fórmula RyFEM
RANGE_MULTIPLIER = 0.682  # 68.2% para desviación estándar
DEFAULT_LENGTH = 21        # Período de lookback por defecto

def cargar_datos():
    """
    Carga los datos diarios limpios

    Returns:
        DataFrame con datos diarios
    """
    logger.info("="*80)
    logger.info("CARGANDO DATOS")
    logger.info("="*80)

    try:
        df = pd.read_csv(DATA_PATH)
        df['Date'] = pd.to_datetime(df['Date'])

        logger.info(f"OK Datos cargados: {len(df)} registros")
        logger.info(f"Período: {df['Date'].min()} a {df['Date'].max()}")

        return df

    except Exception as e:
        logger.error(f"ERROR al cargar datos: {str(e)}")
        raise

def clasificar_dias(df):
    """
    Clasifica días como alcistas o bajistas según RyFEM.cs

    Lógica:
        - Alcista: Close > Open
        - Bajista: Close <= Open

    Args:
        df: DataFrame con datos diarios

    Returns:
        DataFrame con columna 'IsBullish' agregada
    """
    logger.info("\n" + "="*80)
    logger.info("CLASIFICANDO DIAS ALCISTAS/BAJISTAS")
    logger.info("="*80)

    # Clasificar según fórmula RyFEM
    df['IsBullish'] = df['Close'] > df['Open']

    # Calcular rango diario
    df['Range'] = df['High'] - df['Low']

    # Estadísticas
    bullish_count = df['IsBullish'].sum()
    bearish_count = (~df['IsBullish']).sum()

    logger.info(f"Total días: {len(df)}")
    logger.info(f"Días alcistas: {bullish_count} ({bullish_count/len(df)*100:.1f}%)")
    logger.info(f"Días bajistas: {bearish_count} ({bearish_count/len(df)*100:.1f}%)")
    logger.info(f"Rango promedio alcista: {df[df['IsBullish']]['Range'].mean():.2f}")
    logger.info(f"Rango promedio bajista: {df[~df['IsBullish']]['Range'].mean():.2f}")

    return df

def calcular_promedios_historicos(df, lookback=DEFAULT_LENGTH):
    """
    Calcula promedios de rangos alcistas y bajistas para cada día

    Para cada día, calcula el promedio de los últimos N días:
    - Rango alcista promedio (de días alcistas)
    - Rango bajista promedio (de días bajistas)

    Args:
        df: DataFrame con datos y clasificación
        lookback: Número de días históricos a considerar

    Returns:
        DataFrame con columnas de promedios agregadas
    """
    logger.info("\n" + "="*80)
    logger.info(f"CALCULANDO PROMEDIOS HISTORICOS (Lookback={lookback})")
    logger.info("="*80)

    # Inicializar columnas
    df['BullishAvg'] = 0.0
    df['BearishAvg'] = 0.0
    df['BullishCount'] = 0
    df['BearishCount'] = 0

    # Calcular para cada día
    for i in range(len(df)):
        # Necesitamos al menos 'lookback' días históricos
        if i < lookback:
            continue

        # Obtener ventana histórica (días anteriores)
        start_idx = i - lookback
        end_idx = i  # No incluye el día actual

        historical_window = df.iloc[start_idx:end_idx]

        # Separar días alcistas y bajistas
        bullish_days = historical_window[historical_window['IsBullish']]
        bearish_days = historical_window[~historical_window['IsBullish']]

        # Calcular promedios
        if len(bullish_days) > 0:
            df.loc[df.index[i], 'BullishAvg'] = bullish_days['Range'].mean()
            df.loc[df.index[i], 'BullishCount'] = len(bullish_days)

        if len(bearish_days) > 0:
            df.loc[df.index[i], 'BearishAvg'] = bearish_days['Range'].mean()
            df.loc[df.index[i], 'BearishCount'] = len(bearish_days)

    logger.info(f"OK Promedios calculados para {len(df[df['BullishAvg'] > 0])} días")

    return df

def calcular_expected_move(df):
    """
    Calcula Expected Move High y Low según fórmula RyFEM.cs

    Fórmula:
        EMH = Open + (BullishAvg * RANGE_MULTIPLIER)
        EML = Open - (BearishAvg * RANGE_MULTIPLIER)
        EM_Range = EMH - EML

    Args:
        df: DataFrame con promedios calculados

    Returns:
        DataFrame con columnas EMH, EML, EM_Range
    """
    logger.info("\n" + "="*80)
    logger.info("CALCULANDO EXPECTED MOVE")
    logger.info("="*80)
    logger.info(f"Multiplicador de rango: {RANGE_MULTIPLIER} (68.2%)")

    # Calcular Expected Move High
    df['EMH_Raw'] = df['Open'] + (df['BullishAvg'] * RANGE_MULTIPLIER)

    # Calcular Expected Move Low
    df['EML_Raw'] = df['Open'] - (df['BearishAvg'] * RANGE_MULTIPLIER)

    # Redondear a cuartos (como en RyFEM.cs)
    df['EMH'] = df['EMH_Raw'].apply(round_to_nearest_quarter)
    df['EML'] = df['EML_Raw'].apply(round_to_nearest_quarter)

    # Calcular rango total
    df['EM_Range'] = df['EMH'] - df['EML']

    # Estadísticas
    valid_em = df[df['EMH'] > 0]
    logger.info(f"\nEstadísticas Expected Move:")
    logger.info(f"  Días con EM válido: {len(valid_em)} de {len(df)}")
    logger.info(f"  EMH promedio: {valid_em['EMH'].mean():.2f}")
    logger.info(f"  EML promedio: {valid_em['EML'].mean():.2f}")
    logger.info(f"  EM_Range promedio: {valid_em['EM_Range'].mean():.2f}")
    logger.info(f"  EM_Range mínimo: {valid_em['EM_Range'].min():.2f}")
    logger.info(f"  EM_Range máximo: {valid_em['EM_Range'].max():.2f}")

    return df

def round_to_nearest_quarter(price):
    """
    Redondea precio al cuarto más cercano (.00, .25, .50, .75)
    Redondeo hacia arriba (ceiling) como en RyFEM.cs

    Args:
        price: Precio a redondear

    Returns:
        Precio redondeado al cuarto más cercano
    """
    if price <= 0:
        return price

    # Multiplicar por 4, ceiling, dividir por 4
    quarters = np.ceil(price * 4)
    return quarters / 4

def validar_calculos(df):
    """
    Valida que los cálculos sean correctos

    Args:
        df: DataFrame con niveles calculados
    """
    logger.info("\n" + "="*80)
    logger.info("VALIDANDO CALCULOS")
    logger.info("="*80)

    # Verificar que EMH > EML
    invalid_range = df[(df['EMH'] > 0) & (df['EMH'] <= df['EML'])]

    if len(invalid_range) > 0:
        logger.warning(f"WARN {len(invalid_range)} días con EMH <= EML:")
        for idx, row in invalid_range.head(5).iterrows():
            logger.warning(f"  {row['Date']}: EMH={row['EMH']:.2f}, EML={row['EML']:.2f}")
    else:
        logger.info("OK Todos los cálculos tienen EMH > EML")

    # Verificar redondeo a cuartos
    def check_quarter_multiple(value):
        """Verifica que el decimal sea múltiplo de 0.25"""
        if value <= 0:
            return True
        decimal = round((value % 1) * 100) / 100
        return decimal in [0.00, 0.25, 0.50, 0.75]

    emh_invalid = df[df['EMH'] > 0][~df[df['EMH'] > 0]['EMH'].apply(check_quarter_multiple)]
    eml_invalid = df[df['EML'] > 0][~df[df['EML'] > 0]['EML'].apply(check_quarter_multiple)]

    if len(emh_invalid) > 0 or len(eml_invalid) > 0:
        logger.warning(f"WARN Valores sin redondeo correcto:")
        logger.warning(f"  EMH: {len(emh_invalid)} valores")
        logger.warning(f"  EML: {len(eml_invalid)} valores")
    else:
        logger.info("OK Todos los valores redondeados correctamente a cuartos")

    # Verificar valores razonables
    valid_df = df[df['EMH'] > 0]
    avg_range_pct = (valid_df['EM_Range'] / valid_df['Open'] * 100).mean()

    logger.info(f"\nRango EM como % del Open: {avg_range_pct:.2f}%")

    if avg_range_pct < 0.5 or avg_range_pct > 5:
        logger.warning(f"WARN Rango promedio parece inusual: {avg_range_pct:.2f}%")
    else:
        logger.info("OK Rangos están dentro de valores esperados")

def exportar_resultados(df, lookback):
    """
    Exporta resultados a CSV y Excel

    Args:
        df: DataFrame con niveles calculados
        lookback: Período de lookback usado
    """
    logger.info("\n" + "="*80)
    logger.info("EXPORTANDO RESULTADOS")
    logger.info("="*80)

    # Crear carpeta si no existe
    Path("..") / "Calculados"
    (Path("..") / "Calculados").mkdir(parents=True, exist_ok=True)

    # Seleccionar columnas para exportar
    columnas_export = [
        'Date', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Range', 'IsBullish',
        'BullishAvg', 'BearishAvg', 'BullishCount', 'BearishCount',
        'EMH', 'EML', 'EM_Range'
    ]

    df_export = df[columnas_export].copy()

    # 1. Exportar a CSV
    df_export.to_csv(OUTPUT_PATH_CSV, index=False)
    logger.info(f"OK CSV exportado: {OUTPUT_PATH_CSV}")

    # 2. Exportar a Excel con formato
    with pd.ExcelWriter(OUTPUT_PATH_EXCEL, engine='openpyxl') as writer:
        # Hoja 1: Datos completos
        df_export.to_excel(writer, sheet_name='Niveles', index=False)

        # Hoja 2: Resumen estadístico
        stats = pd.DataFrame({
            'Métrica': [
                'Total Días',
                'Días con EM Válido',
                'Lookback Period',
                'Range Multiplier',
                'Días Alcistas (%)',
                'Días Bajistas (%)',
                'EMH Promedio',
                'EML Promedio',
                'EM_Range Promedio',
                'EM_Range Mínimo',
                'EM_Range Máximo',
                'EM_Range % Open'
            ],
            'Valor': [
                len(df),
                len(df[df['EMH'] > 0]),
                lookback,
                RANGE_MULTIPLIER,
                f"{df['IsBullish'].sum() / len(df) * 100:.1f}",
                f"{(~df['IsBullish']).sum() / len(df) * 100:.1f}",
                f"{df[df['EMH'] > 0]['EMH'].mean():.2f}",
                f"{df[df['EML'] > 0]['EML'].mean():.2f}",
                f"{df[df['EM_Range'] > 0]['EM_Range'].mean():.2f}",
                f"{df[df['EM_Range'] > 0]['EM_Range'].min():.2f}",
                f"{df[df['EM_Range'] > 0]['EM_Range'].max():.2f}",
                f"{(df[df['EMH'] > 0]['EM_Range'] / df[df['EMH'] > 0]['Open'] * 100).mean():.2f}%"
            ]
        })
        stats.to_excel(writer, sheet_name='Resumen', index=False)

    logger.info(f"OK Excel exportado: {OUTPUT_PATH_EXCEL}")

    # Mostrar muestra de resultados
    logger.info("\n--- MUESTRA DE RESULTADOS (últimos 5 días) ---")
    muestra = df_export[df_export['EMH'] > 0].tail(5)
    for _, row in muestra.iterrows():
        logger.info(
            f"{row['Date'].strftime('%Y-%m-%d')}: "
            f"Open={row['Open']:8.2f} | "
            f"EMH={row['EMH']:8.2f} | "
            f"EML={row['EML']:8.2f} | "
            f"Range={row['EM_Range']:6.2f}"
        )

def main():
    """
    Función principal
    """
    try:
        logger.info("\n" + "="*80)
        logger.info("FASE 1 - TAREA 1.3: CALCULO DE NIVELES (EXPECTED MOVE)")
        logger.info("="*80)
        logger.info(f"Fórmula: RyFEM.cs (Expected Move)")
        logger.info(f"Range Multiplier: {RANGE_MULTIPLIER} (68.2%)")
        logger.info(f"Lookback Period: {DEFAULT_LENGTH} días")

        # 1. Cargar datos
        df = cargar_datos()

        # 2. Clasificar días alcistas/bajistas
        df = clasificar_dias(df)

        # 3. Calcular promedios históricos
        df = calcular_promedios_historicos(df, lookback=DEFAULT_LENGTH)

        # 4. Calcular Expected Move
        df = calcular_expected_move(df)

        # 5. Validar cálculos
        validar_calculos(df)

        # 6. Exportar resultados
        exportar_resultados(df, lookback=DEFAULT_LENGTH)

        logger.info("\n" + "="*80)
        logger.info("TAREA 1.3 COMPLETADA EXITOSAMENTE")
        logger.info("="*80)

    except Exception as e:
        logger.error(f"ERROR en tarea 1.3: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
