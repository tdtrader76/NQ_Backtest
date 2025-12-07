# Versión 1.3 - 2025-12-07 - Corregido criterio "tocar": TCH/TCL vs Q1Y, TVH/TVL vs Q4Y

"""
Script de Análisis de Niveles TCH/TCL y TVH/TVL - FASE 1
Versión: 1.3
Fecha: 2025-12-07
Autor: Sistema Backtesting NASDAQ

Descripción:
    Analiza en detalle los niveles TCH/TCL y TVH/TVL para determinar:

    Para TCH/TCL (niveles superiores):
    - Toques de TCH y TCL (se comparan con Q1Y = High del día anterior)
    - Toca TCL: TCL <= Q1Y
    - Toca TCH: TCH <= Q1Y
    - Rupturas de TCH (High > TCH)
    - Toques de Q1 tras rotura
    - Vueltas a zona TCH-TCL tras rotura

    Para TVH/TVL (niveles inferiores):
    - Toques de TVH y TVL (se comparan con Q4Y = Low del día anterior)
    - Toca TVH: TVH >= Q4Y
    - Toca TVL: TVL >= Q4Y
    - Rupturas de TVL (Low < TVL)
    - Toques de Q4 tras rotura
    - Vueltas a zona TVL-TVH tras rotura

    Nomenclatura:
    - Q1Y = High del día anterior (High.shift(1))
    - Q4Y = Low del día anterior (Low.shift(1))
    - Q1Ex = Q1 = EMH (niveles EM21)
    - Q4Ex = Q4 = EML (niveles EM21)

Entrada:
    - Datos_2025_EM21_Niveles.xlsx (hoja 'Sheet1')

Salida:
    - Datos_2025_EM21_Niveles_actualizado.xlsx con 3 hojas nuevas:
        * Analisis_TCH_TCL: Estadísticas detalladas TCH/TCL
        * Analisis_TVH_TVL: Estadísticas detalladas TVH/TVL
        * Detalle_Rupturas: Tabla con días que rompieron TCH o TVL
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Configurar logging
log_path = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Logs")
log_path.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path / 'analizar_niveles_TC_TV.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Rutas de archivos
INPUT_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/Datos_2025_EM21_Niveles.xlsx")
OUTPUT_FILE = Path("c:/Users/oscar/Documents/Proyecto-Trading/Github/NQ_Backtest/Resultados/Fase1/Datos_2025_EM21_Niveles_actualizado.xlsx")

def cargar_datos():
    """
    Carga los datos del archivo Excel y crea columnas Q1Y y Q4Y

    Returns:
        DataFrame con datos completos incluyendo Q1Y (High día anterior) y Q4Y (Low día anterior)
    """
    logger.info("="*80)
    logger.info("CARGANDO DATOS")
    logger.info("="*80)

    try:
        df = pd.read_excel(INPUT_FILE, sheet_name='Sheet1')
        logger.info(f"OK Datos cargados: {len(df)} registros")
        logger.info(f"Columnas disponibles: {list(df.columns)}")

        # Convertir Date a datetime si es necesario
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            logger.info(f"Período: {df['Date'].min()} a {df['Date'].max()}")

        # Crear Q1Y y Q4Y (niveles del día anterior)
        df['Q1Y'] = df['High'].shift(1)  # High del día anterior
        df['Q4Y'] = df['Low'].shift(1)   # Low del día anterior

        # Eliminar primera fila (NaN por shift)
        registros_antes = len(df)
        df = df.dropna(subset=['Q1Y', 'Q4Y'])
        logger.info(f"Creadas columnas Q1Y y Q4Y (niveles día anterior)")
        logger.info(f"Registros después de eliminar primera fila: {len(df)} (antes: {registros_antes})")

        return df

    except Exception as e:
        logger.error(f"ERROR al cargar datos: {str(e)}")
        raise

def analizar_TCH_TCL(df):
    """
    Analiza niveles TCH/TCL con estadísticas detalladas

    IMPORTANTE: TCH y TCL se comparan con Q1Y (High del día anterior)
    - Toca TCH: TCH <= Q1Y
    - Toca TCL: TCL <= Q1Y

    Args:
        df: DataFrame con datos completos (debe incluir Q1Y)

    Returns:
        dict con estadísticas y DataFrame con detalles de rupturas
    """
    logger.info("\n" + "="*80)
    logger.info("ANALIZANDO NIVELES TCH/TCL")
    logger.info("="*80)

    # Verificar columnas necesarias
    required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'TCH', 'TCL', 'Q1', 'Q1Y']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.warning(f"Columnas faltantes: {missing_cols}")

    # Inicializar contadores
    stats = {}

    # 1. Toques de TCH y TCL (comparados con Q1Y = High del día anterior)
    toco_TCH = (df['TCH'] <= df['Q1Y']).sum()
    toco_TCL = (df['TCL'] <= df['Q1Y']).sum()

    stats['total_dias'] = len(df)
    stats['toco_TCH'] = toco_TCH
    stats['toco_TCH_pct'] = toco_TCH / len(df) * 100
    stats['toco_TCL'] = toco_TCL
    stats['toco_TCL_pct'] = toco_TCL / len(df) * 100

    # 2. Toques exclusivos y ambos
    toco_solo_TCH = ((df['TCH'] <= df['Q1Y']) & (df['TCL'] > df['Q1Y'])).sum()
    toco_solo_TCL = ((df['TCL'] <= df['Q1Y']) & (df['TCH'] > df['Q1Y'])).sum()
    toco_ambos = ((df['TCH'] <= df['Q1Y']) & (df['TCL'] <= df['Q1Y'])).sum()

    stats['toco_solo_TCH'] = toco_solo_TCH
    stats['toco_solo_TCH_pct'] = toco_solo_TCH / len(df) * 100
    stats['toco_solo_TCL'] = toco_solo_TCL
    stats['toco_solo_TCL_pct'] = toco_solo_TCL / len(df) * 100
    stats['toco_ambos'] = toco_ambos
    stats['toco_ambos_pct'] = toco_ambos / len(df) * 100

    # 3. Rupturas de TCH (High > TCH)
    rompio_TCH = df['High'] > df['TCH']
    total_rupturas_TCH = rompio_TCH.sum()

    stats['rompio_TCH'] = total_rupturas_TCH
    stats['rompio_TCH_pct'] = total_rupturas_TCH / len(df) * 100

    # Crear DataFrame de rupturas TCH
    df_rupturas_TCH = df[rompio_TCH].copy()

    if total_rupturas_TCH > 0:
        # Calcular rango de rotura
        df_rupturas_TCH['Rango_Rotura_TCH'] = df_rupturas_TCH['High'] - df_rupturas_TCH['TCH']

        # 4. De las que rompieron TCH, cuántas tocaron Q1
        if 'Q1' in df.columns:
            toco_Q1 = (df_rupturas_TCH['High'] >= df_rupturas_TCH['Q1']).sum()
            no_toco_Q1 = total_rupturas_TCH - toco_Q1

            stats['rompio_TCH_toco_Q1'] = toco_Q1
            stats['rompio_TCH_toco_Q1_pct'] = toco_Q1 / total_rupturas_TCH * 100
            stats['rompio_TCH_no_toco_Q1'] = no_toco_Q1
            stats['rompio_TCH_no_toco_Q1_pct'] = no_toco_Q1 / total_rupturas_TCH * 100

        # Rango promedio de rotura
        stats['rango_promedio_rotura_TCH'] = df_rupturas_TCH['Rango_Rotura_TCH'].mean()
        stats['rango_maximo_rotura_TCH'] = df_rupturas_TCH['Rango_Rotura_TCH'].max()
        stats['rango_minimo_rotura_TCH'] = df_rupturas_TCH['Rango_Rotura_TCH'].min()

        # 5. Vueltas a la zona TCH-TCL
        # Volvió a zona = el Low del día volvió a estar entre TCL y TCH
        volvio_zona = ((df_rupturas_TCH['Low'] >= df_rupturas_TCH['TCL']) &
                      (df_rupturas_TCH['Low'] <= df_rupturas_TCH['TCH'])).sum()

        stats['rompio_TCH_volvio_zona'] = volvio_zona
        stats['rompio_TCH_volvio_zona_pct'] = volvio_zona / total_rupturas_TCH * 100

        # De las que volvieron a zona
        df_volvio_zona = df_rupturas_TCH[
            (df_rupturas_TCH['Low'] >= df_rupturas_TCH['TCL']) &
            (df_rupturas_TCH['Low'] <= df_rupturas_TCH['TCH'])
        ]

        if len(df_volvio_zona) > 0:
            # Cuántas NO bajaron de la zona (Low >= TCL)
            no_bajo_zona = (df_volvio_zona['Low'] >= df_volvio_zona['TCL']).sum()
            stats['volvio_zona_no_bajo_TCL'] = no_bajo_zona
            stats['volvio_zona_no_bajo_TCL_pct'] = no_bajo_zona / volvio_zona * 100

            # Cuántas cerraron por encima de la zona (Close > TCH)
            cerro_encima = (df_volvio_zona['Close'] > df_volvio_zona['TCH']).sum()
            stats['volvio_zona_cerro_encima_TCH'] = cerro_encima
            stats['volvio_zona_cerro_encima_TCH_pct'] = cerro_encima / volvio_zona * 100

    # Logging de resultados
    logger.info(f"\nEstadísticas TCH/TCL:")
    logger.info(f"  Total días analizados: {stats['total_dias']}")
    logger.info(f"  Tocó TCH (TCH <= Q1Y): {stats['toco_TCH']} ({stats['toco_TCH_pct']:.1f}%)")
    logger.info(f"  Tocó TCL (TCL <= Q1Y): {stats['toco_TCL']} ({stats['toco_TCL_pct']:.1f}%)")
    logger.info(f"  Tocó solo TCH: {stats['toco_solo_TCH']} ({stats['toco_solo_TCH_pct']:.1f}%)")
    logger.info(f"  Tocó solo TCL: {stats['toco_solo_TCL']} ({stats['toco_solo_TCL_pct']:.1f}%)")
    logger.info(f"  Tocó ambos: {stats['toco_ambos']} ({stats['toco_ambos_pct']:.1f}%)")
    logger.info(f"  Rompió TCH: {stats['rompio_TCH']} ({stats['rompio_TCH_pct']:.1f}%)")

    if total_rupturas_TCH > 0:
        logger.info(f"  De las que rompieron TCH:")
        if 'rompio_TCH_toco_Q1' in stats:
            logger.info(f"    - Tocaron Q1: {stats['rompio_TCH_toco_Q1']} ({stats['rompio_TCH_toco_Q1_pct']:.1f}%)")
            logger.info(f"    - NO tocaron Q1: {stats['rompio_TCH_no_toco_Q1']} ({stats['rompio_TCH_no_toco_Q1_pct']:.1f}%)")
        logger.info(f"    - Rango promedio rotura: {stats['rango_promedio_rotura_TCH']:.2f} pts")
        logger.info(f"    - Volvieron a zona: {stats['rompio_TCH_volvio_zona']} ({stats['rompio_TCH_volvio_zona_pct']:.1f}%)")

    return stats, df_rupturas_TCH

def analizar_TVH_TVL(df):
    """
    Analiza niveles TVH/TVL con estadísticas detalladas

    IMPORTANTE: TVH y TVL se comparan con Q4Y (Low del día anterior)
    - Toca TVH: TVH >= Q4Y
    - Toca TVL: TVL >= Q4Y

    Args:
        df: DataFrame con datos completos (debe incluir Q4Y)

    Returns:
        dict con estadísticas y DataFrame con detalles de rupturas
    """
    logger.info("\n" + "="*80)
    logger.info("ANALIZANDO NIVELES TVH/TVL")
    logger.info("="*80)

    # Verificar columnas necesarias
    required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'TVH', 'TVL', 'Q4', 'Q4Y']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.warning(f"Columnas faltantes: {missing_cols}")

    # Inicializar contadores
    stats = {}

    # 1. Toques de TVH y TVL (comparados con Q4Y = Low del día anterior)
    toco_TVH = (df['TVH'] >= df['Q4Y']).sum()
    toco_TVL = (df['TVL'] >= df['Q4Y']).sum()

    stats['total_dias'] = len(df)
    stats['toco_TVH'] = toco_TVH
    stats['toco_TVH_pct'] = toco_TVH / len(df) * 100
    stats['toco_TVL'] = toco_TVL
    stats['toco_TVL_pct'] = toco_TVL / len(df) * 100

    # 2. Toques exclusivos y ambos
    toco_solo_TVH = ((df['TVH'] >= df['Q4Y']) & (df['TVL'] < df['Q4Y'])).sum()
    toco_solo_TVL = ((df['TVL'] >= df['Q4Y']) & (df['TVH'] < df['Q4Y'])).sum()
    toco_ambos = ((df['TVH'] >= df['Q4Y']) & (df['TVL'] >= df['Q4Y'])).sum()

    stats['toco_solo_TVH'] = toco_solo_TVH
    stats['toco_solo_TVH_pct'] = toco_solo_TVH / len(df) * 100
    stats['toco_solo_TVL'] = toco_solo_TVL
    stats['toco_solo_TVL_pct'] = toco_solo_TVL / len(df) * 100
    stats['toco_ambos'] = toco_ambos
    stats['toco_ambos_pct'] = toco_ambos / len(df) * 100

    # 3. Rupturas de TVL (Low < TVL)
    rompio_TVL = df['Low'] < df['TVL']
    total_rupturas_TVL = rompio_TVL.sum()

    stats['rompio_TVL'] = total_rupturas_TVL
    stats['rompio_TVL_pct'] = total_rupturas_TVL / len(df) * 100

    # Crear DataFrame de rupturas TVL
    df_rupturas_TVL = df[rompio_TVL].copy()

    if total_rupturas_TVL > 0:
        # Calcular rango de rotura (TVL - Low, valor positivo)
        df_rupturas_TVL['Rango_Rotura_TVL'] = df_rupturas_TVL['TVL'] - df_rupturas_TVL['Low']

        # 4. De las que rompieron TVL, cuántas tocaron Q4
        if 'Q4' in df.columns:
            toco_Q4 = (df_rupturas_TVL['Low'] <= df_rupturas_TVL['Q4']).sum()
            no_toco_Q4 = total_rupturas_TVL - toco_Q4

            stats['rompio_TVL_toco_Q4'] = toco_Q4
            stats['rompio_TVL_toco_Q4_pct'] = toco_Q4 / total_rupturas_TVL * 100
            stats['rompio_TVL_no_toco_Q4'] = no_toco_Q4
            stats['rompio_TVL_no_toco_Q4_pct'] = no_toco_Q4 / total_rupturas_TVL * 100

        # Rango promedio de rotura
        stats['rango_promedio_rotura_TVL'] = df_rupturas_TVL['Rango_Rotura_TVL'].mean()
        stats['rango_maximo_rotura_TVL'] = df_rupturas_TVL['Rango_Rotura_TVL'].max()
        stats['rango_minimo_rotura_TVL'] = df_rupturas_TVL['Rango_Rotura_TVL'].min()

        # 5. Vueltas a la zona TVL-TVH
        # Volvió a zona = el High del día volvió a estar entre TVL y TVH
        volvio_zona = ((df_rupturas_TVL['High'] <= df_rupturas_TVL['TVH']) &
                      (df_rupturas_TVL['High'] >= df_rupturas_TVL['TVL'])).sum()

        stats['rompio_TVL_volvio_zona'] = volvio_zona
        stats['rompio_TVL_volvio_zona_pct'] = volvio_zona / total_rupturas_TVL * 100

        # De las que volvieron a zona
        df_volvio_zona = df_rupturas_TVL[
            (df_rupturas_TVL['High'] <= df_rupturas_TVL['TVH']) &
            (df_rupturas_TVL['High'] >= df_rupturas_TVL['TVL'])
        ]

        if len(df_volvio_zona) > 0:
            # Cuántas NO subieron de la zona (High <= TVH)
            no_subio_zona = (df_volvio_zona['High'] <= df_volvio_zona['TVH']).sum()
            stats['volvio_zona_no_subio_TVH'] = no_subio_zona
            stats['volvio_zona_no_subio_TVH_pct'] = no_subio_zona / volvio_zona * 100

            # Cuántas cerraron por debajo de la zona (Close < TVL)
            cerro_debajo = (df_volvio_zona['Close'] < df_volvio_zona['TVL']).sum()
            stats['volvio_zona_cerro_debajo_TVL'] = cerro_debajo
            stats['volvio_zona_cerro_debajo_TVL_pct'] = cerro_debajo / volvio_zona * 100

    # Logging de resultados
    logger.info(f"\nEstadísticas TVH/TVL:")
    logger.info(f"  Total días analizados: {stats['total_dias']}")
    logger.info(f"  Tocó TVH (TVH >= Q4Y): {stats['toco_TVH']} ({stats['toco_TVH_pct']:.1f}%)")
    logger.info(f"  Tocó TVL (TVL >= Q4Y): {stats['toco_TVL']} ({stats['toco_TVL_pct']:.1f}%)")
    logger.info(f"  Tocó solo TVH: {stats['toco_solo_TVH']} ({stats['toco_solo_TVH_pct']:.1f}%)")
    logger.info(f"  Tocó solo TVL: {stats['toco_solo_TVL']} ({stats['toco_solo_TVL_pct']:.1f}%)")
    logger.info(f"  Tocó ambos: {stats['toco_ambos']} ({stats['toco_ambos_pct']:.1f}%)")
    logger.info(f"  Rompió TVL: {stats['rompio_TVL']} ({stats['rompio_TVL_pct']:.1f}%)")

    if total_rupturas_TVL > 0:
        logger.info(f"  De las que rompieron TVL:")
        if 'rompio_TVL_toco_Q4' in stats:
            logger.info(f"    - Tocaron Q4: {stats['rompio_TVL_toco_Q4']} ({stats['rompio_TVL_toco_Q4_pct']:.1f}%)")
            logger.info(f"    - NO tocaron Q4: {stats['rompio_TVL_no_toco_Q4']} ({stats['rompio_TVL_no_toco_Q4_pct']:.1f}%)")
        logger.info(f"    - Rango promedio rotura: {stats['rango_promedio_rotura_TVL']:.2f} pts")
        logger.info(f"    - Volvieron a zona: {stats['rompio_TVL_volvio_zona']} ({stats['rompio_TVL_volvio_zona_pct']:.1f}%)")

    return stats, df_rupturas_TVL

def crear_tabla_estadisticas(stats_dict, titulo):
    """
    Convierte diccionario de estadísticas en DataFrame formateado

    Args:
        stats_dict: Diccionario con estadísticas
        titulo: Título para la sección

    Returns:
        DataFrame con estadísticas formateadas
    """
    data = []

    # Crear filas de estadísticas con formato legible
    for key, value in stats_dict.items():
        # Formatear nombre de métrica
        metric_name = key.replace('_', ' ').title()

        # Formatear valor
        if isinstance(value, float):
            if 'pct' in key.lower():
                formatted_value = f"{value:.2f}%"
            else:
                formatted_value = f"{value:.2f}"
        else:
            formatted_value = str(value)

        data.append({
            'Metrica': metric_name,
            'Valor': formatted_value
        })

    return pd.DataFrame(data)

def exportar_resultados(df_original, stats_TCH, df_rupturas_TCH, stats_TVL, df_rupturas_TVL):
    """
    Exporta resultados a archivo Excel con múltiples hojas

    Args:
        df_original: DataFrame con datos originales
        stats_TCH: Estadísticas de TCH/TCL
        df_rupturas_TCH: DataFrame con detalles de rupturas TCH
        stats_TVL: Estadísticas de TVH/TVL
        df_rupturas_TVL: DataFrame con detalles de rupturas TVL
    """
    logger.info("\n" + "="*80)
    logger.info("EXPORTANDO RESULTADOS")
    logger.info("="*80)

    try:
        # Crear tablas de estadísticas
        tabla_TCH = crear_tabla_estadisticas(stats_TCH, "Análisis TCH/TCL")
        tabla_TVL = crear_tabla_estadisticas(stats_TVL, "Análisis TVH/TVL")

        # Combinar rupturas TCH y TVL para hoja de detalle
        df_rupturas_TCH_export = df_rupturas_TCH.copy()
        df_rupturas_TCH_export['Tipo_Rotura'] = 'TCH'

        df_rupturas_TVL_export = df_rupturas_TVL.copy()
        df_rupturas_TVL_export['Tipo_Rotura'] = 'TVL'

        # Combinar ambas tablas
        df_detalle_rupturas = pd.concat([df_rupturas_TCH_export, df_rupturas_TVL_export],
                                        ignore_index=True, sort=False)

        # Ordenar por fecha
        if 'Date' in df_detalle_rupturas.columns:
            df_detalle_rupturas = df_detalle_rupturas.sort_values('Date')

        # Exportar a Excel con múltiples hojas
        with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
            # Hoja 1: Datos originales completos
            df_original.to_excel(writer, sheet_name='Datos_Completos', index=False)
            logger.info(f"  Hoja 'Datos_Completos': {len(df_original)} registros")

            # Hoja 2: Análisis TCH/TCL
            tabla_TCH.to_excel(writer, sheet_name='Analisis_TCH_TCL', index=False)
            logger.info(f"  Hoja 'Analisis_TCH_TCL': {len(tabla_TCH)} métricas")

            # Hoja 3: Análisis TVH/TVL
            tabla_TVL.to_excel(writer, sheet_name='Analisis_TVH_TVL', index=False)
            logger.info(f"  Hoja 'Analisis_TVH_TVL': {len(tabla_TVL)} métricas")

            # Hoja 4: Detalle de rupturas
            df_detalle_rupturas.to_excel(writer, sheet_name='Detalle_Rupturas', index=False)
            logger.info(f"  Hoja 'Detalle_Rupturas': {len(df_detalle_rupturas)} rupturas")

        logger.info(f"\nOK Archivo exportado exitosamente:")
        logger.info(f"  {OUTPUT_FILE}")

    except Exception as e:
        logger.error(f"ERROR al exportar resultados: {str(e)}")
        raise

def main():
    """
    Función principal
    """
    try:
        logger.info("\n" + "="*80)
        logger.info("ANÁLISIS DE NIVELES TCH/TCL Y TVH/TVL")
        logger.info("="*80)
        logger.info(f"Archivo entrada: {INPUT_FILE}")
        logger.info(f"Archivo salida: {OUTPUT_FILE}")

        # 1. Cargar datos
        df = cargar_datos()

        # 2. Analizar TCH/TCL
        stats_TCH, df_rupturas_TCH = analizar_TCH_TCL(df)

        # 3. Analizar TVH/TVL
        stats_TVL, df_rupturas_TVL = analizar_TVH_TVL(df)

        # 4. Exportar resultados
        exportar_resultados(df, stats_TCH, df_rupturas_TCH, stats_TVL, df_rupturas_TVL)

        logger.info("\n" + "="*80)
        logger.info("ANÁLISIS COMPLETADO EXITOSAMENTE")
        logger.info("="*80)

        # Resumen final
        logger.info("\nRESUMEN:")
        logger.info(f"  Total días analizados: {len(df)}")
        logger.info(f"  Rupturas TCH: {stats_TCH.get('rompio_TCH', 0)}")
        logger.info(f"  Rupturas TVL: {stats_TVL.get('rompio_TVL', 0)}")
        logger.info(f"  Total rupturas: {stats_TCH.get('rompio_TCH', 0) + stats_TVL.get('rompio_TVL', 0)}")

    except Exception as e:
        logger.error(f"ERROR en análisis: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
